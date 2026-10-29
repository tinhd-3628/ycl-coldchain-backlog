# Task breakdown — từ LAB-4 tới backlog trên GitHub Project

Nguồn: `LAB4/specs/` (18 spec màn to-be, ERD to-be, 13 ADR, file gap). Nguồn sự thật của backlog là [`backlog/backlog-breakdown.yaml`](backlog/backlog-breakdown.yaml); script [`backlog/sync-github-backlog-issues.py`](backlog/sync-github-backlog-issues.py) tạo và cập nhật issue từ file này. Số `#n` = `https://github.com/tinhd-3628/ycl-coldchain-backlog/issues/n`.

Kết quả: **18 epic · 50 story · 168 task** (117 task dev + 51 task test/QA) = 236 issue, 1.934h, 711 SWP. T-167, T-168 được bổ sung sau Sprint 1 (§4).

## 1. Nguyên tắc chia task

**Ba tầng, khớp WBS LAB-1**

| Tầng trên Project | Ứng với | Mã | Nhãn |
|---|---|---|---|
| Epic (issue cha) | Nhóm chức năng LAB-1 (FG-xx) | `E-xx` | `type:epic` |
| Issue (sub-issue của epic) | 1 chức năng LAB-1 (F-xxx) = 1 story | `E-xx-Syy` (giữ số của WBS LAB-1, nên có chỗ nhảy số) | `type:story` |
| Sub-issue (sub-issue của story) | 1 task làm được trong 1–3 ngày | `T-001`..`T-168` | `type:task`, `layer:*`, `priority:P0` nếu có |

Quan hệ cha–con dùng tính năng sub-issue của GitHub. Cột "Sub-issues progress" trên view *Project Overall* cho thấy epic đã xong bao nhiêu.

**Độ hạt: chia tới đâu thì dừng**
- Dừng khi task thỏa cả 4 điều sau:
  - **4–24h** (tối đa 3 ngày; hiện nhỏ nhất 4h, lớn nhất 24h);
  - **một tầng** (`db` / `api` / `ui` / `batch` / `test`);
  - **một người phụ trách**;
  - có **điều kiện nghiệm thu kiểm được**.
- Tách thêm một sub-issue khi gặp một trong ba trường hợp:
  - vượt 24h (vd. kiểm giờ lái tách thành T-050 hàm kiểm khi công bố / T-051 tổng hợp theo ngày / T-052 cửa sổ theo kỳ / T-054 tách loại đoạn);
  - chạm hai tầng (DB và màn hình tách riêng);
  - cần người khác làm (task QA).
- Mỗi task trỏ về dòng spec nguồn trong trường `refs` (DLT, GAP, ADR, D-xx, Q-new). Task không trỏ được về spec nào thì không tạo.
- Task QA: story nào chưa có task test đặc thù (test biên, test quyền, test tải) thì có đúng một task QA. Task được sinh tự động bởi [`backlog/backlog_qa_tasks.py`](backlog/backlog_qa_tasks.py) cho story chưa có task test.

**Định nghĩa xong**

| Tầng | Xong khi |
|---|---|
| Task dev | Mọi ô điều kiện nghiệm thu (tiếng Nhật) đã tick; có unit test và đã review; PR merge; issue đóng "completed"; Status = Done |
| Task QA | Có test case theo từng điều kiện nghiệm thu của story và đã review; đã chạy hết, ghi bằng chứng; lỗi tìm được đã ghi và test lại |
| Story | Mọi sub-issue đóng; điều kiện nghiệm thu story (LAB-1 story §9) đã kiểm bằng test |
| Epic | Mọi story đóng; epic khép ở mốc UAT của story cuối cùng |

