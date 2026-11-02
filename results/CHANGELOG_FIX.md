# Nhật ký hoàn thiện HomeValue Lab

## Phạm vi

Đồng bộ code và Word với bộ mô hình đã tinh chỉnh lưu trong gói Round1. Giữ nguyên dữ liệu CSV gốc, bản sao trọng số và kết quả trước tinh chỉnh. Lần hoàn thiện này chạy lại suy luận, xuất báo cáo và kiểm thử; không chạy lại tìm kiếm siêu tham số lịch sử.

Đã sửa chẩn đoán bốn mức, tách chỉ số theo train/holdout/unknown, bổ sung trang Quy trình, tham số trước/sau, đặc trưng quan trọng, đổi đơn vị diện tích ở UI, định dạng tiền và khởi động demo một lệnh. XGBoost dùng định dạng UBJSON để tránh phụ thuộc bản chụp bộ nhớ.

## Bảng trước và sau do code đọc từ tuning_summary.csv

| Model | CV gốc có Id USD | CV gốc bỏ Id USD | CV sau USD | MAE holdout trước USD | MAE holdout sau USD |
|---|---:|---:|---:|---:|---:|
| Linear Regression | 19894.989309 | 20026.418205 | 20026.418205 | 20594.936853 | 20420.499821 |
| Decision Tree | 24641.684904 | 25102.582480 | 24404.830912 | 25754.333182 | 25895.711944 |
| Random Forest | 18276.919302 | 18265.393037 | 17337.203954 | 17634.873836 | 16880.350711 |
| Gradient Boosting | 16235.178116 | 16096.958371 | 15043.516960 | 17099.275711 | 15814.429493 |
| XGBoost | 16329.826172 | 16175.364063 | 15393.440234 | 15822.881702 | 16178.732556 |

Winner theo CV: Gradient Boosting. Không đổi winner theo kết quả holdout.

## Output kiểm thử thật

### python scripts/prepare_vnd_audit.py

Exit code: 0

```text
Linear Regression final holdout MAE USD 20420.49982101374
Decision Tree final holdout MAE USD 25895.71194391829
Random Forest final holdout MAE USD 16880.35071114779
Gradient Boosting final holdout MAE USD 15814.429493030604
XGBoost final holdout MAE USD 16178.732555650686
AUDIT EXPORTED: no fit, 79 features; final selection hash verified
```

### python scripts/export_vnd.py

Exit code: 0

```text
Đã xuất proof_vnd.json, doi_chieu_30_can_VND.csv và model_results_VND.csv
Exported final feature importance, holdout plot and training report; no model fitted.
```

### python scripts/prepare_final_report.py

Exit code: 0

```text
Generated EDA, current TRAIN/TEST, CV tables, process manifest and figures from actual code.
```

### python scripts/verify_vnd.py

Exit code: 0

```text
PASS 55 checks
Linear Regression Khoảng cách nhỏ
Decision Tree Khoảng cách lớn
Random Forest Khoảng cách lớn
Gradient Boosting Khoảng cách lớn
XGBoost Khoảng cách vừa
```

### python scripts/verify_dynamic.py

Exit code: 0

```text
PASS 85 dynamic numerical checks
```

### python scripts/verify_training_report.py

Exit code: 0

```text
PASS 53 training report checks
```

### python scripts/verify_round1.py

Exit code: 0

```text
PASS 94 round1 checks
```

### python scripts/verify_portable_xgboost.py

Exit code: 0

```text
PASS 33 portable checks; max prediction difference = 0 USD; Booster pickle blocked; no retraining.
```

### python scripts/verify_completion.py

Exit code: 0

```text
PASS 83 completion checks
```

### node scripts/smoke_http.mjs

Exit code: 0

```text
PASS HTTP: five real pipelines, prices/metrics, decomposition, CSV 150 rows and invalid model.
```

### node scripts/smoke_dynamic_http.mjs

Exit code: 0

```text
PASS dynamic HTTP: arbitrary inputs, actual lookup beyond 30, complete 1459-row Kaggle test × 5, missing-label guards and true model explanations.
```

### node scripts/browser_check.mjs

Exit code: 0

```text
PASS 17 real-browser checks
```

### verification_launchers.json

```json
{
  "status": "PASS",
  "passed": 4,
  "failed": 0,
  "checks": [
    "Production supervisor serves health through PORT=3002",
    "Supervisor forwards termination and exits",
    "Local demo starts Express and Flask",
    "Ctrl+C stops local demo cleanly"
  ]
}
```

### verification_git_artifacts.json

