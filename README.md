Markdown
# 📸 GZONE - Hệ Thống Chấm Công Thông Minh Bằng Khuôn Mặt (Face ID)

Hệ thống quản lý và máy chấm công thời gian thực sử dụng công nghệ thị giác máy tính (**Computer Vision**) để định danh nhân sự qua Camera. Dự án được tối ưu hóa hiệu năng bằng các thuật toán xử lý luồng khung hình thông minh, giúp nhận diện mượt mà, chính xác và giảm tải tối đa cho phần cứng.

---

## ✨ Tính Năng Nổi Bật

* **Nhận diện Real-time siêu tốc:** Tích hợp công nghệ *Frame Skipping* (xử lý xen kẽ) kết hợp giảm độ phân giải ma trận ảnh (`fx=0.25, fy=0.25`), tăng đáng kể tốc độ khung hình (FPS), chống lag hoàn hảo trên cả máy cấu hình yếu.
* **Học máy chính xác cao:** Sử dụng thư viện `face_recognition` (dựa trên mô hình Dlib Deep Learning có độ chính xác 99.38% trên tập dữ liệu chuẩn LFW).
* **Quét và Nạp tự động:** Tự động quét thư mục lưu trữ, trích xuất vector đặc trưng 128 số của khuôn mặt và lưu vào bộ nhớ.
* **Giao diện trực quan:** Tự động vẽ khung định vị thông minh, phân biệt màu sắc trực quan (Xanh lá: Nhân viên hệ thống / Đỏ rực: Người lạ) và nhãn tên đẩy lên đỉnh khung hình chống che khuất tầm nhìn.

---

## 🏗️ Kiến Trúc Thư Mục Dự Án

Cấu trúc mã nguồn của dự án được sắp xếp gọn gàng như sau:

```text
├── database/               # Thư mục chứa ảnh gốc của nhân sự (Mã_Tên.jpg)
├── app.py                  # Mã nguồn kịch bản chạy nhận diện (Desktop App)
└── README.md               # Hướng dẫn sử dụng hệ thống
⚠️ Quy tắc đặt tên ảnh trong database/:
Hệ thống sẽ tự động bóc tách tên file làm nhãn hiển thị trên camera. Hãy đặt tên file không dấu và phân tách bằng ký tự gạch dưới để hiển thị đẹp nhất.
Ví dụ: NV01_Quang_Huy.jpg, NV02_Nguyen_Van_A.jpg

🛠️ Hướng Dẫn Cài Đặt & Chạy Dự Án
1. Cài đặt các thư viện cần thiết
Dự án yêu cầu cài đặt Python (phiên bản tối ưu: 3.8 đến 3.11) cùng các thư viện cốt lõi sau:

Bash
pip install opencv-python numpy
Riêng đối với thư viện nhận diện khuôn mặt face_recognition, bạn cần cài đặt thêm trình biên dịch C++ (CMake) trước:

Bash
pip install cmake
pip install face_recognition
2. Khởi chạy hệ thống
Bước 1: Tạo thư mục database/ ở cùng cấp với file code và sao chép ảnh chân dung của các thành viên vào đây.

Bước 2: Mở terminal tại thư mục dự án và chạy lệnh:

Bash
  python app.py
Bước 3: Cửa sổ camera sẽ hiển thị để bắt đầu chấm công. Để tắt ứng dụng an toàn, bạn chỉ cần bấm phím q trên bàn phím.

⚙️ Hướng Dẫn Tinh Chỉnh Tham Số Hệ Thống
Để hệ thống hoạt động tốt nhất trong từng môi trường ánh sáng và phần cứng khác nhau, các tham số sau trong file app.py có thể được chỉnh sửa trực tiếp:

AI_TOLERANCE = 0.48: Đây là khoảng cách toán học để kiểm tra độ giống nhau giữa 2 khuôn mặt.

Nếu hạ thấp (Ví dụ: 0.40): Nhận diện sẽ khắt khe hơn, giúp chống chấm công giả mạo rất tốt nhưng đòi hỏi người dùng phải đứng thẳng và đủ sáng.

Nếu tăng cao (Ví dụ: 0.55): Hệ thống sẽ nhạy hơn, đứng xa hoặc góc hơi nghiêng vẫn nhận được nhưng có thể tăng tỷ lệ nhận nhầm nếu 2 người có nét mặt gần giống nhau.

fx=0.25, fy=0.25: Tỷ lệ thu nhỏ khung hình để AI xử lý. Mức 0.25 (giảm độ phân giải đi 4 lần) là con số tối ưu giúp hệ thống chạy mượt mà, không bị trễ hình mà vẫn đảm bảo độ chính xác ở khoảng cách từ 1-2 mét.

🛡️ Bản Quyền & Phát Triển
Dự án được nghiên cứu và phát triển bởi nhóm 10 ,sinh viên PTIT,học trò thầy HUỲNH.

Nghiêm cấm mọi hành vi sử dụng mã nguồn vào mục đích giả mạo thông tin hoặc xâm phạm quyền riêng tư khi chưa được sự đồng ý của nhân sự.
