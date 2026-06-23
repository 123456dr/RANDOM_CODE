/*
- bitset<32 or 8> name(num) : 轉二進位
- int result = (int)a^(int)b : 兩整數可以直接 XOR 運算

- 組合博弈論（Combinatorial Game Theory）
    - Nim 遊戲
    - SG 函數
- 兩人輪流、一次一堆、最後動手獲勝

有n堆石子，每次必取任意大於0顆，最後取石的獲勝(拿不到石子的輸)，求是否為先手必勝
把每堆石子數轉二進位做 XOR，如果最後為 0 (開局平衡)則先手必輸
- 勝者關鍵為: 可以透過拿取一堆中的石子把局面達成數量平衡。平衡定義為[各石堆轉二進位每個位元都有偶數個1或0]
- 因為平衡時不管拿取任意數石子，換對方時皆可還原局面成平衡導致先手輸
- 所有石子堆做 XOR，等於零代表二進位每個位元都有偶數個1或0
- 如果當下失衡，則找XOR後的最高位，並找到所有石堆中一個同位(必為奇數但可能大於1個)為1的改為0
    - 「高位減少、低位任意翻轉」的數學特權
        - 因為是最高位改為零代表可以任意改動後面幾位，一次把所有奇數位元變成偶數個
        - 也就是 XOR 後[101]=> 101->010 == 拿掉3個石子(保證在同堆操作 最大位扣掉保留數量)
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    int cal = 0;
    while(n--){
        int x;cin>>x;
        cal ^=x; 
    }
    if(cal != 0){
        cout<<"Yes";
    }
    else cout<<"No";
}

signed main(){
    int t;cin>>t;
    while(t--){
        solve();
        cout<<"\n";
    }

    return 0;
}