# RANDOM_CODE  [![wakatime](https://wakatime.com/badge/user/ec29ef99-8c9b-4017-ba6e-b52d5fcc5c9a.svg)](https://wakatime.com/@ec29ef99-8c9b-4017-ba6e-b52d5fcc5c9a)

JUST CODE 

![Repo Snake](https://raw.githubusercontent.com/123456dr/RANDOM_CODE/output/repo-snake-dark.svg)

[![GitHub Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=123456dr&repo=RANDOM_CODE&theme=github-dark)](https://github.com/123456dr/RANDOM_CODE)

![GitHub last commit](https://img.shields.io/github/last-commit/123456dr/RANDOM_CODE?style=flat-square&color=green) <br>
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/123456dr/RANDOM_CODE?style=flat-square&color=green)

<hr>
void solve() // 裡面宣告變數，結束直接銷毀<br>
GCD 最大公因
MST 最小公倍
<!--
||  |  | &nbsp; |  | [C++](./Code) |
-->

[目前總題數](/cont.txt)
<br>不想記錄水題ㄌ...


| 再 | 題源 | 題目 | 難 | 標籤 | NOTE | 程式碼連結 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | | | &nbsp; | ![](https://img.shields.io/badge/--blue) | | [C++](./Code) |
| | | | &nbsp; | ![](https://img.shields.io/badge/--blue) | | [C++](./Code) |
| | | | &nbsp; | ![](https://img.shields.io/badge/--blue) | | [C++](./Code) |
| | | | &nbsp; | ![](https://img.shields.io/badge/--blue) | | [C++](./Code) |
| | | | &nbsp; | ![](https://img.shields.io/badge/--blue) | | [C++](./Code) |
| ✅ 更加解 => 計數陣列 | CF | 0027_A 找最小未用過 ID | &nbsp; | ![](https://img.shields.io/badge/-pq-blue) ![](https://img.shields.io/badge/-邏輯-blue) | 其實當讀入的數字大於存在數字各數n者可以無視，因為未出現的數值一定會小於n，所以只要開計數陣列arr[n+1]預留index-1。舊思路: priority_queue<int, vector<int>, greater<int>>pq, 預設是less<i| [C++](./Code/Codeforces/0027_A_pq_greater.cpp) |
| ✅ 模板題 | 洛谷 | P2613. 有理数取余 | O | ![](https://img.shields.io/badge/-費馬數論-blue) ![](https://img.shields.io/badge/-大數-blue) | Fermat's Little Theorem (費馬小定理) [b^(P-1)%P == 1], P 是一個質數，任一非 P 倍數的整數 b/ Modular Inverse (模反元素 / 乘法逆元)/ Exponentiation by Squaring (快速冪)/ Big Number Modulo (大數取模)/ Congruence (同餘)| [C++](./Code/Luogu/2613_Fermat質數_快速冪_大數同餘.cpp) |
| ✅ 模板題 | 洛谷 | P2197. Nim 游戏 | OO | ![](https://img.shields.io/badge/-Nim_Game-blue) ![](https://img.shields.io/badge/-組合博弈論-blue) ![](https://img.shields.io/badge/-bitset-blue) ![](https://img.shields.io/badge/-XOR^-blue) | 有n堆石子，每次必取任意大於0顆，最後取石的獲勝(拿不到石子的輸)，求是否為先手必勝把每堆石子數轉二進位做 XOR，如果最後為 0 (開局平衡)則先手必輸。「高位減少、低位任意翻轉」最高位改為零代表可以任意改動後面幾位，一次把所有奇數位元變成偶數個 | [C++](./Code/Luogu/2197_NimGame.cpp) |
| ✅有更佳解 | LC | 3699. Number of ZigZag Arrays I | OOOOO | ![](https://img.shields.io/badge/-DP-blue) ![](https://img.shields.io/badge/-prefix_sum-blue) ![](https://img.shields.io/badge/-狀態擴展/轉移-blue) ![](https://img.shields.io/badge/-降維/平面化-blue) ![](https://img.shields.io/badge/-MOD-blue) | 嚴格交替轉狀態動態規劃，前綴和與一維滾動排除（TLE/MLE），鏡像對稱（reverse）與原地變數累加（curr）將重複狀態與記憶體配置降維打擊 | [C++](./Code/LeetCode/3699.cpp) |
| | LC | 1189 給字串求單字出現次數 | &nbsp; | ![](https://img.shields.io/badge/-map-blue) | map初始化不給定大小，mp['a'],{'a', 0} | [C++](./Code/LeetCode/1189.cpp) |
| | CF | 0204_A 求範圍 l~r 首尾數字一樣的數字個數 | &nbsp; | ![](https://img.shields.io/badge/-邏輯-blue) | ans = 9 + (n/10 - 1) + (末位是否大於等於首位 ? +1 : 0) | [C++](./Code/Codeforces/0204_A.cpp) |
| ✅未完成 | LC | WC_507_Q3 最少權重走訪所有節點並符合連續重複字母小於k個| OOOO | ![](https://img.shields.io/badge/-Diijkstra-blue) ![](https://img.shields.io/badge/-DFS_剪枝-blue) | 記憶陣列紀錄每個節點走訪所有子節點中的最小權重路徑，走過不重複走直接取值；每次走訪新路徑判斷當前累積連續重複字母數是否大於k，大於則剪枝，若當前字母與前一個字母不同技術直接歸零(必小於k個)| [C++](./Code) |
| | LC | WC_507_Q2. Valid Subarrays With Matching Sum Digits I | &nbsp; | ![](https://img.shields.io/badge/-前綴和-blue) ![](https://img.shields.io/badge/-prefix_sum-blue) | 求[l ,r] => v[r]-v[l-1] 插入第零項為0 | [C++](./Code/LeetCode/WC_507_q2.cpp) |
| ✅ | LC | BiWC_185_q3 樹 & 最短完成工作時間 | OOOO | ![](https://img.shields.io/badge/-DFS-blue) ![](https://img.shields.io/badge/-Tree_DP-blue) ![](https://img.shields.io/badge/-拓撲-blue) | | [C++](./Code/LeetCode/BiWC_185_q3.cpp) |
| ✅ | LC | BiWC_185_q2 路段點亮燈 | OO | ![](https://img.shields.io/badge/-貪心-blue) ![](https://img.shields.io/badge/-差分-blue) ![](https://img.shields.io/badge/-前綴-blue) | 點亮所有點並求最少設置燈數量，每盞燈可點亮+-1區段，差分[開始點+1, 離開點-1]並前綴建立初始燈況，貪心左到右遇到暗燈在其右手一點設燈(最貪)| [C++](./Code/LeetCode/BiWC_185_q2.cpp) |
| | TOPC_CF | 106084_B | &nbsp; | ![](https://img.shields.io/badge/-質數檢查-blue) | 最大檢查到 [i*i<=n] 是否整除 以及 先行判斷是否為偶數 %2 == 0| [C++](./Code/Contests/topc_2025_CF/106084_B.cpp) |
| | CF | 0026_A Almost Prime | | ![質數表](https://img.shields.io/badge/-暴力質數表-blue) | 建立暴力質數表 | [C++](./Code/Codeforces/0026_A.cpp) |
| | TOPC_CF | 106084_C One-Way Abyss | O | ![](https://img.shields.io/badge/-邏輯-blue) | 垂直水管有多條平行通道，選定出發的一條水管後每遇到左右轉通道都要隨之轉彎；每次讀入 x, y, val 就把水管v[x]值和v[y]值交換並且各自同時加上 val| [C++](./Code/Contests/topc_2025_CF/106084_C.cpp) |
| | TOPC_CF | 106084_D Palindromic Distance| OO | ![](https://img.shields.io/badge/-區間_DP-blue) ![](https://img.shields.io/badge/-回文與修正-blue) | 區間 DP 從長度2開始每次dp[i][j] = min(1+dp[i][j-1]刪右, 1+dp[i+1][j]刪左, dp[i+1][j-1]替換 也就是強迫改成i, j一樣)，最終答案為 dp[0][sz-1]| [C++](./Code/Contests/topc_2025_CF/106084_D.cpp) |
| | CF | 2237_A div1、2| OOO | ![](https://img.shields.io/badge/-單調棧-blue)  ![](https://img.shields.io/badge/-Monotonic_Stack-blue)| 利用【單調棧 (Monotonic Stack)】由右向左逆序掃描，維護「高度由小到大」的遞增序列；遇高牆則將其數量「整包累加」至當前跳板（引發連鎖削平合體），最終加總棧內所有「高度 × 數量」即為 $O(n)$ 最優解。| [C++](./Code/Codeforces/2237_A.cpp) |
| | CF | 0013_A 進位 | &nbsp; | ![](https://img.shields.io/badge/-進位制-blue) ![](https://img.shields.io/badge/-gcd()-blue) | 進位制轉換 先% 再/; 最小公因gcd()| [C++](./Code/Codeforces/0013_A.cpp) |
| | CF | 1084. 房間 | &nbsp; | ![](https://img.shields.io/badge/-貪心-blue) | 邏輯題 | [C++](./Code/Codeforces/1804_D.cpp) |
| | LC | 2095. Delete the Middle Node of a Linked List | O | ![](https://img.shields.io/badge/-Linked_List-blue) ![](https://img.shields.io/badge/-快慢指標-blue) | 題目求刪除中間節點，用快慢指標找中，蔡指標一次跳兩格到尾止，此時慢指標剛好指向中節點，直接設新變數為該節點，並修改該節點->next| [C++](./Code/LeetCode/2095.cpp) |
| | CF | 2236_C | &nbsp; | ![](https://img.shields.io/badge/-Math-blue)  ![](https://img.shields.io/badge/-雙迴圈-blue) | 數學題，最少動作次數，每次可/x或+1直到a == b，先除再加雙迴圈紀錄最小，[=max(ak,bk);v-aj+V-bk其中一個為0]，| [C++](./Code/Codeforces/2236_C.cpp) |
| ✅ | UT_DS| pF | OOOOOO | ![](https://img.shields.io/badge/-Dijkstra-blue) ![](https://img.shields.io/badge/-pq_greater-blue) | 首先建立一個二維陣列v，用來記錄每個節點相連接的節點及其權重。接著透過Dijkstra演算法搭配優先佇列（priority queue）進行計算，並使用一個distance陣列來記錄起點到達各節點i的最短距離x。初始化時，先將代表起點到自身距離為0的數對(0, s)丟入佇列。隨後持續執行pop操作直到佇列為空，每次取出一組資料(x, u)後，便遍歷節點u的所有相鄰節點v[u]；若x加上u到該相鄰節點的邊權重大於目前distance陣列中記錄的距離，則直接跳過，否則便更新該節點的最短距離最小值，並將此新距離與該相鄰節點的組合丟入佇列中繼續運算 | [C++](./Code/UT/Data_Structure/graph/graph_F.cpp) |
| ✅ | UT_DS| pE | OOO | ![](https://img.shields.io/badge/-加權最小-blue) ![](https://img.shields.io/badge/-互斥集_DSU-blue)  ![](https://img.shields.io/badge/-Kruskal's_Algorithm-blue) | 在過路費總額最少的情況下走訪所有節點，貪心並且每次檢查路線連接兩端的老大是否相異 | [C++](./Code/UT/Data_Structure/graph/graph_E.cpp) |
| ✅未完成 | CF | 0021 | O | ![](https://img.shields.io/badge/-正則表達式-blue) | regax | [C++](./Code/Codeforces/0021.cpp) |
| ✅未完成 | LC | 2196. Create Binary Tree From Descriptions | OOOOOO | ![](https://img.shields.io/badge/-binary_tree-blue) ![](https://img.shields.io/badge/-struct-blue) ![](https://img.shields.io/badge/-unordered_map-blue) ![](https://img.shields.io/badge/-unordered_set-blue)| | [C++](./Code/LeetCode/2196.cpp) |
| ✅ | UT_DS| pD Shortest Path | OOOO | ![](https://img.shields.io/badge/-最短路徑-blue) ![](https://img.shields.io/badge/-互斥集_DSU-blue)  ![](https://img.shields.io/badge/-Kruskal's_Algorithm-blue) | 求權重下最短路徑，克魯斯克爾演算法，貪心權重小到大，走與否根據檢查兩節點的根是否不相同，個節點的根預設為自己，之後每次連線，只把其中一邊的「根」改為另一邊的「根」達成集合串聯| [C++](./Code/UT/Data_Structure/graph/graph_D.cpp) |
| | CF | 2204 B - Right Maximum | &nbsp; | ![](https://img.shields.io/badge/-規律-blue) | 從左到右掃描若當前數字比前面最大值還大則一定會被輸出，第0項為一定會 | [C++](./Code/Codeforces/2204_B.cpp) |
| ✅未完成 | LC | 3753. Total Waviness of Numbers in Range II | OOOOO | ![](https://img.shields.io/badge/-Digit_DP-blue) | 數位DP & 前綴和 | [C++](./Code/LeetCode/3753.cpp) |
| ✅未完成 | LC | 3753 Total Waviness of Numbers in Range II| OOOOOO | ![](https://img.shields.io/badge/-Digit_DP-blue) ![](https://img.shields.io/badge/-位元處理-blue) | 三digit為組單位，比較中間數字是否被兩旁數字高/低包圍| [C++](./Code/LeetCode/3751.cpp) |
| ✅ | UT_DS | graph_C | OOO | ![](https://img.shields.io/badge/-DFS-blue) ![](https://img.shields.io/badge/-遍歷找最佳路線-blue) | 深度優先加剪枝，遍歷各條路徑並更新體力消耗最小值(找最佳路線) [DFS 時有任意一項累加超過 100% 則剪枝] [已記錄至少一組解答時，若當前 DFS se 累加高於已記錄結果之 se 則剪枝] | [C++](./Code/UT/Data_Structure/graph/graph_C.cpp) |
| | UT_DS | graph_B | O | ![](https://img.shields.io/badge/-DFS-blue) ![](https://img.shields.io/badge/-BFS-blue) | 廣度優先/深度優先 求圖走訪順序| [C++](./Code/UT/Data_Structure/graph/graph_B.cpp) |
| | CF | 2204_C Spring | &nbsp; | ![](https://img.shields.io/badge/-gcd()-blue) ![](https://img.shields.io/badge/-lcm()-blue) | 最大公因、最小公倍| [C++](./Code/Codeforces/2204_C.cpp) |
| ✅ | CF | 2204_D Alternating Path | OOO | ![](https://img.shields.io/badge/-Graph-blue) ![](https://img.shields.io/badge/-二分圖-blue) ![](https://img.shields.io/badge/-節點上色-blue) | 遍歷節點，上色各節點(上色分為向內/外節點)，並看當前節點鄰居有沒有同色，若同色則為不合法，若無上色則將該鄰點上為異色 三角關係為否 | [C++](./Code/Codeforces/2204_D.cpp) |
| | LC | 3633 & 3635 | &nbsp; | ![](https://img.shields.io/badge/-區間排程-blue) ![貪心](https://img.shields.io/badge/-貪心-blue) | 進階 => 區間排程 & 貪心 [有限時間內，每個設施有開始以及持續時間，求玩最多設施的排程]| [C++](./Code/LeetCode/3633.cpp) |
| ✅ | 洛谷 | 1908 逆序對 | OO | ![逆序對](https://img.shields.io/badge/-逆序對-blue) ![線段樹](https://img.shields.io/badge/-線段樹%20segment%20tree-blue) | 逆序對, 線段樹 segment tree , 離散化數據 | [C++](./Code/Luogu/1908.cpp) |
| | CF | 0022_A Second Order Statistics | &nbsp; | ![st.begin()++](https://img.shields.io/badge/-st.begin()%2B%2B-blue) | set 雙向迭代取址st.begin()++, insert()| [C++](./Code/Codeforces/0022_A.cpp) |
| | LC | 3496 Maximum Number of Items From Sale I | OOO | ![0/1 背包問題](https://img.shields.io/badge/-0%2F1%20背包問題-blue) ![dp](https://img.shields.io/badge/-dp-blue) | [預處理每個 item 真實價值 = 本身1 + 可觸發多少 free copies] [0/1 背包問題: 針對當前物品買或不買] [dp 紀錄各種價錢下可以買的最大值] [紀錄最便宜的 item price 在荷包有剩餘的情況下可以 all in 最便宜的商品]| [C++](./Code/LeetCode/3496.cpp) |
| ✅ | CF | 2232_C2 Seating Arrangement (Hard Version) | OO | | [O建立三變數: 空桌數、併桌位數、幾個客人A可移動] [X逐次遍歷各張桌子] | [C++](./Code/Codeforces/2232_C2.cpp) |
| ✅ | LC | 3161 Block Placement Queries | OO | ![線段樹](https://img.shields.io/badge/-線段樹-blue) ![upper_bound](https://img.shields.io/badge/-upper_bound-blue) ![最大區間](https://img.shields.io/badge/-最大區間-blue) | 線段樹, upper_bound位址, 最大區間 | [C++](./Code/LeetCode/3161.cpp) |
| | CF | 0276_A Lunch Rush | | | 注意 mx 初始化 -1e10(可能有負值) | [C++](./Code) |
| ✅ | LC | 3093 | OOOO | ![Trie](https://img.shields.io/badge/-Trie-blue) ![最長子序列](https://img.shields.io/badge/-最長子序列-blue) | 建立 Trie 樹, struct, class, 前後綴, 最長子序列 | [C++](./Code/LeetCode/3093_AIcode.cpp) |
| | CF | 0025_A IQ test | | | 找奇或偶陣列中哪個是奇葩 | [C++](./Code/Codeforces/0025_A.cpp) |
| | UVA | 10591 Happy Number | | ![unordered_set](https://img.shields.io/badge/-unordered_set-blue) | unordered_set 無序 & insert(x) & s.find() == s.end()判定未找到 | [C++](./Code/uva/CPE_20260324/10591.cpp) |
| | UVA | 10226 Hardwood Species | | | map<char,int>mp =>mp[x]=1 直接插入(x,1),遍歷時mp.first & mp.second ;printf 不和 cout混用, printf(%s, ss[i].data) | [C++](./Code/uva/CPE_20260324/10226.cpp) |
| | CF | 0026_C Parquet | O | ![貪心法](https://img.shields.io/badge/-貪心法-blue) | 數學題 當 n*m 為奇數則 false (由於木板類型各位偶數面積), 當 n or m(不可能同時)為奇數，分別用 1*2 and 2*1 填滿多出的奇數列/行，如果木板個數不夠則 false, 當奇數列行補足後，貪心法從最大面積開始排，若排不滿則 false | [C++](./Code/Codeforces/0026_C.cpp) |
| | CF | 0003_C Tic_tac_toe | | | 圈圈叉叉判輸贏或 illegal | [C++](./Code/Codeforces/0003_C.cpp) |
| | CF | 0026_B Regular_Bracket_Sequence | | | 合法括號對，當左括數不為零出現又括 => ok | [C++](./Code/Codeforces/0026_B.cpp) |
| | LC | 3120 Count the Number of Special Characters I | | ![isupper(char)](https://img.shields.io/badge/-isupper(char)-blue) ![toupper()](https://img.shields.io/badge/-toupper()-blue) | isupper(char), toupper() | [C++](./Code/LeetCode/3120.cpp) |
| | LC | 1871 Jump Game VII | O | ![DP](https://img.shields.io/badge/-DP-blue) ![滑動視窗](https://img.shields.io/badge/-滑動視窗-blue) | DP紀錄該'0'跳板是否可到達, 滑動視窗 合法範圍內累加跳板okCont，當剛超出左界的dp[i]為合法跳板則okCont-- | [C++](./Code/LeetCode/1871.cpp) |
| | LC | 1340 Jump Game V | O | ![DP](https://img.shields.io/badge/-DP-blue) ![DFS](https://img.shields.io/badge/-DFS-blue) |  DP, DFS, 任意點跳樓高到低求最長路徑 | [C++](./Code/LeetCode/1340.cpp) |