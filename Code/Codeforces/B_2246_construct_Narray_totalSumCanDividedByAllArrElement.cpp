// https://codeforces.com/contest/2246/problem/B
#include<bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    vector<int>v(t);
    int mx = 0;
    for(auto &i:v)cin>>i, mx = max(mx, i);

    vector<int>dp(max(3LL,mx+1), 0);
    dp[0] = 1, dp[1] = 2, dp[2] = 3;
    int id = 3;
    int sum  = 6;
    while(id < mx){
        dp[id++] = sum;
        sum *= 2;
    }

    auto solve = [&](int n) -> auto{
        for(int i=0;i<n;i++){
            cout<<dp[i]<<" ";
        }cout<<'\n';
    };

    for(auto i:v){
        if(i == 2)cout<<-1<<'\n';
        else if(i == 1)cout<<1<<'\n';
        else if(i == 3)cout<<"1 2 3\n";
        else{
            solve(i);
        }
    }
    return 0;
}