#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    string s;
    cin>>s;
    int ok = 1;
    int sz = s.length();
    for(int i=1;i<sz;i++){
        isupper(s[i]) ? ok = 1 : ok = 0;
        if(!ok)break;
    }
    if(ok){
        if(isupper(s[0]))cout<<(char)tolower(s[0]);
        else cout<<(char)toupper(s[0]);
        for(int i=1;i<sz;i++){
            cout<<(isupper(s[i]) ? (char)tolower(s[i]) : (char)toupper(s[i]));
        }
    }
    else cout<<s;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}