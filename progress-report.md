# 進捗報告 — Sprint 1 / Báo cáo tiến độ — Sprint 1

食品コールドチェーン業務支援システム（YCL）開発 / Phát triển hệ thống YCL

| 項目 / Mục | 内容 / Nội dung |
|---|---|
| Iteration（Project 上の名称） | **Sprint 1** — [GitHub Project #1](https://github.com/users/tinhd-3628/projects/1), view 「Sprint Detail view」 |
| 期間 / Kỳ | 2026-11-02（月）〜 2026-11-13（金）稼働 10 日。Iteration 枠は 11-02 〜 11-15 / 10 ngày làm việc |
| 報告日 / Ngày báo cáo | 2026-11-13（Sprint 1 最終日） |
| 対象マイルストーン / Mốc | UAT 1st（2026-12-01）— Sprint 1・2 で構築。UAT 1st〜3rd は**演習用の仮想日程**で、ご提案時の UAT 時期・本稼働日（2027-06-01）は変更していません / Các mốc UAT là lịch giả lập cho bài tập; lịch UAT trong đề xuất và ngày go-live 2027-06-01 không đổi |
| データ / Dữ liệu | **演習用の仮想データ**（[`backlog/sprint-1-simulation.yaml`](backlog/sprint-1-simulation.yaml)）。GitHub 上のクローズ日時はスクリプト実行日（2026-10-29）であり、本報告の日付は YAML に従う / Dữ liệu giả lập; ngày đóng issue trên GitHub là ngày chạy script, báo cáo dùng ngày trong YAML |

**要約 / Tóm tắt**
- 計画 26 タスク（118 SWP・310h）のうち 19 タスク・77 SWP（65%）が完了しました。6 タスクが仕掛り、1 タスクが未着手で、計 41 SWP を Sprint 2 へ持ち越します。
- 遅延の主因は 2 つです。
  - 引当ハード制約チェック（T-029）の工数超過。
  - 契約版（T-100）と画面（T-103）の依存関係がバックログに未登録だったこと。
- 持ち越し分を加えると、Sprint 2 は BE・QA が上限 70h を超えます。UAT 1st を守るため、11/16 の Sprint 2 計画で調整します。

*Vi:*
- Xong 19/26 task, 77/118 SWP (65%). Còn 6 task đang làm và 1 task chưa bắt đầu, tổng 41 SWP chuyển sang Sprint 2.
- Hai nguyên nhân chính:
  - T-029 (kiểm ràng buộc cứng khi phân bổ) vượt giờ.
  - Phụ thuộc T-103 → T-100 không có trong backlog.
- Cộng phần chuyển sang thì Sprint 2 của BE và QA vượt 70h. Sẽ điều chỉnh ở buổi lập kế hoạch Sprint 2 ngày 16/11 để giữ mốc UAT 1st.

## 1. ステータス / Trạng thái

| ステータス / Trạng thái | 件数 / Số issue | 合計 SWP / Tổng SWP | 備考 / Ghi chú |
|---|---|---|---|
| Done | 19 | 77 | 計画 202h に対し実績 207h（+2%）。QA 3 件は 18h → 19h / Kế hoạch 202h, thực tế 207h |
| In Progress | 6 | 37 | 計画 98h・消化 61h、残り約 55h を Sprint 2 へ持ち越し: T-029 #97, T-100 #168, T-033 #101, T-034 #102, T-147 #215, T-157 #225 / Còn khoảng 55h chuyển sang Sprint 2 |
| Todo | 1 | 4 | T-103 #171（10h）: T-100 完了待ち / chờ T-100 xong |
| **合計 / Tổng** | **26** | **118** | 計画 310h、消化 268h（86%）/ Kế hoạch 310h, đã dùng 268h |

担当別の消化（計画 → 実績）/ Theo người phụ trách (kế hoạch → đã dùng):

| PIC | 計画 / KH | 消化 / Đã dùng | 状況 / Tình trạng |
|---|---|---|---|
| BE-1 | 64h | 53h | T-100 仕掛り / T-100 đang làm |
| BE-2 | 66h | 67h | T-029 超過（24h → 30h）で T-033 が仕掛り / T-029 vượt giờ, T-033 dở dang |
| BE-3 | 62h | 62h | 予定どおり完了 / Xong đúng kế hoạch |
| FE-1 | 22h | 12h | T-103 未着手。稼働余力あり / T-103 chưa làm, còn trống năng lực |
| FE-2 | 32h | 38h | T-080 超過（20h → 24h）/ T-080 vượt giờ |
| QA-1 | 64h | 36h | T-034・T-147・T-157 が開発完了待ち / ba task QA chờ dev xong |

## 2. バーンダウン / Burndown

残 SWP（日終わり時点）。「理想」は直線、「計画」は各タスクの予定完了日、「実績」は実際の完了日で計算しています。
*Vi: SWP còn lại cuối mỗi ngày. "Lý tưởng" là đường thẳng; "Kế hoạch" theo ngày dự kiến xong của từng task; "Thực tế" theo ngày xong thật.*

| 日 / Ngày | 日付 | 理想 / Lý tưởng | 計画 / Kế hoạch | 実績 / Thực tế | 差 / Lệch so với kế hoạch |
|---|---|---|---|---|---|
| D0 | 開始 / bắt đầu | 118 | 118 | 118 | 0 |
| D1 | 11-02 | 106 | 118 | 118 | 0 |
| D2 | 11-03 | 94 | 101 | 101 | 0 |
| D3 | 11-04 | 83 | 85 | 98 | +13 |
| D4 | 11-05 | 71 | 76 | 89 | +13 |
| D5 | 11-06 | 59 | 59 | 81 | +22 |
| D6 | 11-09 | 47 | 52 | 71 | +19 |
| D7 | 11-10 | 35 | 43 | 62 | +19 |
| D8 | 11-11 | 24 | 32 | 51 | +19 |
| D9 | 11-12 | 12 | 27 | 51 | +24 |
| D10 | 11-13 | 0 | 0 | **41** | +41 |

```
残SWP 118 ┤■■■■■■■■■■■■■■■■■■■■■■■■  D0
           ┤■■■■■■■■■■■■■■■■■■■■      D3   実績 98 / 計画 85
           ┤■■■■■■■■■■■■■■■■          D5   実績 81 / 計画 59
           ┤■■■■■■■■■■■■■             D7   実績 62 / 計画 43
           ┤■■■■■■■■■■                D9   実績 51 / 計画 27
        41 ┤■■■■■■■■                  D10  実績 41 / 計画 0
```

**計画との乖離 / Chỗ lệch kế hoạch**
- **D3〜（+13）:** T-029（10 SWP）は D3 完了予定でした。④までは完了しましたが、⑤日付逆転（同じ顧客×SKU の直近の受領済み配送との比較）で、「同日複数便」と「受領拒否・取消の配送行の除外」の扱いが見積に含まれていませんでした。これらのケースは ADR-0006 と SCR-034 仕様に記載済みで、見積側の漏れです。
  *Vi: T-029 dự kiến xong D3. Phần ⑤ 日付逆転 (so với lần giao đã nhận gần nhất của đúng cặp khách × SKU) có hai ca estimate chưa tính: nhiều chuyến cùng ngày, và loại bỏ dòng giao bị từ chối nhận hoặc bị huỷ. ADR-0006 và spec SCR-034 đã ghi các ca này.*
- **D5〜D7（+19〜22）:** BE-2 が T-029 に留まったため、T-031・T-032 の着手が 2 日遅れました。FE-2 の T-080（SCR-079 画面）も 1 日超過しています。
  *Vi: BE-2 kẹt ở T-029 nên T-031, T-032 bắt đầu muộn 2 ngày; T-080 của FE-2 trễ 1 ngày.*
- **D9〜D10（+24〜41）:**
  - T-033（30 万出荷行での EXPLAIN 計測）は、テストデータ生成に想定以上の時間がかかりました。
  - T-100 は契約データの版移行に時間がかかりました。
  - その結果、後続の T-034・T-157・T-103 が着手できず、最終日に 41 SWP が残りました。

  *Vi: T-033 tốn thời gian sinh dữ liệu 300.000 dòng; T-100 chuyển dữ liệu hợp đồng sang dạng có phiên bản lâu hơn dự kiến. Các task sau nó (T-034, T-157, T-103) không bắt đầu được nên còn 41 SWP.*
- 完了したタスクは計画比 +2% と大きなずれはありません。遅れの主因は仕掛りタスクと、その待ち時間です。
  *Vi: Task đã xong chỉ lệch +2% giờ; trễ chủ yếu do task dở dang và thời gian chờ.*

## 3. 遅延リスク / Rủi ro trễ tiến độ

| リスク / Rủi ro | Issue | 影響するマイルストーン / Mốc bị ảnh hưởng | 対応 / Hành động | 担当・期限 / Ai làm, khi nào |
|---|---|---|---|---|
| 引当ハード制約チェックが未完了（30h/24h、残り約 10h）。境界値テストも止まっている<br>*T-029 chưa xong, vượt giờ; test biên đang chờ* | #97 T-029, #102 T-034 | UAT 1st 2026-12-01（E-08-S01） | Sprint 2 の初日から T-029 を最優先で完了させ、直後に T-034 を実行する。同種の DB 制約タスク（cal-001 グループ）の見積を見直す<br>*Làm xong T-029 ngay đầu Sprint 2, chạy T-034 liền sau; xem lại estimate các task DB cùng nhóm* | BE-2: 11-17 まで。QA-1: 11-19 まで。PL（見積見直し）: 11-16 |
| 契約版移行（T-100）が仕掛り。画面 T-103 との依存がバックログに未登録で、同じ Sprint に置かれていた<br>*Phụ thuộc T-103 → T-100 không có trong backlog* | #168 T-100, #171 T-103, #225 T-157 | UAT 1st（E-20-S02） | 依存関係 T-103 → T-100 を追加する。T-100 → T-103 → T-157 の順に実施。AGR-008 / AGR-014 は D-02 どおり未設定のまま移す（既定値を入れない）<br>*Thêm phụ thuộc, làm theo thứ tự; AGR-008/014 vẫn để 未設定* | PL（依存追加）: 11-16。BE-1: 11-17。FE-1: 11-19。QA-2: 11-20 |
| 30 万出荷行テストデータの生成が遅い。性能確認（NFR-PERF）が後ろ倒しになる<br>*Sinh dữ liệu 300.000 dòng chậm* | #101 T-033（後続: #158 T-090） | UAT 1st（引当性能）、UAT 3rd（トレース 60 秒） | データ生成スクリプトを T-090 でも再利用できる形で完成させる。件数は 30 万行のまま減らさない<br>*Làm script sinh dữ liệu dùng lại được cho T-090; giữ đủ 300.000 dòng, không giảm* | BE-2: 11-16（Sprint 2 初日） |
| 持ち越し約 65h（Todo 含む）で Sprint 2 が上限超過。BE-1 70h → 約 80h、BE-2 74h → 約 90h、BE-3 78h、QA-1 70h → 約 99h（上限 70h。追加タスク #235・#236 を含む）<br>*Sprint 2 quá tải sau khi cộng phần chuyển sang* | Sprint 2 全体（計画時点の超過: #186 T-118、#188 T-120） | UAT 1st | QA の持ち越し（T-147・T-157）を QA-2 に移す。BE の超過分は、UAT 1st の範囲内で後ろ倒しできるタスクを選び、必要なら顧客と UAT 1st の範囲を調整する。または FE-2 を一時的に支援に回す<br>*Chuyển phần QA sang QA-2; BE thì chọn task lùi được hoặc thỏa thuận lại phạm vi UAT 1st với khách* | PL: Sprint 2 計画（11-16）。顧客合意が必要な場合は 11-18 の定例で |
| 80 ユーザー同時の負荷テスト（NFR-PERF-01）が当初のバックログに無かった<br>*Ban đầu backlog thiếu test tải 80 user đồng thời* | #235 T-168（Sprint 2 に追加） | UAT 1st（性能要件の確認） | タスク追加済み。T-033 のテストデータ生成スクリプトを再利用し、80 ユーザーのまま実施する（42 名に縮小しない）<br>*Đã thêm task; dùng lại script dữ liệu của T-033, giữ đúng 80 user* | QA-1 / QA-2: Sprint 2 中（11-27 まで） |
| 運転時間規制の未回答事項（Q-new-08〜12）が残っている<br>*Khách chưa trả lời các câu về giờ lái* | E-11 #27、E-12 #32 | UAT 2nd 2027-01-05（Sprint 3 から着手） | Sprint 3 開始前に回答を依頼する。値が変わっても版の追加で対応できる設計（ADR-0008）のため、未回答のまま着手は可能<br>*Xin trả lời trước Sprint 3; thiết kế dùng version nên vẫn bắt đầu được* | PL / BrSE: 11-27 まで |
