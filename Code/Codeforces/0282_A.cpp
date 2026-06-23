// https://codeforces.com/problemset/problem/282/A
#include <bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int t;cin>>t;
    int ans = 0; 
    while(t--){
        string s;cin>>s;
        for(auto i:s){
            if(i == '+'){
                ans++;
                break;
            }
            else if(i == '-'){
                ans--;
                break;
            }
        }
    }
    cout<<ans;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}