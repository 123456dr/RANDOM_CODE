// https://codeforces.com/contest/2244/problem/C
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, x, y;
    cin>>n>>x>>y;
    vector<pair<int, int>>v(n);
    int id = 0;
    for(auto &i:v)cin>>i.first, i.second = id++;
    sort(v.begin(), v.end());
    int k = gcd(x, y);
    for(int i=0;i<n;i++){
        if(abs(v[i].second - i) % k != 0){
            cout<<"NO\n";
            return;
        }
    }
    cout<<"YES\n";
    return;

}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}