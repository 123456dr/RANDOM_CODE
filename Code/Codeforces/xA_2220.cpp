// https://codeforces.com/problemset/problem/2220/A
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    vector<int>v(n);
    map<int, int>freq;
    int ok = 1;
    for(auto &i:v){cin>>i; freq[i]++;if(freq[i] >= 2)ok = 0;}
    if(!ok){cout<<-1<<'\n';return;}
    sort(v.rbegin(), v.rend());
    for(auto i:v)cout<<i<<" ";
    cout<<'\n';
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}