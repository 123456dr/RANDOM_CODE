#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    string s;cin>>s;
    s[0] = toupper(s[0]);
    cout<<s;
    /*
    int t = 1;
    for(auto i:s){
        if(t){
            t=0;
            cout<<(char)toupper(i);
        }
        else cout<<i;
    }
    */
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}