```json
{
  "status": "PASS",
  "passed": 23,
  "checks": [
    "git add autocrlf=true preserves models/best_model.pkl",
    "git add autocrlf=true preserves models/feature_defaults.json",
    "git add autocrlf=true preserves data/train.csv",
    "git add autocrlf=true preserves data/test.csv",
    "git add autocrlf=true preserves results/model_results.csv",
    "git add autocrlf=true preserves models/final/manifest.json",
    "git add autocrlf=true preserves results/tuning_selection.json",
    "checkout autocrlf=false models/best_model.pkl",
    "checkout autocrlf=false models/feature_defaults.json",
    "checkout autocrlf=false data/train.csv",
    "checkout autocrlf=false data/test.csv",
    "checkout autocrlf=false results/model_results.csv",
    "checkout autocrlf=false models/final/manifest.json",
    "checkout autocrlf=false results/tuning_selection.json",
    "API engine starts after false checkout",
    "checkout autocrlf=true models/best_model.pkl",
    "checkout autocrlf=true models/feature_defaults.json",
    "checkout autocrlf=true data/train.csv",
    "checkout autocrlf=true data/test.csv",
    "checkout autocrlf=true results/model_results.csv",
    "checkout autocrlf=true models/final/manifest.json",
    "checkout autocrlf=true results/tuning_selection.json",
    "API engine starts after true checkout"
  ],
  "integrity_guard_disabled": false,
  "data_or_weights_modified": false
}
```

## Chạy lại từ đầu

