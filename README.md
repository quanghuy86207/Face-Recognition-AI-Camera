<<<<<<< HEAD
=======
Markdown
# 🌐 Hệ Thống Chấm Công Nhận Diện Khuôn Mặt AI (AI Time Attendance System)

Hệ thống chấm công thời gian thực dành cho doanh nghiệp kết hợp giữa giao diện Web hiện đại (Cyberpunk dark theme) và lõi xử lý AI nhận diện khuôn mặt tốc độ cao bằng Python. Hệ thống hỗ trợ cả chế độ đăng ký/nhận diện trực tuyến qua Web và công cụ đăng ký ngoại tuyến (offline) bằng OpenCV.

---

## 📂 Cấu Trúc Thư Mục Dự Án

Dựa theo cấu trúc mã nguồn hiện tại:

```text
├── templates/
│   └── index.html              # Giao diện Web Client (HTML, CSS, JavaScript)
├── .gitignore                  # Cấu hình bỏ qua các tệp tin rác/bảo mật khi đẩy lên Git
├── README.md                   # Tài liệu hướng dẫn dự án (File này)
├── add_face.py                 # Công cụ đăng ký khuôn mặt offline bằng OpenCV qua Terminal
├── app.py                      # Flask Server chính - Xử lý API nhận diện và Burst Mode Web
├── main.py                     # File logic chạy thử nghiệm hoặc lõi xử lý phụ
└── ngrok.exe                   # Công cụ chuyển tiếp cổng (Port Forwarding) để chạy Web qua Internet
✨ Tính Năng Nổi Bật
-Nhận Diện Thời Gian Thực Chống Lag: Sử dụng kỹ thuật giảm độ phân giải hình ảnh ($fx=0.25, fy=0.25$)
kết hợp công nghệ Frame Skipping giúp hệ thống chạy siêu mượt trên các máy cấu hình phổ thông.
-Đăng Ký Đa Năng: * Qua Web (Burst Mode 10x): Tự động chụp 10 góc mặt khác nhau theo chỉ dẫn trên màn hình.
-Qua Local Script (add_face.py): Sử dụng phím tắt OpenCV để chụp khuôn mặt nhanh ngay trên máy chủ.
-Xuất Dữ Liệu Tự Động: Lịch sử Check-in/out lưu trữ trực tiếp ra tệp tin CSV cục bộ và cập nhật Real-time lên bảng nhật ký Web.
-Hỗ Trợ Triển Khai Từ Xa: Tích hợp sẵn ngrok.exe giúp public nhanh server local ra internet để test camera trên điện thoại hoặc máy trạm khác.
🛠️ Hướng Dẫn Cài Đặt & Khởi Chạy
1. Cài đặt thư viện phụ thuộc
Yêu cầu hệ thống đã cài đặt Python 3.8+ và gói C++ biên dịch (cho thư viện dlib). Mở Terminal tại thư mục này và chạy lệnh:
pip install flask opencv-python face_recognition numpy
2. Sử dụng công cụ Đăng ký khuôn mặt Offline (Tùy chọn)
Nếu bạn muốn đăng ký nhanh khuôn mặt cho nhân viên trực tiếp bằng camera của máy chủ không qua giao diện web:
python add_face.py
3. Khởi chạy Hệ thống Web chính
Để mở toàn bộ hệ thống giao diện chấm công và phân quyền tự động:
python app.py
4. Cách sử dụng Ngrok để chấm công từ xa
Nếu muốn chạy hệ thống chấm công này thông qua mạng Internet (tiện cho việc test camera bằng thiết bị di động bên ngoài):
Mở Terminal mới tại thư mục dự án.
Chạy lệnh:
ngrok http 5000
Sao chép đường dẫn có đuôi *.ngrok-free.app (sử dụng giao thức https://) và mở trên trình duyệt của thiết bị khác.
🔒 Quy định File .gitignore
Hệ thống được cấu hình tự động bỏ qua các thư mục dữ liệu nội bộ sau để tránh rò rỉ thông tin lên các nền tảng public như GitHub:
Không lưu cache Python (__pycache__/).
Không đẩy thư mục ảnh gốc nhân sự (database/).
Không đẩy báo cáo dữ liệu chấm công (Danh_Sach_Cham_Cong.csv).
🌐 Phát triển bởi: Hệ Thống AI Doanh Nghiệp (Tối ưu hóa thời gian thực).
>>>>>>> 11944467b383e745b92986c7d6436557e5030a47
