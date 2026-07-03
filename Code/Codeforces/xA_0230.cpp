#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int s, n;cin>>s>>n;
    vector<pair<int, int>>v(n);
    for(auto &i:v)cin>>i.first>>i.second;
    sort(v.begin(), v.end());
    int t = 0;
    for(auto i:v){
        if(i.first < s)s+=i.second, t++;
        else {
            cout<<"NO";
            return;
        }
    }
    cout<<"YES";
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}