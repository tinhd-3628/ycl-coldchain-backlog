"""Bilingual issue titles and bodies for the LAB-5 backlog: Japanese first, Vietnamese below.

Follows the pm-create-tasks template. Vietnamese acceptance criteria are plain bullets (not
checkboxes) so GitHub's task-list progress counts only the Japanese checklist.
"""

VI_HEADER = "\n---\n\n# Tiếng Việt\n\n"
SWP_JA = "- SWP: Project の SWP フィールド参照（tkm:sun-estimate で採点、PL レビュー済み）\n"
SWP_VI = "- SWP: xem trường SWP trên Project (chấm bằng tkm:sun-estimate, PL đã review)\n"
DRIVER_HOURS_JA = (
    "\n## 特有制約: トラックドライバーの労働時間規制（改善基準告示 2024年4月改正）\n"
    "この Epic は運転時間・拘束時間・休息期間の上限に直接影響されるため、他の Epic と分けて管理する。\n"
    "- 規制値の正本は ADR-0008（DRV-RULE 表）。RFP FR-SCH-02 の値を使い、緩和しない\n"
    "- 運転・休憩・待機・荷役を区間別に計算し、拘束時間を別に判定する（合計時間だけで判定しない）\n"
    "- 違反はルート公開を止めるハード制約。判定は DB トランザクション内で再計算する（ADR-0004）\n"
    "- 顧客未回答: Q-new-08〜12（回答で値が変わる場合は版の追加で対応）\n")
DRIVER_HOURS_VI = (
    "\n## Ràng buộc đặc thù: quy định giờ làm việc của tài xế xe tải (改善基準告示, sửa đổi 04/2024)\n"
    "Epic này chịu ảnh hưởng trực tiếp từ giới hạn giờ lái, thời gian ràng buộc (拘束時間) và thời gian nghỉ, "
    "nên được quản lý tách riêng khỏi các epic khác.\n"
    "- Giá trị quy định lấy theo ADR-0008 (bảng DRV-RULE), dùng đúng giá trị RFP FR-SCH-02, không nới lỏng\n"
    "- Tính riêng từng đoạn lái / nghỉ / chờ / bốc dỡ và phán định thời gian ràng buộc riêng (không chỉ cộng tổng giờ)\n"
    "- Vi phạm là ràng buộc cứng chặn công bố tuyến; phán định được tính lại trong transaction DB (ADR-0004)\n"
    "- Khách chưa trả lời: Q-new-08〜12 (nếu câu trả lời làm đổi giá trị thì thêm phiên bản mới)\n")


def bullets(items):
    return "\n".join(f"- {i}" for i in items)


def issue_title(kind, item_id, ja, vi):
    return f"[{kind}][{item_id}] {ja} / {vi}"


def screens(s):
    joined = ", ".join(s["screens"])
    return joined or "画面なし（共通基盤）", joined or "Không có màn hình (nền tảng chung)"


def epic_body(e):
    stories_ja = bullets(f"{s['id']} {s['title']}" for s in e["stories"])
    stories_vi = bullets(f"{s['id']} {s['title_vi']}" for s in e["stories"])
    ja = (f"## 概要\n機能グループ {e['id']}（WBS LAB-1）。LAB-4 詳細設計の to-be と prototype（as-built）の差分を実装する。\n\n"
          f"## Story\n{stories_ja}\n\n## 見積\n- 合計見積時間: {e['hours']}h（子タスクの合計）\n{SWP_JA}")
    vi = (f"## Tổng quan\nNhóm chức năng {e['id']} (WBS LAB-1). Hiện thực phần chênh lệch giữa thiết kế to-be "
          f"của LAB-4 và prototype (as-built).\n\n"
          f"## Story\n{stories_vi}\n\n## Ước lượng\n- Tổng giờ: {e['hours']}h (cộng từ các task con)\n{SWP_VI}")
    if e.get("constraint"):
        ja, vi = ja + DRIVER_HOURS_JA, vi + DRIVER_HOURS_VI
    return ja + VI_HEADER + vi


