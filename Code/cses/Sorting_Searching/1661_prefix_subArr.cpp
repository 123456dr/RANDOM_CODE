// https://cses.fi/problemset/task/1661
/*
走一次算前綴和，並把「前綴和各項值」和「原始元素各值』雜湊紀錄
再走一次檢查前綴和迴圈看雜湊表是否存在 [pref - tar] 項目
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, tar;
    cin>>n>>tar;
    map<int, int>mp;
    //set<int>st;
    vector<int>pref(n+1, 0);
    int ans = 0;
    mp[0]=1;
    for(int i=1;i<=n;i++){
        int x;cin>>x;
        pref[i] = pref[i-1] + x;
        if(mp.find(pref[i] - tar) != mp.end())ans+=mp[pref[i] - tar];
        mp[pref[i]]++;
    }
    cout<<ans;
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}