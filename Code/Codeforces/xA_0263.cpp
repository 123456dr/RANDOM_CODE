// https://codeforces.com/problemset/problem/263/A
#include <bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    for(int i=0;i<25;i++){
        int x;cin>>x;
        if(x == 1){
            cout<<abs(i/5-2) + abs((i-i/5*5)-2);
            return;
        }
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}