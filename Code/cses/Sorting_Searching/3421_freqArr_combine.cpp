/*
freqArray, 每一種數字有存在個數 num 個，總共有 num+1 種選擇數(+1 為不選擇)
ans = 所有數字頻率數 +1 後相乘
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    const int mod = 1e9+7;
    map<int, int>mp;
    if(n == 0){cout<<1;return;}
    while(n--){
        int x;cin>>x;
        mp[x]++;
    }
    int ans = 1;
    for(auto i:mp){
        ans *= (i.second+1);
        ans %= mod;
    }
    cout<<(ans-1) % mod;
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}