Cài Python và Node.js; mở PowerShell trong thư mục dự án:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm ci
.\.venv\Scripts\python.exe scripts/start_demo.py
```

Không cần huấn luyện lại để trình chiếu. Nếu chủ động tái tạo thực nghiệm, sao lưu trước rồi chạy:

```powershell
.\.venv\Scripts\python.exe scripts/backup_original.py
.\.venv\Scripts\python.exe notebooks_or_src_py/tune_models.py --force
.\.venv\Scripts\python.exe notebooks_or_src_py/train_all.py --force
.\.venv\Scripts\python.exe scripts/prepare_vnd_audit.py
.\.venv\Scripts\python.exe scripts/export_vnd.py
.\.venv\Scripts\python.exe scripts/prepare_final_report.py
npm install --no-save --package-lock=false playwright
npx playwright install chromium
.\.venv\Scripts\python.exe scripts/run_all_checks.py
```

## Giới hạn đã ghi nhận

Dockerfile/Render chưa được build hoặc deploy thực tế ở môi trường tạo gói. Holdout từng được xem ở bản cũ, vì vậy cần dữ liệu kiểm nghiệm mới. CV cải thiện không bảo đảm mọi chỉ số holdout cải thiện. Biểu đồ và ảnh màn hình có vị trí dán trong Word; nhóm cần chèn hình thật và cập nhật mục lục trước khi in.

## Các tệp mới hoặc khác so với ZIP đã giao trước

Danh sách được sinh bằng đối chiếu byte; bao gồm kết quả được tái xuất.

- `.dockerignore`
- `.gitattributes`
- `.gitignore`
- `Dockerfile`
- `README.md`
- `config/display.json`
- `data/data_description.txt`
- `data/sample_submission.csv`
- `data/test.csv`
- `data/train.csv`
- `docs/RENDER_GIT_FIX.md`
- `docs/WINDOWS_FIX.md`
- `docs/archive/HousePrice_Code_Final_before_sync.zip`
- `docs/history/HUONG_DAN_THANH.md`
- `docs/history/KET_QUA_DEMO_THANH.json`
- `docs/history/README.md`
- `docs/history/README_DYNAMIC.md`
- `docs/history/README_VND.md`
- `models/_backup_original/best_model.pkl`
- `models/_backup_original/feature_defaults.json`
- `models/_backup_original/manifest.json`
- `models/_backup_original/vnd_supplement/boosting.pkl`
- `models/_backup_original/vnd_supplement/forest.pkl`
- `models/_backup_original/vnd_supplement/linear.pkl`
- `models/_backup_original/vnd_supplement/tree.pkl`
- `models/best_model.manifest.json`
- `models/best_model.pkl`
- `models/feature_defaults.json`
- `models/final/boosting.pkl`
- `models/final/forest.pkl`
- `models/final/linear.pkl`
- `models/final/manifest.json`
- `models/final/tree.pkl`
- `models/final/xgboost.pkl`
- `models/final/xgboost.ubj`
- `models/final/xgboost_preprocess.pkl`
- `models/vnd_supplement/.forest.pkl.YVJd2s`
- `models/vnd_supplement/boosting.pkl`
- `models/vnd_supplement/forest.pkl`
- `models/vnd_supplement/linear.pkl`
- `models/vnd_supplement/tree.pkl`
- `notebooks_or_src_py/eda.py`
- `notebooks_or_src_py/export_defaults.py`
- `notebooks_or_src_py/metrics.py`
- `notebooks_or_src_py/model_utils.py`
- `notebooks_or_src_py/preprocess.py`
- `notebooks_or_src_py/train_all.py`
- `notebooks_or_src_py/train_compare.py`
- `notebooks_or_src_py/tune_models.py`
- `package-lock.json`
- `public/app.js`
- `public/examples/holdout_30.csv`
- `public/examples/train_30.csv`
- `public/index.html`
- `public/styles.css`
- `render.yaml`
- `requirements.txt`
- `results/ROUND1_REPORT.md`
- `results/actual_vs_predicted.png`
- `results/baseline_original/correlation_heatmap.png`
- `results/baseline_original/doi_chieu_30_can_VND.csv`
- `results/baseline_original/manifest.json`
- `results/baseline_original/missing_values_report.csv`
- `results/baseline_original/model_results.csv`
- `results/baseline_original/model_results_VND.csv`
- `results/baseline_original/proof_vnd.json`
- `results/baseline_original/repository_evidence.json`
- `results/baseline_original/saleprice_distribution.png`
- `results/baseline_original/source_before_round1.zip`
- `results/baseline_original/training_holdout_report.json`
- `results/baseline_original/verification_dynamic.json`
- `results/baseline_original/verification_training_report.json`
- `results/baseline_original/verification_vnd.json`
- `results/baseline_original/vnd_audit_source.json`
- `results/baseline_original/xgboost_feature_importance.csv`
- `results/baseline_original/xgboost_feature_importance.png`
- `results/chuan_hoa/CV_truoc_sau.csv`
- `results/chuan_hoa/du_doan_TEST_chi_tiet.csv`
- `results/chuan_hoa/du_doan_TRAIN_chi_tiet.csv`
- `results/chuan_hoa/ket_qua_TEST.csv`
- `results/chuan_hoa/ket_qua_TRAIN.csv`
- `results/doi_chieu_30_can_VND.csv`
- `results/eda_report.json`
- `results/figures/hinh_3_3_phan_phoi_gia.png`
- `results/figures/hinh_3_4_tuong_quan.png`
- `results/figures/hinh_3_5.png`
- `results/figures/hinh_3_6.png`
- `results/final_test_results.json`
- `results/missing_values_report.csv`
- `results/model_results.csv`
- `results/model_results_VND.csv`
- `results/pipeline_manifest.csv`
- `results/pipeline_manifest.json`
- `results/proof_vnd.json`
- `results/render_failure_diagnosis.json`
- `results/repository_evidence.json`
- `results/round1_test_results.json`
- `results/training_holdout_report.json`
- `results/tuning_cv_results/boosting_log.json`
- `results/tuning_cv_results/boosting_raw.json`
- `results/tuning_cv_results/forest_log.json`
- `results/tuning_cv_results/forest_raw.json`
- `results/tuning_cv_results/tree_raw.json`
- `results/tuning_cv_results/xgboost_log.json`
- `results/tuning_cv_results/xgboost_raw.json`
- `results/tuning_report.json`
- `results/tuning_selection.json`
- `results/tuning_summary.csv`
- `results/verification_browser.json`
- `results/verification_completion.json`
- `results/verification_dynamic.json`
- `results/verification_git_artifacts.json`
- `results/verification_launchers.json`
- `results/verification_portable_xgboost.json`
- `results/verification_round1.json`
- `results/verification_training_report.json`
- `results/verification_vnd.json`
- `results/vnd_audit_source.json`
- `results/windows_fix_results.json`
- `results/xgboost_feature_importance.csv`
- `results/xgboost_feature_importance.png`
- `results/xgboost_portable_reference.json`
- `scripts/backup_original.py`
- `scripts/browser_check.mjs`
- `scripts/export_portable_xgboost.py`
- `scripts/export_vnd.py`
- `scripts/prepare_final_report.py`
- `scripts/prepare_vnd_audit.py`
- `scripts/report_round1.py`
- `scripts/run_all_checks.py`
- `scripts/run_round1_checks.py`
- `scripts/smoke_dynamic_http.mjs`
- `scripts/smoke_http.mjs`
- `scripts/start_demo.ps1`
- `scripts/start_demo.py`
- `scripts/start_production.py`
- `scripts/verify_completion.py`
- `scripts/verify_dynamic.py`
- `scripts/verify_git_artifacts.py`
- `scripts/verify_portable_xgboost.py`
- `scripts/verify_round1.py`
- `scripts/verify_training_report.py`
- `scripts/verify_vnd.py`
- `scripts/wait_ready.mjs`
- `server.js`
- `service/audit_engine.py`
- `service/flexible_engine.py`
- `service/predict_service.py`
- `service/training_report.py`
