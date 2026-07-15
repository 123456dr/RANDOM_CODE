// https://codeforces.com/contest/2244/problem/D
/*
分區段求前n-1段絕對值和 + 最末段原始和
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, m;cin>>n>>m;
    vector<int>v(n);
    vector<int>b(m);
    for(auto &i:v)cin>>i;
    for(auto &i:b)cin>>i;
    sort(b.begin(), b.end());
    int id = 0;
    int ans = 0;
    for(int i=0;i<n && id<m;){
        int t = b[id++] - (id >=2 ? b[id-2] : 0);
        int sum = 0;
        while(t-- && i<n){
            sum += v[i++];
        }
        ans += abs(sum);
    }
    id = b[m-1];
    while(id < n){
        ans += v[id++];
    }
    cout<<ans<<'\n';
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}