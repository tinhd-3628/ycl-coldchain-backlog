# ycl-coldchain-backlog

**食品コールドチェーン業務支援システム (YCL) — Backlog, GitHub Project và báo cáo tiến độ (LAB-5)**

| | |
|---|---|
| Dự án | YCL — hệ thống quản lý chuỗi kho lạnh thực phẩm cho ユキコールドロジスティクス (khách giả lập) |
| Học viên | Huynh Duc Tin (GitHub `tinhd-3628`) · mã học viên: không có, định danh bằng tên và tài khoản GitHub |
| Đề | **Product B** — chuỗi kho lạnh thực phẩm |

## Tổng quan

- **Nguồn break:** bộ thiết kế chi tiết LAB-4 (`LAB4/specs/`, bản nộp 2026-10-28; to-be PL duyệt 2026-10-26). Gồm 18 spec màn to-be, ERD to-be, 13 ADR và bảng gap prototype ↔ thiết kế. Bộ spec không đưa vào repo này (đề ghi "không phải nộp lại bộ spec"); mã DLT/GAP/ADR trong tài liệu là mã của bộ LAB-4.
- **PREMISE.md có thay đổi:**
  - Không sửa thiết kế màn nào của LAB-4.
  - Thêm công đoạn kiểm thử tích hợp (1 task QA mỗi story).
  - Hoãn 6 dòng GAP chưa đủ thiết kế.
  - Ghi rõ 2 việc bị sót lúc break (GAP-066, test tải 80 user); đã bổ sung thành T-167, T-168 sau Sprint 1.
  - Thêm các giả định về đội hình, lịch sprint, mốc UAT, cách tính giờ QA.

  Xem [PREMISE.md](PREMISE.md).
- **Backlog:**
  - **18 epic**, 50 story, 168 task (117 dev + 51 test/QA) = 236 issue.
  - **711 SWP** (đã qua PL review), **1.934h**.
  - PIC giả định: epic = PL; story và task = BE-1/2/3, FE-1/2, QA-1/2.
  - Hạng mục giờ lái xe tải 2024 tách riêng ở E-11 và E-12 (nhãn `constraint:driver-hours-2024`).
- **Sprint giả lập đã chạy:** **Sprint 1** (2026-11-02 → 2026-11-13). Kết quả: 26 task, Done 19 (77/118 SWP); 6 đang làm, 1 chưa bắt đầu. Xem [progress-report.md](progress-report.md).

## Link

| | |
|---|---|
| Repo | https://github.com/tinhd-3628/ycl-coldchain-backlog |
| GitHub Project | https://github.com/users/tinhd-3628/projects/1 (view *Project Overall* và *Sprint Detail view*) |
| Báo cáo HTML chấm SWP | [`reports/sun-estimate-ycl-coldchain-backlog-20261029-1818.html`](reports/sun-estimate-ycl-coldchain-backlog-20261029-1818.html) (task dev)<br>[`reports/sun-estimate-ycl-coldchain-backlog-qa-tasks-20261029-1911.html`](reports/sun-estimate-ycl-coldchain-backlog-qa-tasks-20261029-1911.html) (task QA) |
| Mở thử bằng cửa sổ ẩn danh | **Chưa** — repo và Project đang private, sẽ chuyển public và kiểm tra trước khi nộp _(cập nhật dòng này sau khi kiểm)_ |

## Cấu trúc repo

| File / thư mục | Nội dung |
|---|---|
| `README.md` | File này |
| [`PREMISE.md`](PREMISE.md) | Backlog khác LAB-4 ở đâu: spec thêm/bỏ/sửa, giả định bổ sung, hướng đã chốt |
| [`task-breakdown.md`](task-breakdown.md) | Nguyên tắc chia task; spec → issue; hạng mục giờ lái 2024; chỗ hở của spec LAB-4 |
| [`estimate.md`](estimate.md) | Issue mẫu và PL chốt SWP; cách quy giờ; tổng theo epic; so với estimate LAB-1 |
| [`progress-report.md`](progress-report.md) | Báo cáo Sprint 1 (JP / VI): trạng thái, burndown, rủi ro trễ |
| [`AI-report.md`](AI-report.md) | Skill và prompt đã dùng; cách review output AI; điểm làm tốt / chưa tốt |
| [`backlog/`](backlog/) | Nguồn sự thật và script:<br>• `backlog-breakdown.yaml` (epic/story/task, giờ, mốc, sprint), `backlog-translations-vi.yaml`<br>• `backlog-swp-reviewed.json` (SWP đã duyệt), `sprint-1-simulation.yaml`<br>• script Python tạo issue, field, view và áp dữ liệu giả lập<br>• `github-issue-map.json` (số issue và trạng thái đã đồng bộ) |
| [`reports/`](reports/) | Hai báo cáo HTML của `tkm:sun-estimate` (mở offline được) |
| `.gitignore` | Bỏ cache Python khỏi repo |

