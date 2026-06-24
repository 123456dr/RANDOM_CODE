// https://codeforces.com/contest/27/problem/A
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    priority_queue<int, vector<int>, greater<int>>pq;
    while(n--){
        int x;cin>>x;
        pq.push(x);
    }
    int id = 1;
    while(1 && !pq.empty()){
        int x = pq.top();
        pq.pop();
        if(id != x){
            cout<<id;
            return;
        }
        id++;
    }
    cout<<id;
    return;
}


signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}