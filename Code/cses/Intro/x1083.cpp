// https://cses.fi/problemset/task/1083
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    int sum = 0;
    for(int i=1;i<n;i++){int x; cin>>x; sum += x;}
    cout<< (n*(1+n))/2 - sum;
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}