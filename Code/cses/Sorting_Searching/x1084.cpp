// https://cses.fi/problemset/task/1084
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, m, k;cin>>n>>m>>k;
    vector<int>apt(n);
    vector<int>v(m);
    for(auto &i:apt)cin>>i;
    for(auto &i:v)cin>>i;
    int ans = 0;
    sort(apt.begin(), apt.end());
    sort(v.begin(), v.end());
    
    int a = 0, b = 0;
    while(a < n && b < m){
        if(abs(apt[a] - v[b]) <= k){
            ans++;
            a++,b++;
        }
        else if(apt[a] < v[b]-k)a++;
        else if(apt[a] > v[b]+k)b++;
    }
    
    cout<<ans<<'\n';
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}