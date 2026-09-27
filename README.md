# FrontierComputerScience
前沿計算機科學

## 主線：可執行規格 → 可重現基線 → 對抗性驗證 → 系統/演算法進步
第一輪先做 **CS-001：repository-scale formal verification**，重現一個小型 Lean 軟體驗證基線與依賴閉包，不先追求「AI 自動寫完整 verified repo」。

| ID | 問題 | 優先 | 第一輪 |
|---|---|---|---|
| CS-001 | Repository-scale 軟體形式驗證 | A | 依賴閉包＋小 proof obligation |
| CS-002 | Verified code generation 的跨語言泛化 | A | 同一 specification 跨 Lean/Verus/Dafny |
| CS-003 | 軟體工程 agent 的真實泛化與防 reward hacking | A | 重驗 verified benchmark 小子集 |
| CS-004 | ML compiler optimization 的跨程式／硬體泛化 | B | LLVM baseline＋held-out corpus |
| CS-005 | Agentic distributed systems 的 epistemic fault tolerance | B | toy quorum model＋correlated errors |
| CS-006 | Long-context retrieval 的 reasoning-relevance 泛化 | B | BRIGHT 小子集＋簡單 retrieval baseline |
| CS-007 | Byzantine/heterogeneous federated learning 的可驗證魯棒性 | B | 小型合成 federation |
| CS-008 | Program-and-proof joint planning | A | sequential vs joint planning |
| CS-009 | Repository-level verified agent construction | B | 多模組小 repo end-to-end |
| CS-010 | Evaluator-grounded algorithm discovery | B | 可精確打分的小演算法任務 |

每輪先讀 AGENTS、STATUS、VALIDATION，再按治理 091d6a26a4af8522683711483f2b97afd90efa7f 的 RESEARCH_PROTOCOL 重新查問題是否已有同範圍解答。OPEN 只是初始篩查狀態。

## 開工
~~~bash
python3 ../FrontierLab-Governance/tools/frontier.py validate .
python3 ../FrontierLab-Governance/tools/frontier.py start . CS-001 --agent glm
# 真正完成四路檢索、讀原文、填 round.json
python3 ../FrontierLab-Governance/tools/frontier.py admit . runs/<round-id>/round.json
~~~

所有 agent 走 branch + PR；結果、驗證器與 benchmark 定義分開審。編譯成功不是 correctness，benchmark 高分不是一般能力，兩個模型同意不是獨立驗證。
