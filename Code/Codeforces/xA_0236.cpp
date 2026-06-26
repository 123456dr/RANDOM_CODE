#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    string s;cin>>s;
    set<int>st;
    for(auto i:s){
        st.insert(i);
    }
    cout<<(st.size() % 2 == 0 ? "CHAT WITH HER!" : "IGNORE HIM!");
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}