# PREMISE — Backlog LAB-5 khác bản LAB-4 ở đâu

Gốc so sánh: bộ thiết kế LAB-4 `LAB4/specs/` (bản nộp 2026-10-28; phần to-be PL duyệt 2026-10-26). Mã spec dùng nguyên của LAB-4:
- `DLT-xxx-nn` là dòng Delta trong `design/screens/SCR-xxx_*/spec.md`.
- `GAP-nnn` là dòng trong `database/prototype-vs-design-gap.md`.
- `D-nn`, `Q-new-nn`, `QA-nnn` nằm trong `PREMISE.md` của LAB-4.

Số `#n` là issue của repo này: `https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/n`.

Tóm tắt:
- Không sửa thiết kế màn hình nào của LAB-4.
- Backlog **thêm** công đoạn kiểm thử tích hợp mà LAB-4 không có.
- Backlog **hoãn** 6 dòng GAP chưa đủ thiết kế để break; GAP-068 không cần việc.
- Lúc break **sót** 2 việc: GAP-066 và test tải 80 user (NFR-PERF-01). Đã bổ sung sau Sprint 1 thành T-167 #236 và T-168 #235.
- Các giả định bổ sung chỉ lấp chỗ LAB-4 để ngỏ: đội hình, lịch sprint, mốc UAT, cách tính giờ QA.

## 1. Spec thêm / bỏ / sửa so với LAB-4

