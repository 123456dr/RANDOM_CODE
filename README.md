# RANDOM_CODE  [![wakatime](https://wakatime.com/badge/user/ec29ef99-8c9b-4017-ba6e-b52d5fcc5c9a.svg)](https://wakatime.com/@ec29ef99-8c9b-4017-ba6e-b52d5fcc5c9a)
JUST [C](./Code/)ODE 

![Repo Snake](https://raw.githubusercontent.com/123456dr/RANDOM_CODE/output/repo-snake-dark.svg)<!--[![GitHub Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=123456dr&repo=RANDOM_CODE&theme=github-dark)](https://github.com/123456dr/RANDOM_CODE) --><br>![GitHub last commit](https://img.shields.io/github/last-commit/123456dr/RANDOM_CODE?style=flat-square&color=green) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/123456dr/RANDOM_CODE?style=flat-square&color=green)
<details><summary>NOTE</summary>

- 確保讀入完全ㄚㄚㄚ
- 優先級 `==` > `&`
- BIT => `x & 1`末位一或零, `x >>= 1`除二 
- `value & 1` 判斷奇偶[== 1 奇; == 0偶]
- 可以暴力解 => 複雜度 `2e18` 
- `printf` 不可 `ios::...` 加速
- `char ca = 'A' | 32 = 'a'` => `tolower(c), toupper(c)`
- 三元運算子回傳型別相同 => `a ? to_string(mp[i]-'0) : ""`
- `GCD` 最大公因
- `LCM` 最小公倍
- `MST` 最小生成樹
- [QuickPower ](./Code/Luogu/QuickPower.cpp)快速冪_位元右移_奇偶 `&1` 交集運算
- 回傳迭代器, `*it` 取址, 找不到 `== v.end()`
    - `upper_bound(v.begin()`, `v.end, x) - v.begin()` // 最後小於, 最高位
    - `lower_bound(...)` // 第一個大於, 最低位
- `binary search` [左閉右開](./Code/Codeforces/C_0371_binarySearch.cpp)
    - `ans = mid` 迴圈內紀錄
    - `while l < r` // 跳出迴圈
    - `if(x <= bud)ans = mid, l = mid+1; else r = mid;`
- `for(...){mx = max(mx, cnt);}` 跳出迴圈記得再 `mx = max(mx, cnt)` 更新

- Lamdba: `auto dfs = [&](int x) -> void{// sth};`
</details>
<hr>

[目前總題數](/cont.txt)

| 再練 | 題源 | 題目與連結 | 難度 | 標籤 |
| :--- | :--- | :--- | :--- | :--- |
| | | [-](./Code)  | - | ![](https://img.shields.io/badge/--blue) |
| | | [-](./Code)  | - | ![](https://img.shields.io/badge/--blue) |
| | CF | [C_0371](./Code/Codeforces/C_0371_binarySearch.cpp) 對答案二分搜 左閉右開 現有部分食材求預算內採購食材湊出最多份漢堡 | 1 | ![](https://img.shields.io/badge/-binary_search-blue) ![](https://img.shields.io/badge/-左閉右開-blue) ![](https://img.shields.io/badge/-對答案二分搜-blue) |
| | CF | [B_2247](./Code/Codeforces/B_2247_constructArr.cpp) 構造最小子陣列長度恰為k且和能被m整除 前綴和同餘 | 2 | ![](https://img.shields.io/badge/-prefix-blue) ![](https://img.shields.io/badge/-formula-blue) ![](https://img.shields.io/badge/-constructive-blue) |
| ✅ | CF | [C_2247](./Code/Codeforces/C_2246_constructArr_taxi_01subArr.cpp) 奇偶性 10子序列和為奇數可翻轉成相反01 求最少操作 陣列a=b | 1 | ![](https://img.shields.io/badge/-枚舉狀況-blue) ![](https://img.shields.io/badge/-計程車-blue) ![](https://img.shields.io/badge/-constructive-blue) ![](https://img.shields.io/badge/-subsequence-blue) |
| | CF | [C_1398](./Code/Codeforces/C_1398_prefix_lengthEqualSum_subArray.cpp) 前綴和 子陣列總和等於長度求組合數 | 1 | ![](https://img.shields.io/badge/-subArray-blue) ![](https://img.shields.io/badge/-prefix-blue) ![](https://img.shields.io/badge/-math_formula-blue)|
| | CF | [C_0466](./Code/Codeforces/C_0466_prefix_linearScan_threeSameSumSubArray.cpp) 含負與零陣列，計算能切三份總和同且「連續」的子陣列切割方法數 | 1 | ![](https://img.shields.io/badge/-prefix-blue) ![](https://img.shields.io/badge/-linear_scan-blue) ![](https://img.shields.io/badge/-subArray-blue) |
| | CF | [E_2244](./Code/Codeforces/E_2244_prefix_math_TurnLight01.cpp) 點亮燈泡問題 | 3 | ![](https://img.shields.io/badge/-light-blue) |
| ✅✅ | CF | [F_2244](./Code/Codeforces/F_2244_DFS_continueTree.cpp) Anya Loves Trees! - 檢查左移子樹連續線段，非遞增落差需<=1 | 7 | ![](https://img.shields.io/badge/-DFS-blue) ![](https://img.shields.io/badge/-Tree-blue) |
| | CF | [B_0706](./Code/Codeforces/B_0706_binarySearch_upper_bound(bg,ed,x).cpp) 預算購買數量 - 二分搜 左閉右開 | - | ![](https://img.shields.io/badge/-binary_search-blue) ![](https://img.shields.io/badge/-lower_bound-blue) ![](https://img.shields.io/badge/-upper_bound()-blue) |
| ✅ | CF | [B_2246](./Code/Codeforces/B_2246_construct_Narray_totalSumCanDividedByAllArrElement.cpp) ezraft and Array - 建構陣列，每次加入元素為當前總和*2 | 3 | ![](https://img.shields.io/badge/-建構陣列-blue) |
| | LC | [M_2685](./Code/LeetCode/M_2685_completeComponents.cpp) Count the Number of Complete Components - 完整連通塊 | 1 | ![](https://img.shields.io/badge/-complete_components-blue) ![](https://img.shields.io/badge/-BFS-blue) ![](https://img.shields.io/badge/-Lamdba-blue) |
| ✅ | CF | [A_0579](./Code/Codeforces/A_0579_Bitmask.cpp) 轉二進位求1個數 - x&1最後一位是否為1, x>>1除二 | 1 | ![](https://img.shields.io/badge/-右移-blue) ![](https://img.shields.io/badge/-Bitmask-blue) |
| | CF | [A_0189](./Code/Codeforces/A_0189_dp_stone_ribbon.cpp) Cut Ribbon - 經典dp走石階/剪緞帶問題 | - | ![](https://img.shields.io/badge/-dp_石階-blue) |
| ✅ | CF | [B_0230](./Code/Codeforces/B_0230_primeTable_squareNum_sqrt(x)^2==x.cpp) T-primes - 質數表判斷與完全平方數 | 2 | ![](https://img.shields.io/badge/-prime_table-blue) |
| ✅ | LC | [M_509](./Code/LeetCode/M_WC_509_q2_pref&suff_更改一字母問s是否為t子字串.cpp) WC_509_q2 可修改一字s是否為t子字串 - pref與suff雙指標夾擊 | 3 | ![](https://img.shields.io/badge/-prefix-blue) ![](https://img.shields.io/badge/-suffix-blue) ![](https://img.shields.io/badge/-subsequeue-blue) ![](https://img.shields.io/badge/-雙指標-blue) |
| | CF | [C_0010](./Code/Codeforces/C_0010_digitalRoot_數論分塊_.cpp) Digital Root - 數位根與數論分塊 | 3 | ![](https://img.shields.io/badge/-digital_root-blue)![](https://img.shields.io/badge/-數論分塊-blue) |
| ✅ | LC | [M_508](./Code/LeetCode/M_WC_508_q2_diffArray_interval.cpp) WC508 Q2. Filter Occupied Intervals - 差分與掃描線 | 2 | ![](https://img.shields.io/badge/-diff_差分-blue) ![](https://img.shields.io/badge/-sweep_line-blue) |
| | CF | [B_0158](./Code/Codeforces/B_0158_taxi_fourPeoInTeamSeat.cpp) taxi四人座 - 頻率陣列貪心併車 | - | ![](https://img.shields.io/badge/-數學技巧-blue) ![](https://img.shields.io/badge/-freqArray-blue) |
| ✅ | LC | [H_3739](./Code/LeetCode/H&M_3739&3737_prefix_FreqArray_DP_Offset_單調性.cpp) Count Subarrays With Majority Element II - +1/-1前綴和與頻率陣列動態維護 | 5 | ![](https://img.shields.io/badge/-freq_arry-blue) ![](https://img.shields.io/badge/-dp-blue) ![](https://img.shields.io/badge/-前綴動態移轉-blue) ![](https://img.shields.io/badge/-單調性-blue) ![](https://img.shields.io/badge/-offset-blue) |
| ✅ | CF | [A_0027](./Code/Codeforces/A_0027_pq_greater.cpp) 找最小未用過ID - 計數陣列預留index-1 | - | ![](https://img.shields.io/badge/-pq-blue) ![](https://img.shields.io/badge/-邏輯-blue) |
| ✅ | 洛谷 | [P2613](./Code/Luogu/2613_Fermat質數_快速冪_大數同餘.cpp) 有理数取余 - 費馬小定理, 模反元素, 快速冪 | 1 | ![](https://img.shields.io/badge/-費馬數論-blue) ![](https://img.shields.io/badge/-大數-blue) |
| ✅ | 洛谷 | [P2197](./Code/Luogu/2197_NimGame.cpp) Nim 游戏 - 組合博弈論, 轉二進位做XOR | 2 | ![](https://img.shields.io/badge/-Nim_Game-blue) ![](https://img.shields.io/badge/-組合博弈論-blue) ![](https://img.shields.io/badge/-bitset-blue) ![](https://img.shields.io/badge/-XOR^-blue) |
| ✅ | LC | [H_3699](./Code/LeetCode/H_3699_dp_prefixSum.cpp) Number of ZigZag Arrays I - 嚴格交替轉狀態DP, 鏡像對稱與原地降維 | 5 | ![](https://img.shields.io/badge/-DP-blue) ![](https://img.shields.io/badge/-prefix_sum-blue) ![](https://img.shields.io/badge/-狀態擴展/轉移-blue) ![](https://img.shields.io/badge/-降維/平面化-blue) ![](https://img.shields.io/badge/-MOD-blue) |
| | LC | [Z_1189](./Code/LeetCode/Z_1189.cpp) 給字串求單字出現次數 - map初始化不給定大小 | - | ![](https://img.shields.io/badge/-map-blue) |
| | CF | [A_0204](./Code/Codeforces/A_0204.cpp) 求範圍l~r首尾數字一樣的個數 - 數學邏輯計算 | - | ![](https://img.shields.io/badge/-邏輯-blue) |
| ✅ | LC | [M_507](./Code/LeetCode/) WC_507_Q3 最少權重走訪所有節點 - DFS剪枝與Dijkstra | 4 | ![](https://img.shields.io/badge/-Diijkstra-blue) ![](https://img.shields.io/badge/-DFS_剪枝-blue) |
| | LC | [M_507](./Code/LeetCode/M_WC_507_q2.cpp) WC_507_Q2. Valid Subarrays With Matching Sum Digits - 前綴和 | - | ![](https://img.shields.io/badge/-前綴和-blue) ![](https://img.shields.io/badge/-prefix_sum-blue) |
| ✅ | LC | [M_185](./Code/LeetCode/M_BiWC_185_q3.cpp) BiWC_185_q3 樹 & 最短完成工作時間 - 拓撲與Tree DP | 4 | ![](https://img.shields.io/badge/-DFS-blue) ![](https://img.shields.io/badge/-Tree_DP-blue) ![](https://img.shields.io/badge/-拓撲-blue) |
| ✅ | LC | [M_185](./Code/LeetCode/M_BiWC_185_q2.cpp) BiWC_185_q2 路段點亮燈 - 差分前綴與極限貪心設燈 | 2 | ![](https://img.shields.io/badge/-貪心-blue) ![](https://img.shields.io/badge/-差分-blue) ![](https://img.shields.io/badge/-前綴-blue) |
| | TOPC | [B_106084](./Code/Contests/topc_2025_CF/106084_B.cpp) 質數檢查 - 判斷偶數與i*i<=n | - | ![](https://img.shields.io/badge/-質數檢查-blue) |
| | TOPC | [C_106084](./Code/Contests/topc_2025_CF/106084_C.cpp) One-Way Abyss - 陣列值交換並累加val | 1 | ![](https://img.shields.io/badge/-邏輯-blue) |
| | TOPC | [D_106084](./Code/Contests/topc_2025_CF/106084_D.cpp) Palindromic Distance - 區間DP求最小刪除替換次數 | 2 | ![](https://img.shields.io/badge/-區間_DP-blue) ![](https://img.shields.io/badge/-回文與修正-blue) |
| | CF | [A_2237](./Code/Codeforces/A_2237.cpp) div1、2 - 逆序掃描，單調棧削平合體 | 3 | ![](https://img.shields.io/badge/-單調棧-blue)  ![](https://img.shields.io/badge/-Monotonic_Stack-blue)|
| | CF | [A_0013](./Code/Codeforces/A_0013.cpp) 進位 - 進位制轉換與GCD | - | ![](https://img.shields.io/badge/-進位制-blue) ![](https://img.shields.io/badge/-gcd()-blue) |
| | CF | [D_1804](./Code/Codeforces/D_1804.cpp) 房間 - 貪心邏輯題 | - | ![](https://img.shields.io/badge/-貪心-blue) |
| | LC | [M_2095](./Code/LeetCode/M_2095.cpp) Delete the Middle Node of a Linked List - 快慢指標找中點 | 1 | ![](https://img.shields.io/badge/-Linked_List-blue) ![](https://img.shields.io/badge/-快慢指標-blue) |
| | CF | [C_2236](./Code/Codeforces/C_2236.cpp) 最少動作次數 - 數學雙迴圈紀錄最小 | - | ![](https://img.shields.io/badge/-Math-blue)  ![](https://img.shields.io/badge/-雙迴圈-blue) |
| ✅ | UT | [F_graph](./Code/UT/Data_Structure/graph/graph_F.cpp) 最短路徑 - Dijkstra演算法搭配優先佇列 | 6 | ![](https://img.shields.io/badge/-Dijkstra-blue) ![](https://img.shields.io/badge/-pq_greater-blue) |
| ✅ | UT | [E_graph](./Code/UT/Data_Structure/graph/graph_E.cpp) 過路費總額最少 - Kruskal貪心與互斥集DSU | 3 | ![](https://img.shields.io/badge/-加權最小-blue) ![](https://img.shields.io/badge/-互斥集_DSU-blue)  ![](https://img.shields.io/badge/-Kruskal's_Algorithm-blue) |
| ✅ | CF | [A_0021](./Code/Codeforces/A_0021.cpp) Regax 正則表達式 | 1 | ![](https://img.shields.io/badge/-正則表達式-blue) |
| ✅ | LC | [M_2196](./Code/LeetCode/M_2196.cpp) Create Binary Tree From Descriptions - 建立二元樹 | 6 | ![](https://img.shields.io/badge/-binary_tree-blue) ![](https://img.shields.io/badge/-struct-blue) ![](https://img.shields.io/badge/-unordered_map-blue) ![](https://img.shields.io/badge/-unordered_set-blue)|
| ✅ | UT | [D_graph](./Code/UT/Data_Structure/graph/graph_D.cpp) Shortest Path - Kruskal克魯斯克爾與集合串聯 | 4 | ![](https://img.shields.io/badge/-最短路徑-blue) ![](https://img.shields.io/badge/-互斥集_DSU-blue)  ![](https://img.shields.io/badge/-Kruskal's_Algorithm-blue) |
| | CF | [B_2204](./Code/Codeforces/B_2204.cpp) Right Maximum - 掃描當前數字與前面最大值 | - | ![](https://img.shields.io/badge/-規律-blue) |
| ✅ | LC | [H_3753](./Code/LeetCode/H_3753.cpp) Total Waviness of Numbers in Range II - 數位DP與前綴和 | 5 | ![](https://img.shields.io/badge/-Digit_DP-blue) |
| ✅ | LC | [H_3753](./Code/LeetCode/H_3753.cpp) Total Waviness of Numbers in Range II - 三digit為組比較包圍 | 6 | ![](https://img.shields.io/badge/-Digit_DP-blue) ![](https://img.shields.io/badge/-位元處理-blue) |
| ✅ | UT | [C_graph](./Code/UT/Data_Structure/graph/graph_C.cpp) 遍歷找最佳路線 - DFS與體力消耗剪枝 | 3 | ![](https://img.shields.io/badge/-DFS-blue) ![](https://img.shields.io/badge/-遍找最佳路線-blue) |
| | UT | [B_graph](./Code/UT/Data_Structure/graph/graph_B.cpp) BFS/DFS 求圖走訪順序 | 1 | ![](https://img.shields.io/badge/-DFS-blue) ![](https://img.shields.io/badge/-BFS-blue) |
| | CF | [C_2204](./Code/Codeforces/xC_2204.cpp) Spring - 最大公因與最小公倍 | - | ![](https://img.shields.io/badge/-gcd()-blue) ![](https://img.shields.io/badge/-lcm()-blue) |
| ✅ | CF | [D_2204](./Code/Codeforces/D_2204.cpp) Alternating Path - 二分圖節點上色判斷合法 | 3 | ![](https://img.shields.io/badge/-Graph-blue) ![](https://img.shields.io/badge/-二分圖-blue) ![](https://img.shields.io/badge/-節點上色-blue) |
| | LC | [M_3633](./Code/LeetCode/M_3633.cpp) 區間排程 - 貪心玩最多設施 | - | ![](https://img.shields.io/badge/-區間排程-blue) ![貪心](https://img.shields.io/badge/-貪心-blue) |
| ✅ | 洛谷 | [P1908](./Code/Luogu/1908_SegmentTree.cpp) 逆序對 - 線段樹與離散化數據 | 2 | ![逆序對](https://img.shields.io/badge/-逆序對-blue) ![線段樹](https://img.shields.io/badge/-線段樹%20segment%20tree-blue) |
| | CF | [A_0022](./Code/Codeforces/xA_0022.cpp) Second Order Statistics - set雙向迭代取址 | - | ![st.begin()++](https://img.shields.io/badge/-st.begin()%2B%2B-blue) |
| | LC | [M_3496](./Code/LeetCode/M_3496.cpp) Maximum Number of Items From Sale I - 0/1背包問題求最大值 | 3 | ![0/1 背包問題](https://img.shields.io/badge/-0%2F1%20背包問題-blue) ![dp](https://img.shields.io/badge/-dp-blue) |
| ✅ | CF | [C_2232](./Code/Codeforces/C_2236.cpp) Seating Arrangement (Hard) - 建立變數追蹤空桌與併桌 | 2 | |
| ✅ | LC | [H_3161](./Code/LeetCode/H_3161.cpp) Block Placement Queries - 線段樹與最大區間 | 2 | ![線段樹](https://img.shields.io/badge/-線段樹-blue) ![upper_bound](https://img.shields.io/badge/-upper_bound-blue) ![最大區間](https://img.shields.io/badge/-最大區間-blue) |
| | CF | [A_0276](./Code/Codeforces/xB_0276.cpp) Lunch Rush - mx初始化-1e10防負值 | - | |
| ✅ | LC | [H_3093](./Code/LeetCode/H_3093_AIcode.cpp) 建立 Trie 樹 - 前後綴與最長子序列 | 4 | ![Trie](https://img.shields.io/badge/-Trie-blue) ![最長子序列](https://img.shields.io/badge/-最長子序列-blue) |
| | CF | [A_0025](./Code/Codeforces/A_0025.cpp) IQ test - 找奇或偶陣列中哪個是奇葩 | - | |
| | UVA | [UVA_10591](./Code/uva/CPE_20260324/10591.cpp) Happy Number - unordered_set判斷未找到 | - | ![unordered_set](https://img.shields.io/badge/-unordered_set-blue) |
| | UVA | [UVA_10226](./Code/uva/CPE_20260324/10226.cpp) Hardwood Species - map插入與printf不混用 | - | |
| | CF | [C_0026](./Code/Codeforces/C_0026.cpp) Parquet - 數學奇偶面積判斷與貪心排木板 | 1 | ![貪心法](https://img.shields.io/badge/-貪心法-blue) |
| | CF | [C_0003](./Code/Codeforces/C_0003.cpp) Tic_tac_toe - 圈圈叉叉判輸贏 | - | |
| | CF | [B_0026](./Code/Codeforces/B_0026.cpp) Regular_Bracket_Sequence - 左括號不為零出現右括即合法 | - | |
| | LC | [Z_3120](./Code/LeetCode/Z_3120.cpp) Count the Number of Special Characters I - 大小寫轉換 | - | ![isupper(char)](https://img.shields.io/badge/-isupper(char)-blue) ![toupper()](https://img.shields.io/badge/-toupper()-blue) |
| | LC | [M_1871](./Code/LeetCode/M_1871.cpp) Jump Game VII - DP紀錄與滑動視窗累加 | 1 | ![DP](https://img.shields.io/badge/-DP-blue) ![滑動視窗](https://img.shields.io/badge/-滑動視窗-blue) |
| | LC | [M_1340](./Code/LeetCode/M_1340.cpp) Jump Game V - DP與DFS跳樓求最長路徑 | 1 | ![DP](https://img.shields.io/badge/-DP-blue) ![DFS](https://img.shields.io/badge/-DFS-blue) |



<br><br><br><hr>
#### VScode快捷們
- `ctrl + k and v` 開啟 .md 預覽 (自訂快捷
- `ctrl + B` 側邊攔
- `ctrl + shift + E` 切換焦點
- `F2` 改檔名
- `F10` 建檔選單<br>
[CP_Tracker.pyw](./AWARD/mess/CheckIn_py/哥本哈根_根本超讚ㄏ_0.png) <small><small><small>(好耶 會自動開啟 desu</small></small></small> <br>
[mem](./AWARD/)