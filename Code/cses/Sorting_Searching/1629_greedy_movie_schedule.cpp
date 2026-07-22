// https://cses.fi/problemset/task/1629/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    vector<pair<int, int>>v(n);
    for(auto &i:v)cin>>i.first>>i.second;
    
    sort(v.begin(), v.end(), [&](auto a, auto b) -> bool{
        return a.second<b.second;
    });

    int time = 0;
    int cnt = 0;
    for(int i=0;i<n;i++){
        if(v[i].first >= time)time = v[i].second, cnt++;
    }
    cout<<cnt;
    /*
    sort(v.begin(), v.end());
    int ans = 0;
    auto f = [&](auto &self, int num, int time, int cnt) -> auto{
        if(num > n-1) return cnt;
        int mx = 0;
        int select1 = self(self, num+1, (v[num].first >= time ? v[num].second : time), (v[num].first >= time ? cnt+1 : cnt));
        int select0 = self(self, num+1, time, cnt);
        mx = max(select0, select1);
        return mx;
    };
    cout<<f(f, 0, 0, 0);
    */
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}