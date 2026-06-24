// https://codeforces.com/problemset/problem/266/B
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, t;cin>>n>>t;
    string s;cin>>s;
    while(t--){
        string ans = "";
        int sz = s.length();
        for(int i=1;i<sz;i++){
            if(s[i-1] == 'B' && s[i] == 'G'){
                ans+="GB";
                i++;
            }
            else ans+=s[i-1];
        }
        if(sz > ans.length())ans+=s[sz-1];
        s.swap(ans);
    }
    cout<<s;
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}