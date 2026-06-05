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
