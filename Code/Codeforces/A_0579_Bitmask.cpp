// https://codeforces.com/problemset/problem/579/A
/*
輸入 x 必須為數個 2 的次方數的和，
而 2 進位 111 代表 2^2 & 2^1 & 2^0 各一個的加總
所以所求為 x 轉為二進制每次右移一檢查有幾個1
好耶好耶
*/
#include <bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int x;cin>>x;
    int cnt = 0;
    while(x){
        if(x & 1)cnt++; // 交集
        x >>= 1;
    }
    cout<<cnt;
}

signed main(){
    solve();
    return 0;
}