# Dự đoán giá nhà sử dụng mô hình học máy — Nhóm 9

## Tổng kết thực hiện

Nhóm đã hoàn thành phân công và các công việc trong kế hoạch 4 tuần. Mức độ hoàn thành được nhóm xác nhận là **100%**; đây là tiến độ công việc, không phải độ chính xác dự đoán của mô hình.

Mã nguồn và hướng dẫn vận hành: [house-price-ml/](house-price-ml/).

## 1. Bảng kế hoạch và mức độ hoàn thành

| Tuần | STT | Nội dung thực hiện | Trạng thái | Hoàn thành |
|---|---:|---|---|---:|
| Tuần 1 | 1 | Tải dữ liệu House Prices; kiểm tra cấu trúc thư mục và repository Git. | Đã hoàn thành | 100% |
| Tuần 1 | 2 | Thống kê dữ liệu, kiểm tra kiểu dữ liệu, missing values, bản ghi trùng lặp và phân phối SalePrice. | Đã hoàn thành | 100% |
| Tuần 1 | 3 | Phân tích khám phá, trực quan hóa và khảo sát tương quan giữa các thuộc tính. | Đã hoàn thành | 100% |
| Tuần 2 | 4 | Xử lý dữ liệu thiếu, ngoại lệ, mã hóa biến phân loại và xây dựng pipeline. | Đã hoàn thành | 100% |
| Tuần 2 | 5 | Chia Train/Test; thiết lập Cross-Validation và mô hình Linear Regression baseline. | Đã hoàn thành | 100% |
| Tuần 2 | 6 | Huấn luyện, tinh chỉnh Decision Tree và Random Forest Regression. | Đã hoàn thành | 100% |
| Tuần 3 | 7 | Huấn luyện, tinh chỉnh Gradient Boosting và XGBoost Regression. | Đã hoàn thành | 100% |
| Tuần 3 | 8 | Đánh giá MAE, RMSE, R²; phân tích overfitting và feature importance. | Đã hoàn thành | 100% |
| Tuần 3 | 9 | Tổng hợp bảng biểu, chọn mô hình và lưu mô hình tốt nhất. | Đã hoàn thành | 100% |
| Tuần 4 | 10 | Xây dựng API Node.js/Express và giao diện HTML/CSS/JavaScript. | Đã hoàn thành | 100% |
| Tuần 4 | 11 | Kiểm thử pipeline, API, dữ liệu đầu vào và giao diện; sửa lỗi. | Đã hoàn thành | 100% |
| Tuần 4 | 12 | Hoàn thiện báo cáo, slide và chuẩn bị thuyết trình. | Đã hoàn thành | 100% |

**Tổng tiến độ: 12/12 công việc đã hoàn thành — 100%.**

## 2. Pipeline chung đã thực hiện

| Tuần | Đầu vào | Công việc đã thực hiện | Đầu ra | Hoàn thành |
|---|---|---|---|---:|
| Tuần 1 | Dữ liệu thô từ Kaggle (train.csv, test.csv) | Tải dữ liệu, khởi tạo Git và cấu trúc thư mục.<br>Thống kê mô tả, kiểm tra kiểu dữ liệu, missing values, trùng lặp.<br>EDA: biểu đồ phân phối SalePrice và khảo sát tương quan. | Repository có dữ liệu; báo cáo thống kê + biểu đồ tương quan làm căn cứ xử lý ở Tuần 2. | 100% |
| Tuần 2 | Dữ liệu thô + kết quả EDA từ Tuần 1 | Xử lý missing values, ngoại lệ, mã hóa biến phân loại.<br>Xây dựng pipeline tiền xử lý dùng chung; chia Train/Test.<br>Huấn luyện Linear Regression (baseline), Decision Tree, Random Forest. | Pipeline tiền xử lý hoàn chỉnh; 3 mô hình đầu tiên đã huấn luyện xong. | 100% |
| Tuần 3 | Pipeline + 3 mô hình đã có từ Tuần 2 | Huấn luyện Gradient Boosting và XGBoost.<br>Đánh giá cả 5 mô hình bằng MAE, RMSE, R², kiểm tra overfitting.<br>Chọn và lưu mô hình tốt nhất. | Bảng so sánh đầy đủ 5 mô hình; 1 mô hình tốt nhất đã lưu, sẵn sàng tích hợp. | 100% |
| Tuần 4 | Mô hình tốt nhất đã lưu từ Tuần 3 | Xây API Node.js/Express chuyển tiếp đến dịch vụ Python/Flask nạp mô hình; xây giao diện nhập liệu.<br>Kiểm thử toàn bộ pipeline, API, giao diện; sửa lỗi.<br>Hoàn thiện báo cáo và slide thuyết trình. | Ứng dụng demo chạy được đầu-cuối; báo cáo và slide sẵn sàng nộp/thuyết trình. | 100% |

