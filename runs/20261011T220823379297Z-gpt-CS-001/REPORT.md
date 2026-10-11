CS-001 實際獨立驗證完成：修復輪 INDEPENDENT_KERNEL_KNOWN_PROOF_PASS。第一輪維持 PARTIAL_OR_FAILED_INDEPENDENT_KERNEL_VALIDATION／exit1，全部失敗未改寫。本輪只重現已公開完整證明，CS-001 題卡仍 OPEN。

| 類別 | 結論與證據 |
|---|---|
| 計畫／准入 | 每輪先四路實際檢索、固定協議／程式與九個原始輸入，獨立靜態審查、公開scope/budget讀回、official admit、本地協議提交，才啟動唯一attempt-1。 |
| 既存基線 | PR4來源 head 8e21cd467c8aeae3c56f44c95e7f6df7103ec403，upstream proof commit4c79694f5b96c6789b307e2911088af6b19540ac；完整公開證明已見。原作者NOT_RUN結果未覆寫。 |
| 實際數值 | 原命題的型別／值 Expr.constants 閉包：161 declarations、1451引用邊、最大BFS距離6，missing0。唯一actual axiom是propext；無sorry/native/custom/unsafe/partial reachable declaration。 |
| 獨立驗證 | 獨立Lean結構式Expr walker＋FIFO BFS，ConstantInfo.type與value? true納opaque內容；獨立Python固定點核對＋official collectAxioms只交叉檢查。未使用作者parser/classifier。八項總checks全true。 |
| 新結果的範圍 | 新增的是這台電腦的實際kernel/type/closure/control重現與測量；不屬於新定理、未見證明搜尋、效能改善或十五科／CS父題完成。 |

官方Elan side-by-side安裝於21:37:55.990625開始、21:43:57.294226完成exit0，先於研究預算。Lean4.18.0 commit11ccbced7964，匹配Lake5.0.0-11ccbce；舊v4.33.1/v4.34.0-rc2四個binary及Elan settings哈希不變。工具鏈安裝不算研究成果。詳見runs/20261011T214605121352Z-gpt-CS-001/installation/。

來源proof原始bytes SHA2562454c074170e8f2ca8e05b1339678457a5873a50307d4e2c1e1c1e585ca02a85；Lake manifest packages=[]。source root51個既存Git entries之OID/mode全未變。最新sourcePR/main讀回仍8e21cd...／1688c473...；治理main d05c1979...比pin9c3ae2db...只改PROTOCOL_VERSIONS.md、STATUS.md，無gate程式改動，沿用CS宣告pin。

保守整體CS預算21:44:59→22:14:59 UTC。第一輪22:05:56.515324→22:06:03.790495；修復輪22:12:50.488293→22:13:00.294090。包括全部準備，finish距start1681.294090秒（少於1800）。兩輪共16個compiler children，全部mask1、順序執行、無逾時；每次上限120秒含有界own-process清理；USD0。後續artifact review／commit／publication是已登記的metadata步驟，不增加科學執行。

第一輪獨立exporter用了Lean保留字at，line37 parse error。Lake build、未修改source之direct trust=0檢查、七邊界、真正rfl反例均通過；exporter未編譯成功，type/closure/sorry/custom因此沒有結果，總verdict PARTIAL／exit1。此錯誤獨立靜態審查也未抓到，已坦白保留；不是權限拒絕。r1 protocol commit296c1218ec7d8b65c423a7207f393e1875f31109，失敗結果commitb6e5f8ba690d0f21222b0af5773d3dd124fec394。

同一原截止時間內新開r2，Lean code只at→cursor，另綁獨立round/result scope与cumulative16 guard；重新檢索、凍結、static review、公開claim/readback、official admit並commit7649f983211c85e015e61afbdddf615bbd5d42bb後才執行。原r1程序／協議／結果未修改或重播。

