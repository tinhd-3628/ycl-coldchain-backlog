# AI-report — Dùng AI để break task, chấm SWP, quy giờ và báo cáo tiến độ

Công cụ: Claude Code (VS Code) với bộ skill Takumi (`tkm:*`); GitHub qua `gh` CLI (REST và GraphQL). Người dùng đóng vai PL: ra yêu cầu, chọn phương án ở mỗi điểm quyết định, review kết quả.

## 1. Skill đã dùng và cách viết prompt

| Việc | Skill / công cụ | Prompt (nguyên văn hoặc rút gọn) | AI làm gì |
|---|---|---|---|
| Tạo repo và Project | `tkm:manage-project` | "LAB5: tạo repo GitHub mới trên account tinhd-3628 (tương tự ycl-coldchain-prototype) để quản lý task, rồi tạo GitHub Project gắn với repo đó." | Tạo repo, Project #1, các trường SWP / Estimate (h) / Iteration. Bộ lọc tự động chặn tạo repo public, nên repo và Project đang để private (README) |
| Break task | `tkm:pm-create-tasks` | "Break detail design LAB-4 (thư mục LAB4/) thành epic → issue → sub-issue, mỗi issue có story point (SWP) và giờ ước lượng; tách riêng hạng mục chịu ràng buộc giới hạn giờ lái xe tải 2024. Sau đó tạo epic/issue lên repo … và Project (fields: Status, SWP, Estimate (h), Iteration)." Sau đó: "issue song ngữ JP / VI", "view giống framgia/projects/281", "cân tải BE" | Đọc 18 spec to-be, file gap, ADR. Viết `backlog/backlog-breakdown.yaml` (nguồn sự thật) và script đồng bộ. Skill gốc ghi vào `project/01_management/task-list.md`; repo này không có thư mục đó nên AI đổi sang YAML + script tạo issue và sub-issue |
| Chấm SWP | `tkm:sun-estimate` | "Chấm SWP cho backlog trên repo … issue #1–#188, Project … có trường number "SWP" đang trống. Cần: báo cáo HTML đặt trong repo, danh sách issue mẫu để PL review (Scope × Complexity → SWP), sau khi PL chốt thì ghi SWP lên Project. Không commit, không đổi visibility repo." | Đọc issue (chỉ đọc), chia 5 lô, chấm Scope và Complexity, chọn 5 issue mẫu, hỏi PL từng issue, lan điều chỉnh theo nhóm, xuất HTML. Lượt 2 chấm 46 task QA |
| Ghi SWP lên Project | Agent chính chạy script; không dùng sub-agent | (trong cùng yêu cầu chấm SWP) "sau khi PL chốt thì ghi SWP lên Project" | Skill chỉ đọc, không ghi. Agent chính:<br>1. Gom giá trị đã duyệt vào `backlog/backlog-swp-reviewed.json`.<br>2. Chạy `sync-github-backlog-issues.py` ghi trường SWP qua GraphQL `updateProjectV2ItemFieldValue`. Story và epic là tổng của con.<br>3. Đọc ngược toàn bộ item trên board để so với file: hiện 236 item, tổng EPIC = STORY = TASK = 711, 0 lệch |
| Quy giờ | Trong lúc break (`tkm:pm-create-tasks`); quy tắc QA do PL chọn | "check xem số lượng task của QA đã hợp lý chưa, thường có dev FE hoặc BE thì có 1 QA task" → PL chọn "1 task QA mỗi story", "~28% giờ dev của story", "thêm QA-2" | Giờ dev: AI ước trực tiếp từng task từ dòng DLT/GAP. Giờ QA: theo công thức trong `backlog_qa_tasks.py`. Không đổi SWP ra giờ (estimate.md §2) |
| Giả lập sprint, báo cáo tiến độ | Agent chính + script. `tkm:pm-report-project` không dùng được vì skill cần `project/01_management/` | "yêu cầu tiếp theo làm gì" → chọn "Giả lập Sprint 1"; "viết cả 6 file xong hãy cho agent khác review độc lập đã đáp ứng đủ yêu cầu để nộp LAB5 chưa" | Viết `sprint-1-simulation.yaml`; script ghi Status, giờ đã dùng, %, ngày và comment song ngữ lên board. Bảng trạng thái và burndown tính bằng script từ YAML, không gõ tay |
| Review độc lập 6 file | Sub-agent `general-purpose`, chỉ đọc | "Đọc lab5_overview.md và 6 file, chấm từng mục bắt buộc là đạt / thiếu / sai, kèm bằng chứng" | Kết quả ở §2 |

Cách viết prompt:
- Ở mỗi bước, prompt nêu đủ bốn thứ: đầu vào (thư mục, repo, số issue), đầu ra mong muốn (file nào, trường nào), ràng buộc đặc thù của đề (giờ lái 2024), và điều không được làm (không commit, không đổi visibility).
- Khi có nhiều cách làm, AI đưa 2–4 phương án kèm khuyến nghị; PL chọn bằng câu hỏi trắc nghiệm.

