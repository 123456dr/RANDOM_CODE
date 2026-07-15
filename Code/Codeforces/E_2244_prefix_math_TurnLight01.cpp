// https://codeforces.com/contest/2244/problem/E
/*
邏輯數學題，可無限次翻轉，所以需要 i 翻轉等於 0~i翻 + 0~i-1翻 => 指變動到i
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, q;cin>>n>>q;
    string s;cin>>s;
    vector<int>v(n, 0);
    for(int i=1;i<n;i++){
        if(s[i-1] == s[i])v[i]=1;
    }
    vector<int>c(n, 0);
    for(int i=1;i<n;i++){
        c[i] = c[i-1] + v[i];
    }
    int l, r, k;
    while(q--){
        cin>>l>>r>>k;
        if((c[r-1] - c[l-1]+1) / 2 <=k)cout<<"YES";
        else cout<<"NO";
        cout<<'\n';
    }
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}