## 3. Phân công và đánh giá thành viên

| Thành viên | Vai trò | Công việc phụ trách | Kết quả bàn giao | Mức độ hoàn thành công việc được giao |
|---|---|---|---|---:|
| Trần Hữu Vọng | Leader / Tester | Quản lý repository và cấu trúc dự án; viết README, phối hợp nhóm; xây dựng test case và kiểm thử. | Repository, tài liệu phân công và các trường hợp kiểm thử. | 100% |
| Nguyễn Phúc Khang | Dữ liệu / EDA | Tải dữ liệu House Prices; kiểm tra cấu trúc, kiểu dữ liệu, giá trị thiếu, trùng lặp; thống kê mô tả và khảo sát tương quan. | Bộ dữ liệu, thống kê và kết quả EDA. | 100% |
| Thị Diễm | Tiền xử lý / Metrics | Xây dựng pipeline xử lý giá trị thiếu và mã hóa; xây dựng, đối chiếu các hàm MAE, RMSE, R². | Pipeline tiền xử lý dùng chung và các hàm đánh giá. | 100% |
| Nguyễn Văn Thành | Dev chính | Xây dựng giao diện HTML/CSS/JavaScript, Node.js/Express và kết nối dịch vụ Python/Flask; tích hợp dự đoán, hiển thị kết quả và kiểm thử ứng dụng. | Ứng dụng demo kết nối giao diện, API và mô hình. | 100% |
| Võ Phú Vinh | Huấn luyện mô hình | Huấn luyện và so sánh Linear Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost; cấu hình tham số, xuất kết quả và lưu mô hình. | Kết quả so sánh 5 mô hình và mô hình đã lưu. | 100% |

**Đánh giá chung:** cả 5 thành viên đã hoàn thành 100% phần việc được giao. Tỷ lệ này được tính riêng theo nhiệm vụ của từng người, không cộng thành 500% và không thể hiện tỷ trọng đóng góp.

## 4. Kết quả và đánh giá chung

| Hạng mục | Kết quả bàn giao | Mức độ hoàn thành |
|---|---|---:|
| Dữ liệu và khảo sát | Dữ liệu House Prices cùng thống kê, phân phối giá và tương quan | 100% |
| Tiền xử lý và đánh giá | Pipeline dùng chung; các chỉ số MAE, RMSE, R² và đối chiếu train/test | 100% |
| Mô hình | So sánh đủ 5 thuật toán và lưu mô hình được lựa chọn | 100% |
| Ứng dụng minh họa | Giao diện nhập liệu, API và dự đoán bằng mô hình đã lưu | 100% |
| Kiểm thử | Kiểm tra pipeline, API, đầu vào và giao diện; xử lý lỗi theo phạm vi đồ án | 100% |
| Báo cáo và trình bày | Hoàn thiện báo cáo, slide và chuẩn bị thuyết trình theo xác nhận của nhóm | 100% |

**Kết luận:** nhóm đã hoàn tất kế hoạch thực hiện và có sản phẩm minh họa phục vụ báo cáo đồ án. Kết quả dự đoán cần được đọc cùng các chỉ số sai số và giới hạn dữ liệu; hoàn thành kế hoạch không có nghĩa mô hình dự đoán đúng tuyệt đối.
