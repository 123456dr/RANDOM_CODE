// gcd == Greatest Common Divisor
// lcm == Least Common Multiple
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int t=1, n;
    while(cin>>n){
    cout<<"Case "<<t++<<":\n";
    auto check = [&](int a, int b) -> int{
        while(b) a %= b, swap(a, b);
        return a;
    };
    auto dfs = [&](auto &self, vector<int>vis, vector<int>rem) -> void{
        if(vis.size() == n){
            for(auto i:vis)cout<<i<<" ";
            cout<<endl;
            return;
        }
        if(vis.size() == n-1){
            if(check(rem[0], vis[0]) != 1)return;
        }
        for(int i = 0;i<rem.size();i++){
            if(check(rem[i], vis.back()) == 1){
                vis.push_back(rem[i]);
                vector<int>backup;
                for(auto i:rem)backup.push_back(i);
                rem.erase(rem.begin()+i);
                self(self, vis, rem);
                vis.pop_back();
                rem.resize(0);
                for(auto i:backup)rem.push_back(i);
            }
        }
        return;
    };
    vector<int>tmp(n-1);
    int ind = 2;
    for(auto &i:tmp) i = ind++;
    dfs(dfs, {1}, tmp);
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);//int t = 1;
    //cin>>t;int T = t;
    //while(t--)
    solve();
    return 0;
}