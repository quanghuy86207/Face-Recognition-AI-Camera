import face_recognition
import cv2
import numpy as np
import os

# ==========================================================
# BƯỚC 1: TỰ ĐỘNG QUÉT VÀ NẠP "VÂN TAY" KHUÔN MẶT CÓ SẴN
# ==========================================================
known_face_encodings = []
known_face_names = []

path = 'database'

# Tạo thư mục database tự động nếu người dùng chưa tạo
if not os.path.exists(path):
    os.makedirs(path)
    print(f"⚠️ Đã tạo thư mục '{path}'. Hãy ném ảnh các thành viên vào đây rồi chạy lại nhé!")

images = os.listdir(path)
print("--------------------------------------------------")
print("🤖 HỆ THỐNG AI: Đang trích xuất đặc trưng khuôn mặt...")

for img_name in images:
    # Kiểm tra định dạng file ảnh hợp lệ
    if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        # 1. Đọc ảnh gốc
        img = face_recognition.load_image_file(f'{path}/{img_name}')
        
        # 2. Tìm khuôn mặt và biến thành dãy 128 số
        encodings = face_recognition.face_encodings(img)
        
        if len(encodings) > 0:
            known_face_encodings.append(encodings[0])
            # Lấy tên file (bỏ đuôi .jpg) làm tên hiển thị
            name = os.path.splitext(img_name)[0]
            known_face_names.append(name)
            print(f"   + Đã nạp thành công: {name}")
        else:
            print(f"   ❌ Lỗi: Không tìm thấy mặt trong file {img_name}")

print(f"✅ Đã nạp xong tổng cộng {len(known_face_names)} thành viên.")
print("--------------------------------------------------")

# ==========================================================
# BƯỚC 2: KHỞI TẠO CAMERA VÀ NHẬN DIỆN THỜI GIAN THỰC
# ==========================================================
video_capture = cv2.VideoCapture(0)

# Cấu hình độ nhạy (Tolerance): Càng nhỏ càng nghiêm ngặt, càng lớn càng dễ dãi
# Mức chuẩn công nghiệp an toàn nhất là từ 0.45 đến 0.55
AI_TOLERANCE = 0.5 

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Không thể kết nối camera!")
        break

    # Giảm kích thước ảnh xuống 4 lần để AI xử lý siêu nhanh (Tăng FPS)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Chuyển đổi hệ màu từ BGR (OpenCV) sang RGB (Thư viện face_recognition yêu cầu)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Tìm vị trí và mã hóa các khuôn mặt xuất hiện trong camera
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Kiểm tra độ khớp
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=AI_TOLERANCE)
        name = "Nguoi la"

        # Tính khoảng cách toán học chi tiết để chọn người giống nhất
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        # Khôi phục lại kích thước thật (Nhân lại với 4) để vẽ khung sắc nét
        top *= 4; right *= 4; bottom *= 4; left *= 4

        # Thiết lập màu sắc: Xanh lá cho người quen, Đỏ rực cho người lạ
        color = (0, 255, 0) if name != "Nguoi la" else (0, 0, 255)

        # Vẽ hình chữ nhật bao quanh khuôn mặt
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Vẽ thanh nền text phía dưới khung mặt
        cv2.rectangle(frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)
        
        # Ghi tên lên màn hình
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

    # Hiển thị giao diện ứng dụng
    cv2.imshow('He thong Nhan dien Khuon mat Cao cap', frame)

    # Bấm phím 'q' trên bàn phím để tắt hệ thống
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
print("🤖 Hệ thống đã tắt an toàn.")
# ==========================================================
# BƯỚC 2: KHỞI TẠO CAMERA VÀ NHẬN DIỆN THỜI GIAN THỰC (ĐÃ TỐI ƯU CHỐNG LAG)
# ==========================================================
video_capture = cv2.VideoCapture(0)
AI_TOLERANCE = 0.5 

# Các biến hỗ trợ công nghệ "Frame Skipping" (Bỏ qua khung hình)
process_this_frame = True
face_locations = []
face_encodings = []
face_names = []

while True:
    ret, frame = video_capture.read()
    if not ret: break

    # Chỉ cho AI chạy toán học 1 nửa số khung hình (Khung có, khung không)
    if process_this_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=AI_TOLERANCE)
            name = "Nguoi la"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
            
            face_names.append(name)

    # Đảo ngược trạng thái: Khung hình tiếp theo sẽ bị bỏ qua không tính toán AI
    process_this_frame = not process_this_frame

    # Vẽ khung hình và hiện tên (Phần vẽ này vẫn chạy liên tục để mắt thấy mượt)
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4; right *= 4; bottom *= 4; left *= 4

        color = (0, 255, 0) if name != "Nguoi la" else (0, 0, 255)

        # Vẽ hình chữ nhật bao quanh khuôn mặt
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # --- ĐÃ CHỈNH SỬA: ĐƯA CHỮ LÊN TRÊN ĐỈNH KHUNG ---
        # Vẽ thanh nền text phía TRÊN khung mặt (top - 30 đến top)
        cv2.rectangle(frame, (left, top - 30), (right, top), color, cv2.FILLED)
        
        # Ghi tên lên màn hình
        cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

    # Hiển thị giao diện ứng dụng
    cv2.imshow('He thong Nhan dien Khuon mat Cao cap', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
print("🤖 Hệ thống đã tắt an toàn.")