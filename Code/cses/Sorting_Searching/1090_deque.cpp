// https://cses.fi/problemset/task/1090
/*
最多兩個人，所以不用四人座問題配對(2-1-1or2-2)
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, x;
    cin>>n>>x;
    vector<int>v(n);
    for(int &i:v)cin>>i;
    /*auto cmp = [&](auto a, auto b) -> bool{
        return a>b;
    };*/
    deque<int>dq;
    sort(v.begin(), v.end());
    for(auto i:v)dq.push_back(i);
    int ans = 0;
    while(!dq.empty()){
        if(dq.size()>1 && dq.front() + dq.back() <= x){
            dq.pop_front();
            dq.pop_back();
        }
        else{
            dq.pop_back();
        }
        ans++;
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