**Cách dùng trên Project** ([Project #1](https://github.com/users/tinhd-3628/projects/1))
- **Trường:**
  - `Status`;
  - `Iteration` (Sprint 1–6, chỉ gán cho task);
  - `PIC` (người phụ trách giả định: epic = PL; story và task = BE-1/2/3, FE-1/2, QA-1/2);
  - `SWP` (point đã review; task chấm trực tiếp, story và epic là tổng của con);
  - `Estimate (h)`;
  - `Công đoạn`, `Priority`, `Start Date`, `Due Date`, `Spent time (h)`, `Progress (%)`.
- **Hai view:**
  - *Project Overall*: epic, nhóm theo Milestone UAT;
  - *Sprint Detail view*: task chưa Done, nhóm theo Công đoạn, sắp theo Priority.
- **Milestone:** UAT 1st / 2nd / 3rd (giả lập).
- Story và epic không có Iteration vì chúng trải qua nhiều sprint.

## 2. Spec → issue

**18 spec màn to-be và phần nền tảng.** Ô trong ngoặc là sub-issue của story đó. Mọi dòng `DLT` của 18 spec đều đã có task: đối chiếu tự động 167 dòng DLT trong `refs`, không sót dòng nào.

| Spec LAB-4 | Epic | Issue (story) và sub-issue | Phần spec chưa thành issue và vì sao |
|---|---|---|---|
| SCR-014 Kiểm hàng nhập (`design/screens/SCR-014_*`) | E-02 #1, E-21 #56 | #2 E-02-S01 (#69, #70, #189); #3 E-02-S02 (#71, #72, #190); #7 E-02-S06 (#81, #82, #194); #58 E-21-S02 (#175, #176, #228) | — |
| SCR-015 Phán định tiếp nhận | E-02 #1 | #5 E-02-S04 (#77, #78, #192); #6 E-02-S05 (#79, #80, #193); #8 E-02-S07 (#83, #195) | — |
| SCR-016 Dải nhiệt tạm thời | E-02 #1 | #4 E-02-S03 (#73–#76, #191) | — |
| SCR-025 Lô cách ly | E-03 #9 | #10 E-03-S01 (#84, #196); #11 E-03-S02 (#85–#88, #197) | — |
| SCR-033 Chạy phân bổ | E-06 #12, E-08 #17, E-09 #20 | #13 E-06-S02 (#89, #198); #18 E-08-S01 (#96–#102, #235); #19 E-08-S02 (#103, #104, #202); #21 E-09-S02 (#105, #203) | — |
| SCR-034 Chi tiết phán định phân bổ | E-06 #12, E-08 #17 | #14 E-06-S03 (#90, #91, #199); #15 E-06-S05 (#92, #93, #200); #16 E-06-S06 (#94, #95, #201); #18 E-08-S01 | — |
| SCR-051 Timeline tuyến & ràng buộc | E-11 #27, E-22 #61 | #28 E-11-S02 (#118–#124); #29 E-11-S03 (#125, #208); #62 E-22-S02 (#182, #230) | — |
| SCR-052 Công bố tuyến & phiên bản | E-12 #32 | #33 E-12-S01 (#135–#139, #211) | — |
| SCR-053 Thực tế giờ làm tài xế | E-11 #27, E-12 #32 | #31 E-11-S05 (#130–#134, #210); #34 E-12-S04 (#140, #212) | — |
| SCR-054 Phiên bản quy tắc tài xế | E-11 #27, E-20 #53 | #30 E-11-S04 (#126–#129, #209); #55 E-20-S06 (#172, #173, #226) | — |
| SCR-062 Giao hàng & POD | E-10 #22, E-06 #12, E-21 #56 | #23 E-10-S01 (#106–#108, #204); #24 E-10-S02 (#109–#111, #205); #25 E-10-S03 (#112–#116, #206); #26 E-10-S04 (#117, #207); #16 E-06-S06; #58 E-21-S02 | — |
| SCR-070 Nhập CSV logger | E-13 #35 | #36 E-13-S01 (#141, #142, #213); #37 E-13-S02 (#143, #144, #214); #39 E-13-S04 (#149, #216) | — |
| SCR-072 Hàng đợi cảnh báo | E-14 #40, E-22 #61 | #41 E-14-S01 (#150, #151, #217); #42 E-14-S02 (#152, #218); #63 E-22-S03 (#183, #231) | — |
| SCR-074 Chi tiết case sai lệch | E-14 #40, E-13 #35 | #43 E-14-S03 (#153–#156, #219); #37 E-13-S02 | — |
| SCR-079 Phiên bản chính sách dải nhiệt | E-13 #35, E-20 #53 | #38 E-13-S03 (#145–#148, #215); #55 E-20-S06 | — |
| SCR-080 Tra cứu truy xuất | E-16 #44, E-19 #51 | #45 E-16-S01 (#157–#160); #46 E-16-S02 (#161, #220); #52 E-19-S01 (#167, #224) | — |
| SCR-082 Chi tiết case thu hồi | E-17 #47, E-19 #51, E-22 #61 | #48 E-17-S01 (#162–#164, #221); #49 E-17-S02 (#165, #222); #50 E-17-S03 (#166, #223); #52 E-19-S01; #63 E-22-S03 | — |
| SCR-101 Master hợp đồng khách | E-20 #53 | #54 E-20-S02 (#168–#171, #225); #55 E-20-S06 | — |
| Nền tảng: ADR-0003/0010/0011/0013, GAP-053..058, PREMISE §4.6 | E-21 #56, E-23 #64, E-24 #66 | #57 E-21-S01 (#174, #227); #59 E-21-S03 (#177–#180, #236); #60 E-21-S04 (#181, #229); #65 E-23-S02 (#184, #185, #232); #67 E-24-S03 (#186, #233); #68 E-24-S04 (#187, #188, #234) | — |

**File gap `database/prototype-vs-design-gap.md`.** 71 dòng GAP: 64 dòng đã có task (đủ 15/15 P0, 35/39 P1, 14/17 P2), tính cả GAP-066 bổ sung sau Sprint 1. Các dòng không có task từ đầu:

| Spec LAB-4 | Epic | Issue | Phần spec chưa thành issue và vì sao |
|---|---|---|---|
| GAP-016, GAP-017, GAP-061, GAP-063 (P1) | (E-05, E-03, E-19, E-22 khi có thiết kế) | — | Màn liên quan (SCR-026..029, 095, 013/032/108) ngoài 18 màn to-be, chưa có DLT và điều kiện nghiệm thu → hoãn ([PREMISE §1](PREMISE.md#1-spec-thêm--bỏ--sửa-so-với-lab-4) dòng 2) |
| GAP-018, GAP-064 (P2) | — | — | GAP-018 còn chờ PL chốt quy tắc put-away; GAP-064 thuộc báo cáo / KPI (FG-18) chưa có thiết kế to-be (PREMISE §1 dòng 3) |
| GAP-066 (P2) | E-21 #56 | #236 T-167 | Bị sót lúc break, bổ sung sau Sprint 1 (PREMISE §1 dòng 4; §4 bên dưới) |
| GAP-068 (P2) | — | — | Không cần việc: to-be giữ nguyên CHECK đang có |

**Chức năng LAB-1 Option 1 chưa có story.** 48/98 chức năng, tổng 315,5 người-ngày (công lập trình) ở LAB-1:

| Nhóm | Chức năng | Vì sao chưa thành issue |
|---|---|---|
| 6 nhóm không có epic: FG-01 nhập dự kiến, FG-04 vị trí, FG-05 kiểm kê, FG-07 đơn hàng, FG-15 HACCP, FG-18 báo cáo/KPI | 20 chức năng: F-001..003, 015..019, 026..028, 056..058, 065..070 (126,5 người-ngày) | Không có màn to-be trong LAB-4 (giả định A-1). GAP-049 (HACCP) chỉ có phần thiếu ghi nhận nhiệt (F-051) đi vào E-13-S04 #39. Phần kiểm vệ sinh và ra vào (F-056..058) chưa có issue |
| Trong 18 epic đã có | 28 chức năng: F-013, 014, 020, 023, 031, 032, 038, 039, 045, 046, 055, 061, 072, 073, 074, 076–078, 080, 085, 086, 089, 090, 092..095, 098 (189 người-ngày) | Màn của chúng không thuộc 18 màn to-be. LAB-4 chỉ có GAP (đã gắn task nếu thuộc màn to-be), không có DLT riêng. Ba chức năng F-090/092/093 (migration) xem §4 |

## 3. Hạng mục chịu ràng buộc đặc thù: giờ lái xe tải từ 2024

Áp dụng 改善基準告示 (Thông báo về tiêu chuẩn cải thiện điều kiện lao động của tài xế), bản sửa đổi 04/2024; giá trị lấy theo LAB-4 ADR-0008 (bảng DRV-RULE) và FR-SCH-02 của RFP, không nới.

Gom vào **2 epic riêng có nhãn `constraint:driver-hours-2024`**, tổng **28 task · 116 SWP · 390h**. Thân issue của mỗi epic có mục 「特有制約」 (ràng buộc đặc thù).

| Ràng buộc | Issue | Vì sao tách riêng |
|---|---|---|
| Ràng buộc cứng khi lập tuyến: thời gian ràng buộc (拘束時間), giờ lái, nghỉ, chờ, bốc dỡ tính **riêng từng đoạn**, không chỉ cộng tổng | Epic #27 E-11 → #28 E-11-S02 (#118 T-050 hàm kiểm tính lại trong DB khi công bố; #119 T-051 tổng hợp theo ngày; #120 T-052 cửa sổ 2 ngày / 2 tuần / tháng / năm; #121 T-053 thiếu dữ liệu ca trước thì chặn; #122 T-054 tách đoạn lái / nghỉ / chờ / bốc dỡ; #123 T-055 panel cảnh báo; #124 T-056 test biên toàn bộ DRV-RULE) | Mỗi đại lượng có giới hạn và cách tính khác nhau. Gộp thì task vượt 3 ngày và không viết được điều kiện nghiệm thu cho từng ngưỡng. Vi phạm phải chặn công bố và được tính lại trong transaction DB (ADR-0004) |
| Tự chèn điểm nghỉ | #29 E-11-S03 (#125, #208) | Logic riêng, phụ thuộc kết quả kiểm ràng buộc ở trên |
| Quy tắc có phiên bản (DRV-RULE) và màn SCR-054 | #30 E-11-S04 (#126–#129, #209) | Khách chưa trả lời Q-new-08..12; đổi giá trị bằng version mới, không sửa code. Tách để có thể nạp version mới mà không đụng engine |
| Tổng hợp giờ làm thực tế (SCR-053) | #31 E-11-S05 (#130–#134 gồm batch #131, test #210) | Dữ liệu từ sự kiện chuyến trên máy tài xế (D-12), tách đoạn lái/nghỉ/chờ; P0 |
| Công bố tuyến có phiên bản; chặn khi vi phạm | Epic #32 E-12 → #33 E-12-S01 (#135–#139, #211) | Cổng cuối: tuyến vi phạm không được công bố. Lịch sử phán định hiện trên SCR-052 |
| Ghi nhận sự kiện bất thường (tắc đường, chờ lâu) không đè kết quả tuân thủ | #34 E-12-S04 (#140, #212) | Tách sự kiện khách quan khỏi số liệu tuân thủ theo thiết kế SCR-053 |
| Liên quan gián tiếp, **không** gắn nhãn: ước thời gian chạy từ dịch vụ bản đồ | #182 T-114 (E-22-S02) | Là đầu vào giờ lái dự kiến, nhưng bản thân là việc tích hợp IF-MAP-01. Ghi lại để khi đổi quy định thì nhớ test lại |

Ảnh hưởng tới effort:
- E-11 có tỉ lệ 4,0h/SWP (task dev), cao nhất cùng với E-09; trung bình là 3,1.
- So với LAB-1, E-11 chỉ giảm 20% giờ dev, trong khi cả backlog giảm 49%. Lý do: engine ràng buộc của prototype phải làm lại gần hết (23 dòng DLT) (estimate.md §4).
- Task QA của 2 epic này là 78h.

## 4. Chỗ hở hoặc mâu thuẫn của spec LAB-4 phát hiện khi break

| Spec | Chỗ hở / mâu thuẫn | Xử lý |
|---|---|---|
| Toàn bộ LAB-4 | Không có dòng spec nào cho kiểm thử tích hợp; chỉ có Verification của ADR và NFR (4 task) | Giả định: [PREMISE §1](PREMISE.md#1-spec-thêm--bỏ--sửa-so-với-lab-4) dòng 1, PREMISE §2 A-6 |
| `database/prototype-vs-design-gap.md`: GAP-016, 017, 061, 063 | Ghi là "ứng viên task LAB-5" nhưng màn của chúng không có spec to-be trong LAB-4, nên thiếu dữ liệu để break | Để mở: cần thiết kế to-be các màn này trước (PREMISE §1 dòng 2) |
| GAP-018 | Cột To-be ghi "chốt với PL quy tắc gợi ý put-away", tức quyết định còn treo | Để mở: chờ PL chốt; màn SCR-022 cũng ngoài 18 màn (PREMISE §1 dòng 3) |
| GAP-066 | Không gắn màn nào nên lọt khỏi các story theo màn. Lỗi của cách break, không phải lỗi spec | Tạo issue #236 (T-167, E-21-S03), Sprint 2 (PREMISE §1 dòng 4) |
| LAB-4 PREMISE §4.5 (NFR-PERF-01, 80 user đồng thời) | LAB-4 ghi "kịch bản test tải ở staging là ứng viên task LAB-5" nhưng không gắn màn nào. Khi break, NFR chỉ được gắn vào task của màn (T-033 đo EXPLAIN 300.000 dòng), nên thiếu test tải toàn hệ thống | Tạo issue #235 (T-168, E-08-S01), Sprint 2, trước UAT 1st (PREMISE §1 dòng 5) |
| GAP-065 (migration) | Nhắc F-090..F-093 nhưng LAB-4 chỉ thiết kế bảng staging và luật phán định (PREMISE §4.6); màn SCR-110/111 giữ spec kit. Không có chi tiết cho profiling dữ liệu, báo cáo đối chiếu, chuyển ảnh POD cũ | Để mở: E-23 chỉ có E-23-S02 (28h dev, so với 122h của F-091 ở LAB-1). Dễ thiếu giờ, ghi ở rủi ro estimate |
| SCR-101: DLT-101-07 (câu chữ 確認状況 — trạng thái xác nhận) và DLT-101-02 (`contract_versions`) | Hai dòng DLT phụ thuộc nhau nhưng spec không ghi. Khi break cũng không đặt `depends`, nên T-103 (#171) và T-100 (#168) bị xếp cùng sprint. Lộ ra ở Sprint 1 | Để mở có kế hoạch: thêm phụ thuộc T-103 → T-100 khi lập Sprint 2 (progress-report §3) |
| ADR-0008 + Q-new-08..12 | Khách chưa trả lời cách tính cửa sổ trung bình và ngày khởi tính; giá trị có thể đổi | Giả định của LAB-4 (D-11, D-12) giữ nguyên; thiết kế dùng version nên đổi giá trị không phải sửa code (PREMISE §3 dòng giờ lái) |
