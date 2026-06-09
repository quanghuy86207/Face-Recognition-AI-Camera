Markdown
 📸 GZONE - Hệ Thống Chấm Công Thông Minh Bằng Khuôn Mặt (Face ID)
Hệ thống quản lý và máy chấm công thời gian thực sử dụng công nghệ thị giác máy tính (**Computer Vision**) để định danh nhân sự qua Camera. Dự án được tối ưu hóa hiệu năng bằng các thuật toán xử lý luồng khung hình thông minh, giúp nhận diện mượt mà, chính xác và giảm tải tối đa cho phần cứng.
✨ Tính Năng Nổi Bật
* **Nhận diện Real-time siêu tốc:** Tích hợp công nghệ *Frame Skipping* (xử lý xen kẽ) kết hợp giảm độ phân giải ma trận ảnh (`fx=0.25, fy=0.25`), tăng đáng kể tốc độ khung hình (FPS), chống lag hoàn hảo trên cả máy cấu hình yếu.
* **Học máy chính xác cao:** Sử dụng thư viện `face_recognition` (dựa trên mô hình Dlib Deep Learning có độ chính xác 99.38% trên tập dữ liệu chuẩn LFW).
* **Quét và Nạp tự động:** Tự động quét thư mục lưu trữ, trích xuất vector đặc trưng 128 số của khuôn mặt và lưu vào bộ nhớ.
* **Giao diện trực quan:** Tự động vẽ khung định vị thông minh, phân biệt màu sắc trực quan (Xanh lá: Nhân viên hệ thống / Đỏ rực: Người lạ) và nhãn tên đẩy lên đỉnh khung hình chống che khuất tầm nhìn.
🏗️ Kiến Trúc Thư Mục Dự Án
Để hệ thống vận hành chính xác, cấu trúc mã nguồn nên được sắp xếp như sau:
text
├── database/               # Thư mục chứa ảnh gốc của nhân sự (Mã_Tên.jpg)
├── app.py                  # Mã nguồn kịch bản chạy nhận diện (Desktop App)
└── README.md               # Hướng dẫn sử dụng hệ thống
⚠️ Lưu ý về quy tắc đặt tên ảnh trong database/: > Hệ thống sẽ tự động bóc tách tên file làm nhãn hiển thị. Bạn nên đặt tên file không dấu và phân tách bằng ký tự gạch dưới để hiển thị đẹp nhất.
Ví dụ: NV01_Quang_Huy.jpg, NV02_Nguyen_Van_A.jpg
🛠️ Hướng Dẫn Cài Đặt
1. Cài đặt các thư viện bổ sung
Hệ thống yêu cầu cài đặt Python (phiên bản khuyên dùng là 3.8 đến 3.11) và các thư viện cốt lõi sau:
pip install opencv-python numpy
Riêng với thư viện face_recognition, bạn cần cài đặt trình biên dịch C++ (CMake) trước khi cài đặt:
pip install cmake
pip install face_recognition
2. Khởi chạy hệ thống
Bước 1: Tạo thư mục database/ và sao chép ảnh chân dung của các thành viên vào trong thư mục này.
Bước 2: Chạy kịch bản nhận diện bằng lệnh:
Bash
python app.py
Bước 3: Hệ thống bật Camera. Để tắt ứng dụng an toàn, bấm phím q trên cửa sổ hiển thị camera.
⚙️ Các Tham Số Tùy Biến Sâu (Fine-Tuning)
Bạn có thể chỉnh sửa trực tiếp các tham số trong file app.py để tối ưu hóa theo môi trường thực tế:
AI_TOLERANCE = 0.48: Khoảng cách toán học tối đa để chấp nhận hai khuôn mặt là một người.
Hạ thấp (Ví dụ 0.40): Hệ thống sẽ cực kỳ nghiêm ngặt, chống chấm công giả mạo tốt nhưng cần đứng thẳng, đủ sáng.
Tăng cao (Ví dụ 0.55): Hệ thống nhạy hơn, dễ nhận diện khi đứng xa nhưng tăng tỷ lệ nhận nhầm người có nét mặt giống nhau.
fx=0.25, fy=0.25: Tỷ lệ nén ảnh để AI tính toán. Giữ nguyên mức 0.25 (giảm 4 lần) để cân bằng tốt nhất giữa hiệu năng (FPS) và độ chính xác ở khoảng cách 1-2 mét.
🛡️ Bản Quyền & Phát Triển
Dự án được phát triển bởi sinh viên PTIT học trò thầy HUỲNH.
Nghiêm cấm mọi hành vi sử dụng mã nguồn vào mục đích giả mạo hoặc xâm phạm quyền riêng tư khi chưa được sự đồng ý của nhân sự.
