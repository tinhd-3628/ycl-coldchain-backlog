# Estimate — SWP và giờ ước lượng của backlog

**Báo cáo HTML của skill chấm SWP (`tkm:sun-estimate`)**:
- [`reports/sun-estimate-ycl-coldchain-backlog-20261029-1818.html`](reports/sun-estimate-ycl-coldchain-backlog-20261029-1818.html) — 120 task ban đầu (116 task dev + 4 task test đặc thù) (lượt 1).
- [`reports/sun-estimate-ycl-coldchain-backlog-qa-tasks-20261029-1911.html`](reports/sun-estimate-ycl-coldchain-backlog-qa-tasks-20261029-1911.html) — 46 task QA thêm sau (lượt 2). Lưu ý: tổng story và epic trong báo cáo này chỉ cộng task QA.

Mở bằng trình duyệt, không cần mạng (dữ liệu nhúng trong file). Giá trị cuối cùng đã ghi lên trường `SWP` của Project nằm ở [`backlog/backlog-swp-reviewed.json`](backlog/backlog-swp-reviewed.json).

SWP = bảng tra Scope (S ∈ 1, 2, 3, 5, 8, 13) × Complexity (C ∈ 0, 1, 2, 3, 5, 8) của skill. Task được chấm trực tiếp; story và epic là tổng của con.

Kết quả: **168 task = 711 SWP**:
- dev 482 SWP (117 task);
- test/QA 229 SWP (46 task QA sinh thêm 204 SWP + 5 task test đặc thù 25 SWP).

## 1. Issue mẫu skill chọn để kiểm

Skill tự chọn 5 issue mẫu mỗi lượt theo quy tắc cố định: thấp nhất, trung vị dưới, cao nhất, lệch nhất, độ tin cậy thấp nhất. PL duyệt từng issue qua hai câu hỏi: chọn mức (rất dễ → rất khó), rồi chọn điểm cụ thể.

**Lượt 1: 120 task ban đầu (AI chấm 494 → sau review 498 SWP; 18 task đổi điểm)**

