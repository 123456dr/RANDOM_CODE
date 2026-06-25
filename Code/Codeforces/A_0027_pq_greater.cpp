// https://codeforces.com/contest/27/problem/A

/*
新思路:
其實當讀入的數字大於存在數字各數n者可以無視，因為未出現的數值一定會小於n，所以只要開計數陣列arr[n+1]預留index-1。

舊思路: 
priority_queue<int, vector<int>, greater<int>>pq, 預設是less<i
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    vector<int>cul(n+1+1, 0); // index-1和答案為n+1
    while(n--){
        int x;cin>>x;
        if(x <= n)cul[x] = 1;
    }
    for(auto i:cul){
        if(i == 0){
            cout<<i;
            return;
        }
    }
}

signed main(){
    solve();
    return 0;
}




/*
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
*/