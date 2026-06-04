import cv2
import os

# 1. Yêu cầu nhập tên trước khi bật camera
print("=========================================")
print("📸 HỆ THỐNG ĐĂNG KÝ KHUÔN MẶT MỚI")
name = input("Nhập tên người mới (Viết không dấu, VD: Quang_Huy): ")

# Đảm bảo thư mục database luôn tồn tại
path = 'database'
if not os.path.exists(path):
    os.makedirs(path)

# 2. Bật camera
cap = cv2.VideoCapture(0)
print("\n[HƯỚNG DẪN]:")
print("- Nhìn thẳng vào camera.")
print("- Nhấn phím 's' để CHỤP VÀ LƯU.")
print("- Nhấn phím 'q' để HỦY BỎ.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Lỗi: Không thể bật camera!")
        break

    # Vẽ một khung hướng dẫn người dùng để mặt vào giữa
    height, width, _ = frame.shape
    cv2.rectangle(frame, (width//2 - 150, height//2 - 200), (width//2 + 150, height//2 + 200), (0, 255, 255), 2)
    cv2.putText(frame, "De khuon mat vao trong khung", (width//2 - 140, height//2 - 210), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

    cv2.imshow("Dang ky khuon mat", frame)

    key = cv2.waitKey(1) & 0xFF
    
    # Bấm 's' (Save) để chụp
    if key == ord('s'):
        file_path = f"{path}/{name}.jpg"
        # Bỏ đi khung vẽ màu vàng trước khi lưu ảnh gốc
        ret, clean_frame = cap.read() 
        cv2.imwrite(file_path, clean_frame)
        print(f"\n✅ THÀNH CÔNG! Đã lưu khuôn mặt của '{name}' vào thư mục {path}.")
        break
    
    # Bấm 'q' (Quit) để thoát
    elif key == ord('q'):
        print("\n❌ Đã hủy bỏ thao tác đăng ký.")
        break

cap.release()
cv2.destroyAllWindows()