| Issue | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |
|---|---|---|---|
| [#91](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/91) T-023 Query đếm POD chưa đồng bộ + dòng migration chờ review (thấp nhất) | S1 × C1 → **1** | S2 × C1 → **3** | Không phải một truy vấn đơn: gộp 2 nguồn (POD chưa đồng bộ và migration chờ review) theo cặp khách × SKU, kèm test |
| [#139](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/139) T-071 UI SCR-052: BlockPanel, cột lịch sử (trung vị dưới) | S3 × C1 → **4** | S3 × C0 → **3** | Chủ yếu hiển thị dữ liệu sự kiện đã có trên một màn |
| [#97](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/97) T-029 Hàm SQL kiểm 5 ràng buộc cứng trong transaction phân bổ (cao nhất) | S5 × C2 → **8** | S5 × C3 → **10** | 5 kiểm tra chặn cứng (消費期限, dải nhiệt, truy xuất, cửa sổ giao, 日付逆転) chạy trong cùng transaction. Đây là lõi an toàn thực phẩm, nặng hơn mức AI chấm |
| [#74](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/74) T-006 evaluate_zone_match tham chiếu đơn dải nhiệt tạm (lệch nhất) | S1 × C2 → **2** | giữ **2** | Một hàm, lọc theo hạn và trạng thái duyệt. Điểm AI khớp với độ khó PL thấy |
| [#69](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/69) T-001 Parser GS1-128, đối chiếu GTIN–SKU (tin cậy thấp nhất) | S2 × C2 → **3** | S5 × C2 → **8** | AI đọc thành "sửa một màn". Thực tế là parser có AI độ dài thay đổi (FNC1), đối chiếu GTIN–SKU, cần test nhiều mẫu mã vạch |

Lan điều chỉnh: skill chỉ áp sang task có **đúng cùng nhóm** (cùng chuyên môn, loại việc, chữ ký scope và complexity), không cộng trừ đồng loạt.

| Quy tắc | Từ issue mẫu | Áp cho | Thay đổi |
|---|---|---|---|
| cal-001 | #97 | Task DB nhiều thành phần, có trạng thái và tranh chấp | #114 6 → 9 |
| cal-002 | #91 | Task DB đơn thành phần, việc thường | #70, #81, #83: 3 → 4 |
| cal-003 | #139 | Task UI có trạng thái. PL chọn "áp cho cả nhóm" | 10 task giảm 1 bậc C: #88, #92, #113, #115, #129, #134, #151, #156, #159, #166 |
| cal-004 | #69 | Không có task nào cùng nhóm | chỉ #69 |

**Lượt 2: 46 task QA (204 SWP, giữ nguyên)**

| Issue | Skill chấm | Bạn chốt | Lý do |
|---|---|---|---|
| [#189](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/189) T-121 QA ghi nhận kiểm hàng nhập (thấp nhất) | S2 × C1 → 3 | giữ 3 | Một màn, 5 dòng chênh lệch, quy tắc thường |
| [#227](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/227) T-159 QA SSO & MFA (trung vị dưới) | S2 × C3 → 4 | giữ 4 | Ít dòng nhưng có IdP bên ngoài và an toàn xác thực |
| [#206](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/206) T-138 QA hàng đợi POD ngoại tuyến (cao nhất) | S5 × C3 → 10 | giữ 10 | Cả cơ chế đồng bộ offline: retry, xung đột, đồng bộ lại |
| [#210](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/210) T-142 QA tổng hợp giờ ràng buộc thực tế (lệch nhất) | S5 × C2 → 8 | giữ 8 | 13 dòng chênh lệch, nhiều ca biên giờ lái / nghỉ / chờ, P0 |
| [#190](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/190) T-122 QA đối chiếu dải nhiệt khi nhập (tin cậy thấp nhất) | S2 × C2 → 3 | giữ 3 | Một màn nhưng nhiều ca biên nhiệt độ |

Vì sao giữ nguyên cả 5 (lượt 2):
- Thứ tự điểm AI khớp thứ tự độ khó PL thấy: nặng nhất là POD offline và giờ lái, nhẹ nhất là một màn nhập. Không có ô nào lệch bậc.
- PL chọn "chấp nhận tất cả" nên không phát sinh quy tắc lan.
- Còn một điểm phải theo dõi: giờ trên mỗi SWP của QA thấp hơn hẳn dev (§2).

**Lượt 3: 2 task bổ sung sau Sprint 1** (chấm trực tiếp theo cùng bảng Scope × Complexity, không chạy lại skill nên không có trong 2 báo cáo HTML)

| Issue | AI chấm | Bạn chốt | Lý do |
|---|---|---|---|
| [#236](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/236) T-167 Chuyển `idempotency_keys` sang schema private, job dọn khoá hết hạn (8h) | S2 × C2 → 3 | giữ **3** | Hai việc (chuyển schema / quyền, job dọn), phải giữ đúng kết quả cho request gửi lại. 2,7h/SWP, sát mức chung |
| [#235](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/235) T-168 Test tải 80 user đồng thời trên staging (16h) | S3 × C3 → 6 | giữ **6** | Ba kịch bản (phân bổ, ghi kiểm hàng nhập, tra cứu), đo p95 và kiểm tranh chấp khi tải. 2,7h/SWP |

Vì sao không chạy lại skill: chỉ có 2 issue. Bước chọn 5 issue mẫu của skill không có ý nghĩa với 2 issue, và chạy lại cả quy trình tốn token. PL xem và chốt trực tiếp cả hai.

## 2. Cách quy ra giờ

**Cách đã chọn: ước giờ trực tiếp từ từng issue.** Không đổi từ SWP ra giờ.

| | Quy tắc | Áp dụng |
|---|---|---|
| Task dev | Ước từ dưới lên khi break, dựa trên nội dung dòng DLT/GAP và code prototype đang có. 8h = 1 ngày; mỗi task 4–24h (§1 task-breakdown) | 117 task, 1.496h (gồm T-167 bổ sung). Giờ có trước khi chấm SWP |
| Task QA sinh thêm | 28% giờ dev của story, làm tròn tới bội số 2h, tối thiểu 4h ([`backlog/backlog_qa_tasks.py`](backlog/backlog_qa_tasks.py), PREMISE A-6) | 46 task, 358h |
| 5 task test đặc thù | Ước trực tiếp như task dev | 80h (gồm T-168 bổ sung) |
| Story, epic | Tổng giờ của task con, không ước riêng | Script tính, ghi vào `Estimate (h)` |

Vì sao không đổi từ SWP:
- Giờ được ước trước, độc lập với SWP. Giữ hai thước đo độc lập để chúng **kiểm chéo nhau**.
- Khi tỉ lệ giờ/SWP của một task lệch xa mức chung, đó là dấu hiệu một trong hai con số sai.
- Lúc nộp chưa có dữ liệu velocity thật để lập quy ước đổi SWP ra giờ. Sprint 1 giả lập chưa đủ làm cơ sở.

Kết quả kiểm chéo (dữ liệu tính từ backlog):

| Nhóm | Tỉ lệ giờ/SWP | Nhận xét |
|---|---|---|
| Task dev (117) | trung bình 3,1h; theo epic từ 2,7 (E-12, E-17) đến 4,0 (E-09, E-11) | Đều nhau, trừ các task lệch bên dưới |
| Task QA sinh thêm (46) | 1,75h | Thấp hơn dev gần một nửa. Nghĩa là quy tắc 28% có thể thiếu giờ cho story test nặng (vd. T-138 POD offline 10 SWP / 22h), hoặc AI chấm QA hơi cao. Theo dõi bằng giờ thực tế (Sprint 1: 3 task QA xong dùng 19h so với 18h dự kiến) |
| Lệch cao: T-061 #129, T-066 #134 (24h, 3 SWP), T-083 #151 (20h, 3 SWP) | 6,7–8h | Cả ba là màn lớn bị quy tắc cal-003 kéo xuống 1 bậc. Quy tắc này lấy từ #139, một màn chỉ hiển thị. Lan cho cả nhóm UI có trạng thái đã làm các màn nhiều form và panel bị đánh thấp. **Cần review lại 10 task của cal-003** |
| Lệch thấp: T-001 #69 (12h, 8 SWP), T-046 #114 (12h, 9 SWP) | 1,3–1,5h | PL nâng SWP nhưng chưa xem lại giờ. Sprint 1: T-001 dùng 14h/12h |

## 3. Tổng theo epic

| Epic | Số issue (story / task) | Tổng SWP | Tổng giờ | Ghi chú |
|---|---|---|---|---|
| [#1](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/1) E-02 入荷検品・受入判定 | 7 / 22 (15 dev + 7 QA) | 84 | 230 | UAT 3rd (story cuối) |
| [#9](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/9) E-03 ロット・在庫状態管理 | 2 / 7 (5 + 2) | 22 | 68 | UAT 3rd |
| [#12](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/12) E-06 期限・引当ルール | 4 / 11 (7 + 4) | 41 | 98 | UAT 2nd |
| [#17](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/17) E-08 引当・ピッキング・積込 | 2 / 11 (8 + 3) | 51 | 146 | UAT 2nd; có T-029 (10 SWP) và T-168 test tải bổ sung |
| [#20](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/20) E-09 出荷前検査・出荷確定 | 1 / 2 (1 + 1) | 6 | 16 | UAT 2nd |
| [#22](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/22) E-10 配送完了（POD）・クレーム | 4 / 16 (12 + 4) | 76 | 190 | UAT 3rd; POD offline |
| [#27](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/27) E-11 ルート計画・拘束時間チェック | 4 / 20 (16 + 4) | 79 | 300 | UAT 2nd; **giờ lái 2024** |
| [#32](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/32) E-12 ルート公開・運行管理 | 2 / 8 (6 + 2) | 37 | 90 | UAT 2nd; **giờ lái 2024** |
| [#35](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/35) E-13 温度データ取込・評価 | 4 / 13 (9 + 4) | 59 | 164 | UAT 3rd |
| [#40](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/40) E-14 アラーム・逸脱管理 | 3 / 10 (7 + 3) | 45 | 106 | UAT 3rd |
| [#44](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/44) E-16 トレーサビリティ検索 | 2 / 6 (4 + 2) | 23 | 62 | UAT 3rd; test 300.000 dòng |
| [#47](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/47) E-17 回収管理 | 3 / 8 (5 + 3) | 34 | 80 | UAT 3rd |
| [#51](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/51) E-19 監査エビデンス・保持 | 1 / 2 (1 + 1) | 9 | 24 | UAT 3rd |
| [#53](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/53) E-20 マスター管理 | 2 / 8 (6 + 2) | 41 | 100 | UAT 1st |
| [#56](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/56) E-21 認証・権限・監査ログ | 4 / 12 (8 + 4) | 51 | 140 | UAT 1st; gồm T-167 (GAP-066) bổ sung |
| [#61](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/61) E-22 外部連携 | 2 / 4 (2 + 2) | 18 | 40 | UAT 3rd |
| [#64](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/64) E-23 データ移行 | 1 / 3 (2 + 1) | 15 | 36 | UAT 1st; dễ thiếu giờ (§4) |
| [#66](https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/66) E-24 共通基盤・非機能 | 2 / 5 (3 + 2) | 20 | 44 | UAT 1st |
| **Tổng** | **50 / 168 (117 + 51)** | **711** | **1.934** | dev 1.496h + test/QA 438h |

## 4. So với estimate LAB-1

**Nguồn LAB-1:** `LAB1/deliverables/…Effort Estimation 20261022_Option1（全機能）.xlsx`, sheet `01_Server`. Đây là công lập trình BE + FE theo từng chức năng F-xxx, đơn vị người-ngày, chưa cộng buffer 15%. Cột LAB-1 lấy đúng các F-xxx có story ở LAB-5, đổi ra giờ theo 1 người-ngày = 7h (quy ước của LAB-1).

**Cột LAB-5:** giờ task dev, không tính task QA (QA so riêng ở dòng cuối).

**Lý do chung cho mức chênh:**
- LAB-1 ước công **làm mới từ đầu**.
- LAB-5 chỉ ước **phần chênh lệch** giữa thiết kế to-be và prototype LAB-2 đang chạy (PREMISE A-1).

Vì vậy LAB-5 thấp hơn ở mọi epic. Chỗ giảm ít nghĩa là prototype phải làm lại nhiều.

| Phần (epic ← chức năng LAB-1) | LAB-1 | LAB-5 | Chênh | Vì sao |
|---|---|---|---|---|
| E-02 Kiểm hàng nhập (F-004..010) | 337h | 178h | −159h (−47%) | 19 DLT + 6 GAP: parser GS1-128, mã bò 10 số, ngưỡng nhiệt có version |
| E-03 Lô & tồn (F-011, 012) | 133h | 52h | −81h (−61%) | SCR-025 đã có ở prototype; 8 DLT, chính là chặn giải phóng lô đang thuộc case thu hồi (GAP-071) |
| E-06 Hạn dùng & phân bổ (F-021, 022, 024, 025) | 206h | 76h | −130h (−63%) | SCR-033/034 đã có ở prototype; 11 DLT: đổi nguồn mốc 日付逆転 sang lịch sử giao đã nhận (ADR-0006), lưu bằng chứng phán định |
| E-08 Phân bổ & lấy hàng (F-029, 030) | 197h | 106h | −91h (−46%) | Kiểm ràng buộc cứng trong transaction (T-029) và xử lý tranh chấp (ADR-0007) gần như làm mới |
| E-09 Xác nhận xuất (F-033) | 35h | 12h | −23h (−66%) | SCR-033 đã có xác nhận xuất; chỉ thêm kiểm lại 消費期限, cách ly, trạng thái truy xuất sau khi khoá lô (1 DLT + GAP-021) |
| E-10 POD (F-034..037) | 321h | 148h | −173h (−54%) | Hàng đợi offline mã hoá, idempotent (ADR-0012) là phần nặng nhất |
| E-11 Lập tuyến & giờ ràng buộc (F-040..043) | 304h | 242h | −62h (−20%) | **Giảm ít nhất**: engine giờ lái của prototype phải làm lại theo DRV-RULE có version, tính từng đoạn (23 DLT). Đây là phần chịu ràng buộc 2024 |
| E-12 Công bố tuyến (F-044, 047) | 112h | 70h | −42h (−38%) | Công bố có version và chặn khi vi phạm (giờ lái 2024) |
| E-13 Dữ liệu nhiệt (F-048..051) | 203h | 128h | −75h (−37%) | Chính sách dải nhiệt có version và nhập CSV idempotent (ADR-0005, 0009) là mới |
| E-14 Cảnh báo & sai lệch (F-052..054) | 186h | 82h | −104h (−56%) | SCR-072/074 đã có ở prototype; 18 DLT, chủ yếu đổi mức cảnh báo (D-04) và mốc SLA sang giờ ISO 8601 (GAP-043) |
| E-16 Truy xuất (F-059, 060) | 169h | 42h | −127h (−75%) | SCR-080 đã có ở prototype; thêm index và test 300.000 dòng xuất (T-090) |
| E-17 Thu hồi (F-062..064) | 172h | 62h | −110h (−64%) | SCR-082 đã có ở prototype; thêm phạm vi thu hồi theo dòng, cách ly tồn trong cùng transaction mở case, người nhận thông báo theo bảng liên hệ (8 DLT + GAP-007, 050, 070) |
| E-19 Bằng chứng kiểm toán (F-071) | 70h | 18h | −52h (−74%) | Chỉ phần xuất; lưu giữ / legal hold (GAP-061) hoãn |
| E-20 Master (F-075, 079) | 119h | 78h | −41h (−34%) | Hợp đồng có version, duyệt master chung (GAP-004, 005) |
| E-21 Xác thực & quyền (F-081..084) | 154h | 108h | −46h (−30%) | SSO/MFA, phiên máy dùng chung, RLS theo vai trò (ADR-0010, 0011) là mới |
| E-22 Liên kết ngoài (F-087, 088) | 42h | 32h | −10h (−24%) | Bản đồ và mail thật thay cho bản giả lập |
| E-23 Migration (F-091) | 122h | 28h | −94h (−77%) | Chỉ có luật phán định và staging. Profiling, đối chiếu, ảnh POD cũ chưa có thiết kế (task-breakdown §4). **Nhiều khả năng thiếu giờ** |
| E-24 Nền tảng (F-096, 097) | 56h | 34h | −22h (−39%) | Mã hoá / secret, UI tiếng Nhật và JST |
| **Cộng 50 chức năng** | **2.936,5h** (419,5 người-ngày) | **1.496h** | **−1.440,5h (−49%)** | Các dòng trên làm tròn tới giờ nên cộng lại lệch 1,5h |
| 48 chức năng chưa có story (task-breakdown §2) | 315,5 người-ngày = 2.209h | 0h | — | Chưa break: không có thiết kế to-be (PREMISE A-1) |
| QA | 2.194,5h (vai trò QA, toàn dự án, sheet WBS) | 438h | — | Không cùng phạm vi: LAB-1 gồm cả thiết kế test, test tổng thể và test phi chức năng; LAB-5 chỉ là test tích hợp theo story của 18 epic. Tỉ lệ QA/dev vẫn giữ khoảng 28% (PREMISE A-6) |