Không có thư mục `skills/`: bài này chỉ dùng skill Takumi sẵn có.

## Spec → epic

Mã màn theo LAB-4 (`LAB4/specs/design/screens/SCR-xxx_*/spec.md`). Một màn có thể đổ vào nhiều epic; ánh xạ tới từng story và task ở [task-breakdown.md §2](task-breakdown.md#2-spec--issue).

| Spec (LAB-4 hoặc PREMISE) | Epic trên Project | Ghi chú |
|---|---|---|
| SCR-014, SCR-015, SCR-016 | [#1](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/1) — E-02 入荷検品・受入判定 (kiểm hàng nhập & phán định tiếp nhận) | Dải nhiệt có version (ADR-0005); mã bò 10 số, không đệm số 9 → 10 |
| SCR-025 | [#9](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/9) — E-03 ロット・在庫状態管理 (trạng thái lô & tồn) | Chặn giải phóng lô đang trong case thu hồi |
| SCR-033, SCR-034, SCR-062 (lịch sử giao đã nhận) | [#12](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/12) — E-06 期限・引当ルール (quy tắc hạn dùng & phân bổ) | 消費期限 (hạn an toàn) chặn cứng, 賞味期限 (hạn ngon nhất) chỉ cảnh báo. 日付逆転 so với lần giao gần nhất của đúng cặp khách × SKU (ADR-0006). 1/3, 1/2 là điều kiện hợp đồng, không phải luật |
| SCR-033, SCR-034 | [#17](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/17) — E-08 引当・ピッキング・積込 (phân bổ, lấy hàng, xếp xe) | Ràng buộc cứng (消費期限 chặn cứng…) kiểm lại trong transaction (ADR-0004, 0007); đo EXPLAIN với 300.000 dòng xuất. Test tải 80 user đồng thời: T-168 #235 (bổ sung sau Sprint 1) |
| SCR-033 | [#20](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/20) — E-09 出荷前検査・出荷確定 (xác nhận xuất) | |
| SCR-062 | [#22](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/22) — E-10 配送完了（POD）・クレーム (hoàn tất giao) | POD offline mã hoá, idempotent (ADR-0012) |
| SCR-051, SCR-053, SCR-054; `design/features/driver-hours-compliance/`; ADR-0008 | [#27](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/27) — E-11 ルート計画・拘束時間チェック (lập tuyến & giờ ràng buộc) | **Ràng buộc đặc thù: giờ lái xe tải từ 2024.** Tách riêng, nhãn `constraint:driver-hours-2024` (task-breakdown §3) |
| SCR-052, SCR-053; ADR-0008 | [#32](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/32) — E-12 ルート公開・運行管理 (công bố tuyến & vận hành) | **Ràng buộc đặc thù: giờ lái xe tải từ 2024.** Tuyến vi phạm không được công bố |
| SCR-070, SCR-074, SCR-079; `design/features/temperature-zone-policy-and-exception/` | [#35](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/35) — E-13 温度データ取込・評価 (dữ liệu nhiệt) | Ngưỡng 3 dải nhiệt là chính sách riêng của Yuki, có version (ADR-0005, 0009) |
| SCR-072, SCR-074 | [#40](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/40) — E-14 アラーム・逸脱管理 (cảnh báo & sai lệch) | |
| SCR-080 | [#44](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/44) — E-16 トレーサビリティ検索 (truy xuất) | Bắt buộc theo luật chỉ với gạo và thịt bò |
| SCR-082 | [#47](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/47) — E-17 回収管理 (thu hồi) | |
| SCR-080, SCR-082 | [#51](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/51) — E-19 監査エビデンス・保持 (bằng chứng kiểm toán) | Lưu giữ / legal hold (GAP-061) hoãn — PREMISE §1 |
| SCR-101, SCR-054, SCR-079 (duyệt master) | [#53](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/53) — E-20 マスター管理 (master) | AGR-008 / AGR-014 để 未設定, không gán mặc định (LAB-4 D-02) |
| ADR-0003, 0010, 0011; SCR-014, SCR-062 (phiên máy dùng chung) | [#56](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/56) — E-21 認証・権限・監査ログ (xác thực, quyền, nhật ký) | GAP-066: T-167 #236 (bổ sung sau Sprint 1) |
| SCR-051 (IF-MAP-01), SCR-072 / SCR-082 (IF-MAIL-01) | [#61](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/61) — E-22 外部連携 (liên kết ngoài) | T-114 ước thời gian chạy là đầu vào của giờ lái |
| LAB-4 PREMISE §4.6, GAP-065 | [#64](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/64) — E-23 データ移行 (migration) | Không tự suy ngày bẩn, không đệm mã bò 9 số |
| ADR-0013, GAP-057, GAP-058 | [#66](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/66) — E-24 共通基盤・非機能 (nền tảng chung) | |
| PREMISE §1 dòng 1 (công đoạn QA) | Trải trên mọi epic: #189–#234 | 1 task QA mỗi story |
