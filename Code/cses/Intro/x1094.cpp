// https://cses.fi/problemset/task/1094
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    int ans = 0;
    int last;cin>>last;n--;
    while(n--){
        int x;cin>>x;
        if(x < last)ans += abs(x - last);
        else last = x;
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