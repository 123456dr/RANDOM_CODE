#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    int a = -1, b = 0;
    for(int i=1;i<=n;i++)cout<<(i & 1 ? b+=2 : a+=2)<<" ";
    cout<<'\n';
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}