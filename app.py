from flask import Flask, render_template, request, jsonify, send_file
import face_recognition
import cv2
import numpy as np
import os
import base64
import sqlite3
import csv
import pickle  
from datetime import datetime, timedelta

app = Flask(__name__)

# ==========================================
# 0. KHỞI TẠO CƠ SỞ DỮ LIỆU SQLITE (TỰ ĐỘNG NÂNG CẤP)
# ==========================================
def init_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT NOT NULL,
            emp_name TEXT NOT NULL,
            log_date TEXT NOT NULL,
            log_time TEXT NOT NULL
        )
    ''')
    # Tự động thêm cột phân loại IN/OUT mà không làm mất dữ liệu cũ
    try:
        cursor.execute("ALTER TABLE attendance_logs ADD COLUMN log_type TEXT DEFAULT 'IN'")
    except sqlite3.OperationalError:
        pass 
    conn.commit()
    conn.close()

    

init_db()

# ==========================================
# 1. HỆ THỐNG PICKLE CACHE
# ==========================================
known_face_encodings = []
known_face_info = [] 
path = 'database'
unique_employees = {}
CACHE_FILE = 'face_cache.pkl'

def parse_filename(img_name):
    raw_name = os.path.splitext(img_name)[0]
    base_part = raw_name.split('-')[0]
    parts = base_part.split('_')
    if len(parts) >= 3:
        return parts[0], "_".join(parts[1:-1]), parts[-1]
    elif len(parts) == 2:
        return parts[0], parts[1], "Chưa cập nhật"
    else:
        return "UNKNOWN", base_part, "Chưa cập nhật"

def build_cache():
    global known_face_encodings, known_face_info, unique_employees
    known_face_encodings, known_face_info, unique_employees = [], [], {}
    if os.path.exists(path):
        for img_name in os.listdir(path):
            if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = f'{path}/{img_name}'
                img = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(img)
                if len(encodings) > 0:
                    known_face_encodings.append(encodings[0])
                    emp_id, emp_name, emp_dept = parse_filename(img_name)
                    known_face_info.append({'id': emp_id, 'name': emp_name, 'dept': emp_dept})
                    if emp_id != "UNKNOWN":
                        unique_employees[emp_id] = {'name': emp_name, 'dept': emp_dept}
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump({'encodings': known_face_encodings, 'info': known_face_info, 'unique': unique_employees}, f)

def load_faces():
    global known_face_encodings, known_face_info, unique_employees
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            data = pickle.load(f)
            known_face_encodings, known_face_info, unique_employees = data['encodings'], data['info'], data['unique']
    else:
        build_cache()

load_faces()

# ==========================================
# 2. HỆ THỐNG GHI NHẬN CHẤM CÔNG CÓ IN/OUT
# ==========================================
last_log_time = {} 
COOLDOWN_MINUTES = 1 
LATE_THRESHOLD = "08:30:00"

def mark_attendance(emp_id, emp_name, log_type):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d/%m/%Y")

    if emp_id in last_log_time:
        if now - last_log_time[emp_id] < timedelta(minutes=COOLDOWN_MINUTES):
            return None 

    last_log_time[emp_id] = now
    try:
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO attendance_logs (emp_id, emp_name, log_date, log_time, log_type) VALUES (?, ?, ?, ?, ?)", 
                       (emp_id, emp_name, current_date, current_time, log_type))
        conn.commit()
        conn.close()
    except Exception as e:
        return None
        
    if log_type == 'IN':
        status = "IN (Muộn)" if current_time > LATE_THRESHOLD else "IN (Đúng giờ)"
    else:
        status = "OUT (Tan ca)"
    return f"{current_time} - {status}"

# ==========================================
# 3. ROUTER & API
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_dashboard():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    emp_list = [{'id': k, 'name': v['name'], 'dept': v['dept']} for k, v in unique_employees.items()]
    
    # Gom nhóm dữ liệu ngày, bóc tách giờ IN và giờ OUT dựa trên Nút bấm
    cursor.execute('''
        SELECT log_date, emp_id, emp_name, 
               MIN(CASE WHEN log_type='IN' THEN log_time END) as check_in, 
               MAX(CASE WHEN log_type='OUT' THEN log_time END) as check_out
        FROM attendance_logs
        GROUP BY log_date, emp_id, emp_name
        ORDER BY log_date DESC
    ''')
    raw_logs = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM attendance_logs")
    total_logs = cursor.fetchone()[0]
    conn.close()

    processed_logs = []
    for row in raw_logs:
        log_date, emp_id, emp_name, check_in, check_out = row
        total_time = "---"
        
        in_time_str = check_in if check_in else "Quên IN"
        out_time_str = check_out if check_out else "Chưa OUT"
        
        if check_in and check_out:
            fmt = '%H:%M:%S'
            tdelta = datetime.strptime(check_out, fmt) - datetime.strptime(check_in, fmt)
            total_seconds = int(tdelta.total_seconds())
            if total_seconds > 0:
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                total_time = f"{hours}h {minutes}m"
        
        status = "Đi muộn" if check_in and check_in > LATE_THRESHOLD else ("Đúng giờ" if check_in else "Thiếu IN")

        processed_logs.append({
            'date': log_date, 'id': emp_id, 'name': emp_name,
            'in': in_time_str, 'out': out_time_str, 'total': total_time, 'status': status
        })

    return render_template('admin.html', employees=emp_list, logs=processed_logs, total_emp=len(unique_employees), total_logs=total_logs)

@app.route('/api/daily_stats')
def daily_stats():
    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")
    
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    # Thống kê chỉ đếm những người đã ấn nút IN
    cursor.execute("SELECT emp_id, MIN(log_time) FROM attendance_logs WHERE log_date = ? AND log_type = 'IN' GROUP BY emp_id", (current_date,))
    today_logs = cursor.fetchall()
    conn.close()

    checked_in_ids = []
    late_count = 0
    for emp_id, first_time in today_logs:
        # CHỈ ĐẾM NHỮNG NGƯỜI CÒN TỒN TẠI TRONG HỆ THỐNG (Lọc người đã bị xóa)
        if emp_id in unique_employees:
            checked_in_ids.append(emp_id)
            if first_time > LATE_THRESHOLD: 
                late_count += 1
            
    not_checked_in = [f"[{emp_id}] {data['name']}" for emp_id, data in unique_employees.items() if emp_id not in checked_in_ids]
    return jsonify({'total': len(unique_employees), 'checked': len(checked_in_ids), 'late': late_count, 'missing': not_checked_in})

@app.route('/manual_checkin', methods=['POST'])
def manual_checkin():
    data = request.get_json()
    emp_id = data.get('emp_id', '').strip()
    log_type = data.get('log_type', 'IN')  # Lấy trạng thái nút bấm
    
    if not emp_id: return jsonify({'success': False, 'message': 'Vui lòng nhập mã!'})

    if emp_id in unique_employees:
        emp_name = unique_employees[emp_id]['name']
        emp_dept = unique_employees[emp_id]['dept']
        log_result = mark_attendance(emp_id, emp_name, log_type)
        if log_result:
            return jsonify({'success': True, 'emp_id': emp_id, 'emp_name': emp_name, 'emp_dept': emp_dept, 'log': log_result})
        else:
            return jsonify({'success': False, 'message': f'Vừa quét xong, vui lòng đợi 1 phút!'})
    else:
        return jsonify({'success': False, 'message': f'Mã [{emp_id}] không tồn tại!'})

@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        data = request.json['image']
        log_type = request.json.get('log_type', 'IN')  # Lấy trạng thái nút bấm
        
        encoded_data = data.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=2)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        attendance_msgs = []
        first_person = None 
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    emp_info = known_face_info[best_match_index]
                    if not first_person:
                        first_person = {'id': emp_info['id'], 'name': emp_info['name'], 'dept': emp_info['dept']}
                    
                    log_result = mark_attendance(emp_info['id'], emp_info['name'], log_type)
                    if log_result:
                        attendance_msgs.append(log_result)

        _, buffer = cv2.imencode('.jpg', frame)
        result_image = "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            'image': result_image, 
            'new_logs': attendance_msgs,
            'emp_id': first_person['id'] if first_person else "N/A",
            'emp_name': first_person['name'] if first_person else "Người lạ",
            'emp_dept': first_person['dept'] if first_person else "---"
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name') 
    image_data = data.get('image')

    try:
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        filename = f"{name}.jpg"
        filepath = os.path.join('database', filename)
        
        with open(filepath, "wb") as f:
            f.write(image_bytes)

        new_img = face_recognition.load_image_file(filepath)
        new_encodings = face_recognition.face_encodings(new_img)

        if len(new_encodings) > 0:
            known_face_encodings.append(new_encodings[0])
            emp_id, emp_name, emp_dept = parse_filename(filename)
            known_face_info.append({'id': emp_id, 'name': emp_name, 'dept': emp_dept})
            unique_employees[emp_id] = {'name': emp_name, 'dept': emp_dept}
            
            with open(CACHE_FILE, 'wb') as f:
                pickle.dump({'encodings': known_face_encodings, 'info': known_face_info, 'unique': unique_employees}, f)
            return jsonify({'success': True})
        else:
            os.remove(filepath) 
            return jsonify({'success': False})
    except Exception as e:
        return jsonify({'success': False})

@app.route('/delete_employee/<emp_id>', methods=['POST'])
def delete_employee(emp_id):
    try:
        if os.path.exists(path):
            for img_name in os.listdir(path):
                if img_name.startswith(f"{emp_id}_"):
                    os.remove(os.path.join(path, img_name))
        build_cache()
        return jsonify({'success': True, 'message': f'Đã xóa nhân sự {emp_id} thành công!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi khi xóa: {str(e)}'})

@app.route('/export_logs')
def export_logs():
    file_path = 'Bao_Cao_Cham_Cong.csv'
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT log_date, emp_id, emp_name, 
               MIN(CASE WHEN log_type='IN' THEN log_time END) as check_in, 
               MAX(CASE WHEN log_type='OUT' THEN log_time END) as check_out
        FROM attendance_logs
        GROUP BY log_date, emp_id, emp_name
        ORDER BY log_date DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Ngày', 'Mã NV', 'Họ và Tên', 'Giờ Vào (IN)', 'Giờ Ra (OUT)', 'Tổng Thời Gian'])
        for row in rows:
            log_date, emp_id, emp_name, check_in, check_out = row
            in_time_str = check_in if check_in else "Quên IN"
            out_time_str = check_out if check_out else "Chưa OUT"
            total_time = "---"
            
            if check_in and check_out:
                fmt = '%H:%M:%S'
                tdelta = datetime.strptime(check_out, fmt) - datetime.strptime(check_in, fmt)
                total_seconds = int(tdelta.total_seconds())
                if total_seconds > 0:
                    total_time = f"{total_seconds // 3600}h {(total_seconds % 3600) // 60}m"
            
            writer.writerow([log_date, emp_id, emp_name, in_time_str, out_time_str, total_time])
            
    return send_file(file_path, as_attachment=True)


@app.route('/clear_attendance', methods=['POST'])
def clear_attendance():
    data = request.get_json()
    target_date = data.get('date') # Nhận ngày từ giao diện
    try:
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        
        if target_date and target_date != "all":
            # Xóa theo ngày được chọn
            cursor.execute("DELETE FROM attendance_logs WHERE log_date = ?", (target_date,))
        else:
            # Xóa toàn bộ nếu không chọn ngày
            cursor.execute("DELETE FROM attendance_logs")
            
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Đã xóa dữ liệu ngày {target_date if target_date else "tất cả"}!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi: {str(e)}'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)