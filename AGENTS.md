# FrontierComputerScience agent 入口

先讀 README、STATUS、VALIDATION 與治理 https://github.com/lijiabao1998/FrontierLab-Governance/tree/9c3ae2dbaa1c814f3ef451c041dedfe3b77d926f 。

所有 agent 用 <agent>/CS-xxx-<topic> 分支；不直接改 main、不自合。每輪必須 start → 本輪 fresh search → 凍結 acceptance/evaluator → admit → baseline → exploration → verifier/skeptic → PR。

CS 特別規則：
- correctness、performance、generality 分開；只改善 benchmark 不能直接宣稱一般進步。
- 隱藏測試、gold patch、未公開答案及 benchmark leakage 不得用作 agent 輸入。
- 正式 verification claim 必須由實際 proof checker / test oracle / certificate 驗證。
- evaluator 改動和候選改動分 PR；不能為過關刪測試、放寬 assertion 或改 workload。
- 保存 compiler/runtime/toolchain/container 版本、seed、hardware class、wall time。
- 第一主線 CS-001，其餘排隊；預設30分鐘、0美元、100 trials。
