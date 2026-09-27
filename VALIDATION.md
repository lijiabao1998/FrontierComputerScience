# 計算機科學驗證契約

每個子任務先凍結 specification、input domain、oracle/evaluator、baseline、resource budget、hardware/runtime、成功與失敗條件。

至少做：
1. 正例、負例、邊界例；故意破壞候選必須能紅。
2. correctness 與速度分開；性能比較固定 workload、warm-up、hardware class 和統計方式。
3. repository 任務記依賴 closure、build commands、tests、hidden-information 邊界。
4. formal verification 記 theorem/spec、toolchain、公理／trusted base；自然語言需求與形式 specification 另作審核。
5. agent benchmark 查 leakage、gold solution 暴露、test contamination 與 task validity。
6. 分散式／隨機系統報 fault model、network model、adversary、概率保證與 liveness/safety 分離。

一輪完成不等於問題完成；有限 benchmark 的結果不能直接外推到所有程式、所有 repository 或所有硬體。