## 2. Review output của AI

**Con người review ở 5 điểm**
1. Cấu trúc board và view: PL so với Project mẫu framgia/projects/281.
2. Tải theo người: PL chọn cân tải trong nhóm BE-1/2/3 thay vì cố định theo miền.
3. SWP:
   - Lượt 1: PL duyệt 5 issue mẫu, mỗi issue hai câu hỏi (mức độ, rồi điểm cụ thể), rồi chọn có lan điều chỉnh cho cả nhóm hay không.
   - Lượt 2 (QA): PL xem 5 issue mẫu và chấp nhận cả 5.
4. Độ đủ của backlog: PL hỏi về số task QA.
5. Kết quả cuối: một agent độc lập review 6 file theo đề.

**AI tự kiểm bằng script** (không tin số do AI viết ra bằng lời):
- Đọc ngược board sau mỗi lần ghi.
- Đối chiếu 167/167 dòng DLT và 63/71 dòng GAP với `refs` của task.
- Trước khi thêm lựa chọn PIC QA-2, thử trên một field tạm để chắc giá trị cũ không mất.

**Vấn đề phát hiện trong output của AI và cách xử lý**

| Vấn đề | Ai phát hiện, lúc nào | Xử lý |
|---|---|---|
| Bản break đầu tiên **thiếu hẳn công đoạn QA**: chỉ 4 task test, 4,3% giờ dev | PL, khi xem board | Thêm quy tắc 1 task QA mỗi story, 28% giờ dev (+46 task, +358h). Chấm SWP lượt 2 (PREMISE §1) |
| Agent `sun-estimate-worker` của skill **không có tool** nên không đọc được file lô: cả 5 lô trả BLOCKED | AI, khi gom kết quả | Chạy lại bằng 5 agent `general-purpose` (sonnet), mỗi agent chỉ được đọc file hướng dẫn và file lô của mình, chỉ ghi file kết quả. Ghi chú sai khác này vào phần caveat của báo cáo HTML |
| Nguy cơ AI chấm SWP **neo theo giờ** có sẵn trong thân issue | AI, khi chuẩn bị dữ liệu | Bỏ mục 「見積」 (ước lượng) và phần tiếng Việt khỏi dữ liệu gửi agent chấm |
| AI chấm thấp các task khó: T-001 parser GS1-128 (3 → PL 8), T-029 ràng buộc cứng (8 → 10), T-023 (1 → 3) | PL, khi duyệt issue mẫu | Sửa theo PL, lan theo nhóm (estimate.md §1) |
| Lan điều chỉnh của #139 cho cả nhóm UI làm các màn lớn bị thấp: T-061, T-066 24h nhưng chỉ 3 SWP | AI, khi kiểm chéo giờ/SWP lúc viết estimate.md | Ghi thành rủi ro, đề xuất review lại 10 task (estimate.md §2). Bài học: trước khi chọn "áp cho cả nhóm", xem danh sách task bị ảnh hưởng |
| Kịch bản giả lập ghi T-100 "bị chặn vì chờ khách trả lời AGR-008". Điều này **trái với LAB-4 D-02** (AGR-008/014 để 未設定, không cần chờ) và rơi đúng bẫy "tự điền mặc định cho AGR-008/014" | AI, khi đối chiếu báo cáo với LAB-4 PREMISE | Viết lại lý do trễ, sửa tại chỗ 3 comment trên board (script giờ sửa comment cũ thay vì đăng thêm) |
| Thiếu phụ thuộc T-103 → T-100 khi break | Lộ ra trong Sprint 1 giả lập | Đưa vào rủi ro và hành động Sprint 2 (task-breakdown §4) |
| Sót GAP-066 (không gắn màn nào) | AI, khi đối chiếu GAP tự động | Ghi PREMISE §1; PL duyệt, tạo T-167 #236 (3 SWP) |
| Sót test tải 80 user đồng thời (NFR-PERF-01). Bản nháp README còn ghi là "có test 80 user" | AI, khi đối chiếu ghi chú README với điều kiện nghiệm thu thật của task | Sửa README, ghi PREMISE §1; PL duyệt, tạo T-168 #235 (6 SWP) trong E-08-S01 |
| Bản nháp các file md có **số sai do AI viết từ trí nhớ**: mô tả sai T-050..052, đếm 46 thay vì 48 chức năng, giờ BE-2 77 thay vì 67 | AI, khi chạy lại script kiểm từng con số | Sửa. Từ đó mọi bảng số đều sinh bằng script từ YAML và JSON |
| Script kiểm báo cáo HTML báo thiếu JSON nhúng (regex phụ thuộc thứ tự thuộc tính) | AI, sau khi render | Sửa regex rồi kiểm lại |

**Kết quả review độc lập.** Một sub-agent mới, không nhận kết luận của agent viết, đọc đề và 6 file, tính lại số từ YAML / JSON / workbook LAB-1 và đọc cả 234 item trên board.

