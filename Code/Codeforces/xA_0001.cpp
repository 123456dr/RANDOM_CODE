// https://codeforces.com/problemset/problem/1/A
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, m, a;
    cin>>n>>m>>a;
    int ansx = n/a, ansy = m/a;
    if(ansx * a<n)ansx++;
    if(ansy * a<m)ansy++;
    cout<<ansx * ansy;
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}