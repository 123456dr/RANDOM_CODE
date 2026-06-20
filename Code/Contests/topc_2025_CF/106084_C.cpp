// https://codeforces.com/gym/106084/problem/C
/*
垂直水管有多條平行通道，選定出發的一條水管後每遇到左右轉通道都要隨之轉彎
- 每次讀入 x, y, val 就把水管v[x]值和v[y]值交換並且各自同時加上 val
*/
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int t;cin>>t;
    while(t--){
        int n,m;
        cin>>n>>m;
        vector<int>v(n+1, 0);
        int ans = 0;
        while(m--){
            int x, y, val;
            cin>>x>>y>>val;
            int temp = v[x]+val;
            v[x] = v[y]+val;
            v[y] = temp;
            ans = max(ans, max(v[x], v[y]));
        }
        cout<<ans<<"\n";
    }
    
    
    return 0;
}