def story_body(s, epic_no):
    scr_ja, scr_vi = screens(s)
    tasks_ja = bullets(f"{t['tid']} {t['title']}（{t['hours']}h）" for t in s["tasks"])
    tasks_vi = bullets(f"{t['tid']} {t['title_vi']} ({t['hours']}h)" for t in s["tasks"])
    ja = (f"## 概要\nStory {s['id']} {s['title']}（親 Epic: #{epic_no}）\n\n## 対象画面\n{scr_ja}\n\n"
          f"## タスク\n{tasks_ja}\n\n## 受入条件（Acceptance Criteria）\n- [ ] すべてのサブ issue がクローズされている\n"
          f"- [ ] 対象画面の Story 受入条件（LAB-1 story §9）をテストで確認済み\n\n"
          f"## 見積\n- 合計見積時間: {s['hours']}h\n{SWP_JA}")
    vi = (f"## Tổng quan\nStory {s['id']} {s['title_vi']} (Epic cha: #{epic_no})\n\n## Màn hình liên quan\n{scr_vi}\n\n"
          f"## Task\n{tasks_vi}\n\n## Điều kiện nghiệm thu (bản dịch — tick ở phần tiếng Nhật)\n"
          f"- Tất cả sub-issue đã đóng\n- Đã xác nhận bằng test điều kiện nghiệm thu story của màn hình liên quan (LAB-1 story §9)\n\n"
          f"## Ước lượng\n- Tổng giờ: {s['hours']}h\n{SWP_VI}")
    return ja + VI_HEADER + vi


def task_body(s, t, story_no, numbers):
    dep_items = [f"{d} #{numbers[d]}" for d in t.get("depends", [])]
    scr_ja, scr_vi = screens(s)
    refs = bullets(t["refs"])
    spec = bullets([f"LAB-4 specs `design/screens/{x}_*/spec.md` §Delta vs As-built" for x in s["screens"]]
                   + ["LAB-4 specs `database/prototype-vs-design-gap.md` / `docs/decisions/ADR-*.md`"])
    checks = "\n".join(f"- [ ] {a}" for a in t["ac"])
    qa = t["layer"] == "test"  # QA tasks: integration test phase, no unit-test criterion
    phase_ja, phase_vi = ("結合テスト（QA）", "kiểm thử tích hợp (QA)") if qa else \
        ("詳細設計・製造・単体テスト", "thiết kế chi tiết · lập trình · unit test")
    unit_ja, unit_vi = ("", "") if qa else ("- [ ] 単体テストを追加し、レビュー済み\n", "- Đã thêm unit test và được review\n")
    basis_ja, basis_vi = ("Story 開発工数の 28%（QA タスク生成ルール）", "28% giờ dev của story (quy tắc sinh task QA)") \
        if t.get("generated_qa") else ("タスクから直接見積", "ước lượng trực tiếp theo task")
    ja = (f"## 概要\n{t['title']}\n\n## 関連WBS\n- WBS ID: {s['id']} {s['title']}（親 Story: #{story_no}）\n"
          f"- フェーズ: {phase_ja}\n- 対象画面: {scr_ja}\n- レイヤー: {t['layer']}\n\n"
          f"## スコープ（LAB-4 差分項目）\n{refs}\n\n"
          f"## 受入条件（Acceptance Criteria）\n{checks}\n{unit_ja}\n"
          f"## 依存\n{bullets(dep_items) or '- なし'}\n\n## 参照\n{spec}\n\n"
          f"## 見積\n- 見積時間: {t['hours']}h（{basis_ja}）\n{SWP_JA}")
    vi = (f"## Tổng quan\n{t['title_vi']}\n\n## WBS liên quan\n- WBS ID: {s['id']} {s['title_vi']} (Story cha: #{story_no})\n"
          f"- Giai đoạn: {phase_vi}\n- Màn hình: {scr_vi}\n- Tầng: {t['layer']}\n\n"
          f"## Phạm vi (hạng mục chênh lệch LAB-4)\n{refs}\n\n"
          f"## Điều kiện nghiệm thu (bản dịch — tick ở phần tiếng Nhật)\n{bullets(t['ac_vi'])}\n{unit_vi}\n"
          f"## Phụ thuộc\n{bullets(dep_items) or '- Không có'}\n\n## Tham chiếu\n{spec}\n\n"
          f"## Ước lượng\n- Giờ ước lượng: {t['hours']}h ({basis_vi})\n{SWP_VI}")
    return ja + VI_HEADER + vi