| Spec | Thêm/Bỏ/Sửa | Trước → sau | Vì sao | Issue bị ảnh hưởng |
|---|---|---|---|---|
| Công đoạn kiểm thử tích hợp cho từng story (LAB-4 không có dòng spec nào) | Thêm | **Trước:** 4 task test đặc thù lấy từ dòng Verification của ADR và NFR (T-034, T-056, T-090, T-112; tổng 64h, bằng 4,3% giờ dev). **Sau:** mỗi story có 1 task QA (thêm 46 task, tổng 50 task, 422h) | PL review board sau khi break: 46/50 story có task BE/FE nhưng không có task QA. Ở estimate LAB-1, QA chiếm 15,61 MM so với BE + FE 54,39 MM (khoảng 28%). Backlog 4,3% là thiếu hẳn một công đoạn | #189–#234 (T-121..T-166); SWP và giờ của 46 story cha cộng thêm |
| GAP-016 (棚卸 — kiểm kê), GAP-017 (訂正 — đính chính), GAP-061 (lưu giữ / legal hold), GAP-063 (job nhập ERP) — đều P1 | Bỏ khỏi đợt break này (hoãn) | **Trước:** cột "Ứng viên task LAB-5" của file gap có ghi. **Sau:** không có issue | Màn hình gắn với các GAP này (SCR-026..029, SCR-095, SCR-013/032/108) không nằm trong 18 màn to-be của LAB-4. Chúng không có dòng DLT và không có điều kiện nghiệm thu, nên không cắt được thành task 1–3 ngày có tiêu chí "xong". Ghi ở [task-breakdown.md §2](task-breakdown.md#2-spec--issue) | Không có |
| GAP-018 (gợi ý put-away), GAP-064 (định nghĩa KPI) — P2 | Bỏ khỏi đợt này (hoãn) | Như trên | GAP-018: cột To-be của LAB-4 ghi "chốt với PL quy tắc gợi ý put-away" mà chưa chốt. GAP-064 thuộc FG-18 (báo cáo, KPI), không có màn to-be | Không có |
| GAP-066 (`idempotency_keys` chuyển sang schema `private`) — P2 | Thêm (bổ sung sau Sprint 1 vì lúc break bị sót) | **Trước:** có trong file gap nhưng backlog không có task. **Sau:** T-167 (8h, 3 SWP), Sprint 2 | Lúc break bị sót: dòng này không gắn màn hình nào nên không lọt vào các story theo màn. Phát hiện khi đối chiếu tự động mã GAP với `refs` của task | #236 T-167 (story E-21-S03 #59) |
| LAB-4 PREMISE §4.5 NFR-PERF-01: p95 đọc ≤ 2s / ghi ≤ 3s với **80 user đồng thời**; "kịch bản test tải ở staging là ứng viên task LAB-5" | Thêm (bổ sung sau Sprint 1 vì lúc break bị sót) | **Trước:** chỉ có T-033 đo EXPLAIN với 300.000 dòng và T-090 đo truy xuất 60 giây. **Sau:** thêm T-168 test tải staging 80 user, không rút về 42 (16h, 6 SWP), Sprint 2 | Khi break, NFR được gắn vào task của màn (T-033), nên phần test tải toàn hệ thống không có chỗ đứng. Phát hiện khi đối chiếu ghi chú README với điều kiện nghiệm thu thật của task | #235 T-168 (story E-08-S01 #18, cùng story với kiểm tranh chấp phân bổ) |


GAP-068 (CHECK người lập ≠ người duyệt) không thêm, bỏ hay sửa gì. Cột To-be của LAB-4 ghi "giữ nguyên ba CHECK", và các bảng duyệt mới đã mang điều kiện "作成者 ≠ 承認者" (người lập ≠ người duyệt) ngay trong task (vd. T-005, T-078, T-104).

Không đổi spec màn hình, ERD to-be hay ADR nào. Phương án wireframe dùng đúng phương án LAB-4 đã chọn (xem §3).

## 2. Giả định bổ sung

Chỉ lấp chỗ LAB-4 và RFP để ngỏ. Không đè lên khối nào RFP đã nêu rõ: giờ lái theo FR-SCH-02, 80 user đồng thời, 300.000 dòng, AGR-008/014 để 未設定 (chưa thiết lập).

| # | Giả định | Chỗ spec/RFP để ngỏ | Ảnh hưởng tới issue/estimate |
|---|---|---|---|
| A-1 | Phạm vi backlog = chênh lệch to-be ↔ as-built của **18 màn to-be** + nền tảng chung (ADR, GAP). Các chức năng Option 1 còn lại sẽ break khi có thiết kế to-be của chúng | LAB-4 chọn Option 1 全機能 (toàn bộ chức năng) nhưng chỉ thiết kế to-be 18 màn lõi (`README §1`, `design/screens/`) | 50 story ứng với 50/98 chức năng LAB-1; còn 48 chức năng chưa có issue (task-breakdown §2). Tổng giờ không so trực tiếp được với tổng LAB-1 (estimate.md §4) |
| A-2 | Đội hình giả định: BE-1/2/3, FE-1/2, QA-1/2. Trường PIC là vai trò, không phải người thật; Assignees trên GitHub đều là tài khoản học viên | LAB-4 không nêu đội thực hiện. LAB-1 chỉ có nhân lực tính theo người-tháng (MM) | Trường PIC của 168 task; 18 epic gán PL (người chịu trách nhiệm chung). Backend dùng chung một nhóm BE-1/2/3 để cân tải (§3) |
| A-3 | Năng lực 70h/người/sprint (10 ngày × 8h, trừ khoảng 10% họp và review) | Không có trong LAB-4 | Xếp sprint. Còn 2 chỗ quá tải ở Sprint 2: BE-2 74h (T-118), BE-3 78h (T-120) |
| A-4 | 6 sprint × 2 tuần từ 2026-11-02, nghỉ 2026-12-28 → 2027-01-03; 3 mốc UAT giả lập 2026-12-01 / 2027-01-05 / 2027-02-02 | LAB-4 không có lịch thực hiện. Mốc go-live 2027-06-01 của RFP không đổi; các mốc UAT chỉ dùng cho bài tập | Trường Iteration, Milestone, Due Date của epic |
| A-5 | Giờ ước lượng trực tiếp cho từng task, 8h = 1 ngày | LAB-1 quy đổi 1 人日 (người-ngày) = 7h | Khi so với LAB-1, đổi người-ngày LAB-1 × 7h (estimate.md §4) |
| A-6 | Giờ task QA = 28% giờ dev của story, làm tròn tới bội số 2h, tối thiểu 4h | LAB-4 không có thiết kế test. Tỉ lệ lấy theo LAB-1: QA 15,61 MM / (BE 36,05 + FE 18,34) MM | 46 task QA, 358h. QA trung bình 1,75h/SWP, dev 3,1h/SWP (estimate.md §2) |
| A-7 | Sprint 1 là dữ liệu giả lập (`backlog/sprint-1-simulation.yaml`), không phải việc thật. Ngày đóng issue trên GitHub là ngày chạy script (2026-10-29), không phải ngày giả lập | Đề cho phép "1 sprint/chu kỳ giả lập" | progress-report.md lấy ngày từ file YAML, không lấy `closed_at` |

## 3. Hướng đã chốt

| Vấn đề | Các phương án ở LAB-4 | Phương án chốt | Vì sao |
|---|---|---|---|
| Chia công đoạn QA | LAB-4 không có. Khi break xét 3 cách: (a) 1 task QA mỗi story; (b) 1 task QA mỗi epic; (c) gộp test vào task dev | (a), giờ theo A-6 | Story là đơn vị có điều kiện nghiệm thu (LAB-1 story §9). Gộp theo epic thì task QA quá to: E-11 sẽ thành khoảng 68h (28% của 242h dev), trái nguyên tắc 1–3 ngày. Gộp vào task dev thì không còn người kiểm độc lập |
| PIC backend | LAB-4 không nêu. Xét: cố định theo miền (BE-1 phân bổ, BE-2 tuyến/giờ lái, BE-3 nhập kho/nhiệt) hoặc dùng chung nhóm BE-1/2/3 | Dùng chung nhóm, người nhà theo miền được ưu tiên trước | Cố định theo miền làm 1 người vượt 70h/sprint. Dùng chung nhóm làm 29 task đổi PIC, tải đều hơn (còn 2 chỗ quá tải, A-3) |
| Wireframe SCR-016 / 053 / 054 / 079 | LAB-4 có option A/B (`wireframes/options/`); spec to-be đã ghi phương án chọn: 016 → A, 053 → A, 054 → B, 079 → A | Giữ nguyên | PL đã duyệt 2026-10-26; khi break không gặp lý do đổi. Task tham chiếu đúng option (vd. T-007 `options/SCR-016 案A`, T-061 `options/SCR-054 案B`) |
| AGR-008 / AGR-014 khi chuyển dữ liệu hợp đồng | LAB-4 D-02 và PREMISE §4.6: để 未設定, đi business-review, không gán ONE_THIRD | Giữ nguyên, ghi thành điều kiện nghiệm thu của T-100 ("既定値を入れない" — không điền mặc định) | Đúng ràng buộc RFP. Sprint 1 giả lập kiểm lại điểm này (progress-report §3) |
| Giờ lái xe tải 2024 | LAB-4 PREMISE §4.8 và ADR-0008: dùng giá trị FR-SCH-02, không nới | Giữ nguyên; tách thành E-11, E-12 có nhãn `constraint:driver-hours-2024` | Đề LAB-5 yêu cầu tách riêng. Chi tiết ở task-breakdown §3 |
