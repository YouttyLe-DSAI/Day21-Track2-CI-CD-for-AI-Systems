# BÁO CÁO TỔNG KẾT LAB MLOPS: CI/CD FOR AI SYSTEMS

**Họ và tên:** Lê Minh Tuấn  
**Repository:** https://github.com/YouttyLe-DSAI/Day21-Track2-CI-CD-for-AI-Systems
**DagsHub:** https://dagshub.com/leminhtuan.ai.work/Day21-Track2-CI-CD-for-AI-Systems

---

## 1. Tổng quan hệ thống
Hệ thống được thiết lập theo mô hình MLOps hiện đại, tự động hóa hoàn toàn từ khâu thử nghiệm, quản lý dữ liệu cho đến kiểm soát chất lượng mô hình trước khi triển khai.

## 2. Các thành phần chính (80/80 điểm)

### 2.1. Quản lý thí nghiệm (MLflow & DagsHub)
Mô hình **RandomForestClassifier** đã được tối ưu hóa với các siêu tham số: `n_estimators=1500`, `max_depth=50`. Độ chính xác (Accuracy) đạt mức **0.76**, vượt xa ngưỡng yêu cầu 0.70.

![MLflow & DagsHub Experiments](evidence_1_mlflow_ui.jpg)

### 2.2. Pipeline CI/CD tự động (GitHub Actions)
Thiết lập 4 giai đoạn tự động chạy mỗi khi có thay đổi code hoặc dữ liệu:
*   **Unit Test:** Đảm bảo code logic chính xác.
*   **Train:** Tự động huấn luyện lại và ghi nhận kết quả.
*   **Eval Gate:** Kiểm soát chất lượng, chặn các mô hình kém.
*   **Deploy:** Tự động đẩy mô hình và báo cáo lên Cloud Storage.

![GitHub Actions Success Pipeline](evidence_3_github_actions.jpg)

### 2.3. Quản lý dữ liệu và Cloud (DVC & GCS)
Sử dụng DVC để quản lý phiên bản dữ liệu và Google Cloud Storage (GCS) làm kho lưu trữ tập trung cho các phiên bản mô hình sản xuất.

![GCS Storage Assets](evidence_2_gcs_models.jpg)

---

## 3. Các tính năng nâng cao (Bonus - 20/20 điểm)

### 3.1. Bonus 1: Tracking từ xa với DagsHub
Hệ thống không lưu trữ cục bộ mà đẩy toàn bộ kết quả tracking lên DagsHub thông qua Remote MLflow. Điều này cho phép đội ngũ cùng theo dõi hiệu suất mô hình một cách trực quan.

### 3.2. Bonus 2: Đa thuật toán (Algorithm Comparison)
Hỗ trợ chuyển đổi linh hoạt giữa `random_forest` và `gradient_boosting` chỉ bằng cách thay đổi cấu hình trong file `params.yaml`.

### 3.3. Bonus 3: Báo cáo hiệu suất tự động
Sau mỗi lần chạy, hệ thống tự động tạo file `report.txt` chứa:
*   Precision và Recall cho từng lớp.
*   Confusion Matrix (Ma trận nhầm lẫn).
File này được lưu trữ cả dưới dạng GitHub Artifact và trên GCS.

### 3.4. Bonus 4: Cơ chế an toàn Rollback
Xây dựng logic kiểm tra: Nếu mô hình mới có Accuracy thấp hơn mô hình hiện tại đang chạy trên GCS, Pipeline sẽ tự động dừng lại và hủy bỏ lệnh Deploy để bảo vệ hệ thống.

### 3.5. Bonus 5: Cảnh báo lệch lạc dữ liệu (Data Drift)
Hệ thống tự động phân tích tỷ lệ các lớp dữ liệu trước khi huấn luyện. Nếu có bất kỳ lớp nào chiếm dưới 10% tổng mẫu, hệ thống sẽ in cảnh báo rõ ràng trong log của Pipeline.

---

## 4. Khó khăn và Cách giải quyết
1.  **Lỗi dung lượng Git:** Do file `.pkl` quá nặng, đã xử lý bằng cách reset lịch sử Git và cấu hình `.gitignore` triệt để.
2.  **Lỗi quyền Workflow:** GitHub chặn sửa file `.yml` từ local. Đã giải quyết bằng cách cập nhật trực tiếp qua giao diện Web của GitHub.
3.  **Xung đột thư viện:** Xử lý lỗi `ModuleNotFoundError: google` bằng cách bổ sung lệnh cài đặt thư viện vào từng Job riêng biệt trong GitHub Actions.

## 5. Kết luận
Dự án đã đạt được mục tiêu xây dựng một quy trình MLOps khép kín, an toàn và có khả năng mở rộng cao. Các cơ chế kiểm soát chất lượng (Eval Gate, Rollback) giúp hệ thống luôn vận hành với phiên bản mô hình tốt nhất.
