// https://codeforces.com/contest/492/problem/B
/*
先建街道表矩陣v[l+1]，，binary search 找符合的 d，但因為要求倒伏點數其實直接找最大間距/2就好，
v[i]-v[i-1] <= 2d，還要特判起點和終點
*/
#include<bits/stdc++.h>
using namespace std;
#define f double
#define int long long

void solve(){
    int n, l;
    cin>>n>>l;
    vector<f>v(n, 0);
    for(auto &i:v)cin>>i;
    sort(v.begin(), v.end());
    
    f mx = 0;
    for(int i=0;i<n-1;i++){
        if((v[i+1] - v[i])/2 > mx)mx = (v[i+1] - v[i])/2;
    }
    if(v[0] != 0)mx = max(mx, v[0]);
    if(v[n-1] != l)mx = max(mx, l - v[n-1]);
    printf("%.10f", mx);
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}