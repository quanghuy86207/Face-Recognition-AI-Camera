from flask import Flask, render_template, request, jsonify
import face_recognition
import cv2
import numpy as np
import os
import base64
import csv
from datetime import datetime, timedelta

app = Flask(__name__)

# ==========================================
# 1. NẠP DỮ LIỆU & TỔNG SỐ NHÂN VIÊN
# ==========================================
known_face_encodings = []
known_face_info = [] 
path = 'database'

# SỬ DỤNG 'set()' ĐỂ TỰ ĐỘNG LỌC TRÙNG LẶP MÃ NHÂN VIÊN
unique_employees = set() 

if os.path.exists(path):
    for img_name in os.listdir(path):
        if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = face_recognition.load_image_file(f'{path}/{img_name}')
            encodings = face_recognition.face_encodings(img)
            if len(encodings) > 0:
                known_face_encodings.append(encodings[0])
                
                raw_name = os.path.splitext(img_name)[0]
                try:
                    emp_id, full_name = raw_name.split('_')
                    emp_name = full_name.split('-')[0] 
                except ValueError:
                    emp_id = "UNKNOWN"
                    emp_name = raw_name.split('-')[0]

                known_face_info.append({'id': emp_id, 'name': emp_name})
                
                # Ném Mã NV vào set. Nếu NV01 đã có rồi, nó sẽ tự động bỏ qua, không đếm 10 lần nữa.
                unique_employees.add(emp_id)

print(f"✅ Đã nạp thành công {len(unique_employees)} nhân viên vào hệ thống.")

# ==========================================
# 2. HỆ THỐNG GHI NHẬN CHẤM CÔNG
# ==========================================
last_log_time = {} 
COOLDOWN_MINUTES = 1 

def mark_attendance(emp_id, emp_name):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d/%m/%Y")

    if emp_id in last_log_time:
        time_diff = now - last_log_time[emp_id]
        if time_diff < timedelta(minutes=COOLDOWN_MINUTES):
            return None 

    last_log_time[emp_id] = now
    file_path = 'Danh_Sach_Cham_Cong.csv'
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Ngày', 'Giờ', 'Mã Nhân Viên', 'Họ và Tên'])
        writer.writerow([current_date, current_time, emp_id, emp_name])
    
    return f"{current_time} - {emp_name}"

# ==========================================
# 3. KẾT NỐI VỚI GIAO DIỆN WEB
# ==========================================
@app.route('/')
def index():
    # Truyền tổng số nhân sự ĐÃ LỌC TRÙNG LẶP ra giao diện web
    return render_template('index.html', total_emp=len(unique_employees))

@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        data = request.json['image']
        encoded_data = data.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=2)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        names_found = []
        attendance_msgs = []
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Người lạ"
            emp_id = ""
            
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    emp_info = known_face_info[best_match_index]
                    name = emp_info['name']
                    emp_id = emp_info['id']
                    
                    log_result = mark_attendance(emp_id, name)
                    if log_result:
                        attendance_msgs.append(log_result)
            
            names_found.append(f"[{emp_id}] {name}" if emp_id else name)

        _, buffer = cv2.imencode('.jpg', frame)
        result_image = "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')
        final_name = ", ".join(names_found) if names_found else "Không tìm thấy khuôn mặt"

        return jsonify({'name': final_name, 'image': result_image, 'new_logs': attendance_msgs})
    
    except Exception as e:
        return jsonify({'name': f"Lỗi: {str(e)}", 'image': None, 'new_logs': []})

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
            
            try:
                emp_id, full_name = name.split('_')
                emp_name = full_name.split('-')[0]
            except ValueError:
                emp_id = "UNKNOWN"
                emp_name = name.split('-')[0]

            known_face_info.append({'id': emp_id, 'name': emp_name})
            
            # Khai báo sử dụng biến đếm toàn cục
            global unique_employees
            unique_employees.add(emp_id) # Thêm Mã NV mới vào set lọc trùng
            
            return jsonify({'success': True, 'message': f'✅ Đã ghi danh: [{emp_id}] {emp_name}'})
        else:
            os.remove(filepath) 
            return jsonify({'success': False, 'message': '❌ Không thấy khuôn mặt, hãy thử lại!'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi hệ thống: {str(e)}'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)