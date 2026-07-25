// https://codeforces.com/problemset/problem/2226/A
#include<bits/stdc++.h>
using namespace std;
#define int long long
int mod = 676767677;

void solve(){
    int n;cin>>n;
    int ans = 0;
    int cnt1 = 0;
    int N = n;
    int mxid = 0;
    while(n--){
        int x;cin>>x;
        if(x!=1)ans+=x;
        else cnt1++;
        if(1 < x)mxid = N-n-1;
    }
    if(mxid != N-1)ans++;
    if(cnt1 == N)cout<<1<<'\n';
    else cout<<ans % mod<<'\n';
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}