| 修復輪實際命令步驟 | exit | wall秒 | CPU mask |
|---|---:|---:|---:|
| 01-lake-build | 0 | 1.994943 | 1 |
| 02-kernel-source | 0 | 1.788759 | 1 |
| 03-audit-support | 0 | 1.393386 | 1 |
| 04-type-root-closure | 0 | 1.308651 | 1 |
| 05-seven-boundaries | 0 | 0.410684 | 1 |
| 06-false-conjunction | 1 | 0.391695 | 1 |
| 07-sorry-control | 0 | 1.238785 | 1 |
| 08-custom-axiom | 0 | 1.242213 | 1 |

命題透過Lean實際ascription核對forall {tau : Ty} (t : Term tau), Term.Equiv t (Term.constFold t)。原proof以direct lean -t0 -j1 --json檢查，七個原Boundary.lean例均編譯成功。FalseControl真rfl錯誤exit1；missing imports／工具錯誤／逾時從不算negative-control成功。Sorry fixture編譯exit0後closed graph15 nodes／29edges／maxdistance2，actual forbidden axiom sorryAx，audit REJECT；custom fixture編譯exit0後3nodes／3edges／distance1，actual independentForbidden，audit REJECT。所有八checks合入總判定。

r2 root graphSHA256 6a108ded3aeae14375107edd994a52e7817eb28b9c09025090b1ffb5945ea54a。allowlist僅propext/Classical.choice/Quot.sound；actual只用propext。closure graph包含core/generated declarations，定義的邊只有type/value Expr.constants；不等同module／所有kernel reduction rules閉包，也不可與benchmark篩選後12依賴／depth3比較。沒跑另一个kernel或native_decide專用mutation；native/custom禁止規則與實際root inventory有記錄，已實際跑sorry和custom公理控制。沒有新compiler correctness全域結論或proof-search系統評估。

公開scope登記：r1 https://github.com/lijiabao1998/FrontierComputerScience/pull/4#issuecomment-6114320766 於22:03:07；r2 https://github.com/lijiabao1998/FrontierComputerScience/pull/4#issuecomment-6114432484 於22:12:28。r1第一次讀回scope/budget/source/protocol hashes均完整，但破折號經PowerShell解碼變兩個replacement chars，complete-string binding assertion失敗；official admit已先完成。原raw讀回與failed binding保留，same-comment cosmetic correction與完整exact readback於22:05:05、protocol commit及任何science之前完成。r2採ASCII JSON傳遞，exact readback先於22:12:35 official admit，順序完整。

復跑入口（歷史实际命令，當前兩個exclusive launch markers禁止再次執行；真正復跑需新授權／新round／新protocol固定與准入，不能刪marker或覆寫attempt）：

```powershell
python -X utf8 problems/CS-001/experiments/independent_20261011_r2/verify.py --round-id 20261011T220823379297Z-gpt-CS-001 --attempt <absolute-repo>/problems/CS-001/results/independent_20261011_r2/attempt-1
```

每個step的.json存絕對binary/完整argv、cwd、PID、affinity、開始/结束、exit、wall、原始stdout/stderr size/SHA。實際commands在results/independent_20261011_r2/attempt-1/01..08*.json；raw source/fixtures與frozenhash manifest在experiments/independent_20261011_r2/；實際elaborated graph及獨立audit在attempt-1/scratch/。compiled .olean與.lake仍本地保留但不進Git，無付費／下載第三方依賴。

獨立r1 artifact review SHA2562d654231b96e280248251d8b3d5b91162c5f39764d5e40c5683789efa73491b9；r2 review SHA2562a8d3aa0ea771cddc3516173c11041f296bc55d1809ed11221bf7ddce676ea92，見run/evidence。靜態BLOCKED與修正、舊失敗、官方工具安裝、初始錯誤讀取路徑與404全部保留；部分早期唯讀／準備命令僅tool UI原輸出與PREPARATION_NOTES重建metadata，未冒稱完整dedicated raw capture。Python頂層有既存98-byte real-location warning；compiler children stderr為空，不將頂層stderr說成空。

SOC-008／ASTRO-003仍PLANNING_ONLY_NOT_RUN。SOC需先固定資料byte hash／GPL及split，不偷看test調參；ASTRO需確認無LICENSE資料分析准入及2024/2025版本差异，否則止於data audit；未下載或訓練。MAT/META所需合法資料／完整外部experiment logs仍待提供。無合併、部署、main／source branch寫入。
