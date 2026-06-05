# 🌐 Hệ Thống Chấm Công Nhận Diện Khuôn Mặt AI (AI Time Attendance System)

Hệ thống chấm công trực quan thời gian thực dành cho doanh nghiệp, kết hợp giữa giao diện Web hiện đại (Cyberpunk/Sci-fi dark theme) và lõi xử lý AI nhận diện khuôn mặt tốc độ cao bằng Python. Hệ thống hỗ trợ đăng ký tự động nhiều góc mặt (Burst Mode 10x) và tối ưu hóa chống lag (Frame Skipping).

---

## ✨ Tính Năng Nổi Bật

* **Nhận Diện Thời Gian Thực Cực Mượt:** Sử dụng kỹ thuật giảm độ phân giải xử lý toán học ($fx=0.25, fy=0.25$) và thuật toán **Frame Skipping** (bỏ qua khung hình xen kẽ) giúp giảm tải CPU/GPU, tăng tối đa chỉ số FPS.
* **Đăng Ký Burst Mode 10x:** Tự động hóa quy trình đăng ký nhân sự mới qua Web với 10 chỉ dẫn góc mặt trực quan (nhìn thẳng, quay trái, quay phải, ngẩng lên, mỉm cười...) để tăng độ chính xác khi chấm công.
* **Bảo Mật & Chuẩn Công Nghiệp:** Tích hợp bộ lọc khoảng cách toán học khuôn mặt (nhận diện chính xác nhất) với cấu hình độ nhạy `AI_TOLERANCE = 0.5`.
* **Xuất Dữ Liệu Tự Động:** Lịch sử Check-in/out được cập nhật theo thời gian thực lên giao diện Web và đồng thời xuất dữ liệu lưu trữ trực tiếp ra file `Danh_Sach_Cham_Cong.csv`.

---

## 📂 Cấu Trúc Thư Mục Dự Án

```text
├── app.py                      # Backend Server chính (Flask + AI Logic)
├── templates/
│   └── index.html              # Giao diện Web Client (HTML, CSS, JavaScript)
├── database/                   # Thư mục lưu trữ các file ảnh khuôn mặt mẫu (.jpg)
├── Danh_Sach_Cham_Cong.csv     # File Excel/CSV lưu lịch sử chấm công
└── .gitignore                  # File cấu hình bỏ qua các tệp tin rác khi đẩy lên Git# Face-Recognition-AI-Camera
Face Recognition AI Camera