- **Kết luận:** "đạt nội dung, cần sửa trước khi nộp".
- **Số liệu và board:** khớp hoàn toàn, gồm tổng 702 SWP và 1.910h ở thời điểm review, burndown, issue mẫu, bảng so LAB-1.
- **Đoạn chép RFP:** không thấy; agent so trùng chuỗi 30 ký tự với text RFP.
- **Bẫy nghiệp vụ:** không mắc.

Các lỗi agent bắt được:

| Lỗi review bắt | Xử lý |
|---|---|
| Báo cáo gửi khách lẫn chuyện nội bộ (FE-1 thiếu việc, quy tắc lan SWP) | Bỏ khỏi progress-report; vẫn giữ ở estimate.md §2 |
| Chưa nói rõ các mốc UAT là lịch giả lập | Thêm vào đầu progress-report |
| Ghi "取消済み出荷 có trong ADR-0006", nhưng ADR chỉ có dòng bị từ chối nhận. Mốc 日付逆転 ghi 「直近出荷」 thay vì 「直近の受領済み配送」 | Sửa báo cáo, ghi chú giả lập và comment #97 |
| Một số lý do chung chung (E-09, E-17); tổng LAB-1 cộng từ số đã làm tròn; con số 58h không rõ cách tính | Sửa estimate.md, PREMISE §3 |
| GAP-066 và test tải 80 user mới chỉ ghi, chưa thành issue; epic chưa có PIC; chưa có link LAB-4 | PL quyết: tạo 2 task (T-167, T-168), SWP chấm trực tiếp rồi PL duyệt (estimate.md §1 lượt 3); gán PIC = PL cho 18 epic; không đưa bộ LAB-4 vào repo vì đề không yêu cầu nộp lại spec |

Đây là đúng tình huống của câu neo P2-11: báo cáo do AI viết nhìn thì đủ, nhưng có chỗ nói quá nguồn (取消済み出荷) và lẫn thông tin không dành cho người nhận. Chỉ đọc lại bằng mắt thì khó thấy.

## 3. Điểm đặc biệt trong cách dùng AI

**Hiệu quả**
- **Một nguồn sự thật + đồng bộ idempotent.** YAML là nguồn sự thật.
  - Script chỉ đẩy phần thay đổi: so `content_sha` cho thân issue, `fields_written` cho trường. Nhờ vậy chạy lại nhiều lần (song ngữ, QA, SWP) mà không tạo trùng.
  - Giá trị người dùng sửa tay trên board (Status, chuyển sprint) không bị ghi đè.
- **Hai thước đo độc lập.** Giờ ước trước, SWP chấm sau và che giờ khỏi dữ liệu chấm. Nhờ vậy tỉ lệ giờ/SWP vạch ra được task lệch (estimate.md §2).
- **Quyết định của PL dạng trắc nghiệm.** AI đưa phương án + khuyến nghị, PL chọn. Duyệt SWP đi theo hai bước (mức độ → điểm) nên luôn ra một con số cụ thể, không lẫn ý kiến.
- **Kiểm bằng script thay vì đọc lại bằng mắt.** Phủ DLT/GAP, tổng SWP trên board, số liệu burndown. Các lỗi ở §2 phần lớn do script bắt, không phải do đọc lại.

**Chưa tốt, cần cải thiện khi làm thật**
- Lan điều chỉnh SWP: phải xem trước danh sách task bị ảnh hưởng rồi mới chọn. Ở đây chọn "áp cả nhóm" khi chưa nhìn danh sách.
- Quy tắc QA 28% là một con số phẳng. Làm thật nên chia theo mức rủi ro của story (offline, giờ lái, tiền) và hiệu chỉnh bằng giờ QA thực tế sau 1–2 sprint.
- Break theo màn hình làm sót việc không gắn màn (GAP-066) và phụ thuộc chéo giữa các dòng DLT (T-103 → T-100). Nên thêm bước đối chiếu tự động "mọi GAP có task / mọi phụ thuộc giữa bảng và màn có `depends`" ngay khi break.
- Chấm SWP bằng 5 agent tốn nhiều token. Agent worker của skill không chạy được nên phải thay thế. Với backlog vài chục task, chấm trực tiếp ở agent chính là đủ.
- AI viết văn bản dễ "tự tin sai số". Mọi con số trong tài liệu gửi đi nên sinh từ dữ liệu, không để AI gõ lại.
- Dữ liệu giả lập: ngày đóng issue là ngày chạy script. Làm thật thì không gặp vấn đề này, nhưng báo cáo phải ghi rõ (progress-report đầu file).

**Chưa có ý tưởng tốt**
- Ước giờ cho phần chưa có thiết kế (48 chức năng ngoài 18 màn): AI chỉ có thể suy từ LAB-1. Chưa có cách tách bạch "ước lại" với "chép LAB-1".

`skills/`: không có. Bài này chỉ dùng skill Takumi sẵn có, không viết hay sửa skill.
