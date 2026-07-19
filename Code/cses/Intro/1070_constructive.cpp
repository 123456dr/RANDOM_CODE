// https://cses.fi/problemset/task/1070
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    if(n == 1){cout<<1;return;}
    if(n == 4){cout<<"2 4 1 3";return;}
    if(n<=4){cout<<"NO SOLUTION";return;}
    vector<int>odd;
    vector<int>even;
    for(int i=1;i<=n;i++){
        if(i & 1)odd.push_back(i);
        else even.push_back(i);
    }
    for(auto i:even)cout<<i<<" ";
    for(auto i:odd)cout<<i<<" ";
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}