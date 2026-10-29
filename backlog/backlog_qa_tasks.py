"""Story-level QA tasks for the LAB-5 backlog (one per story that has no test task of its own).

Rule agreed with the PL on 2026-10-29: every story with BE/FE development gets one QA task that
writes, runs and re-checks its integration test cases. Hours = 28% of the story's development hours
(the QA / development ratio of the LAB-1 estimate: QA 15.61 MM vs BE 36.05 + FE 18.34 MM), rounded
to 2h with a 4h floor. QA tasks are numbered after the hand-written tasks so existing T-IDs never move.
"""
QA_SHARE = 0.28
QA_MIN_HOURS = 4
AC_JA = ["Story と各開発タスクの受入条件ごとにテストケースを作成し、レビュー済み",
         "全テストケースを実行し、合否とエビデンスを記録",
         "検出した不具合を起票し、修正後の再テストで確認"]
AC_VI = ["Viết test case theo từng điều kiện nghiệm thu của story và các task dev, đã review",
         "Chạy toàn bộ test case, ghi kết quả đạt/không đạt kèm bằng chứng",
         "Ghi nhận lỗi phát hiện được, test lại sau khi sửa"]


def qa_hours(dev_hours):
    return max(QA_MIN_HOURS, 2 * round(QA_SHARE * dev_hours / 2))


def add_story_qa_tasks(epics, next_seq):
    """Append a generated QA task to each story lacking a test task; return the next free sequence."""
    for e in epics:
        for s in e["stories"]:
            dev = [t for t in s["tasks"] if t["layer"] != "test"]
            if not dev or len(dev) < len(s["tasks"]):
                continue
            next_seq += 1
            s["tasks"].append({
                "tid": f"T-{next_seq:03d}", "layer": "test", "generated_qa": True,
                "title": f"{s['title']} の結合テスト（テストケース作成・実行・不具合確認）",
                "title_vi": f"Kiểm thử tích hợp: {s['title_vi']} (viết test case, chạy, xác nhận lỗi)",
                "refs": list(dict.fromkeys(r for t in dev for r in t["refs"])),
                "ac": AC_JA, "ac_vi": AC_VI, "hours": qa_hours(sum(t["hours"] for t in dev)),
                **({"priority": "P0"} if any(t.get("priority") == "P0" for t in dev) else {}),
            })
    return next_seq
