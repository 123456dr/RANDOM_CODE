// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int t;
    while(cin>>t){
    vector<pair<int, int>>v(t);
    int mx = 0;
    for(auto &i:v){
        cin>>i.first>>i.second;
        mx = max(mx, i.second);
    }
    vector<int>val(mx+1, 0);
    for(auto i:v){
        val[i.first]+=1;
        val[i.second]-=1;
    }
    int sum = 0;
    int ans = 0;
    for(auto i:val){
        sum += i;
        ans = max(ans, sum);
    }
    cout<<ans<<endl;}
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}