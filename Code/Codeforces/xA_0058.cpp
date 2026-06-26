#include<bits/stdc++.h>
using namespace std;
#define int long long

vector<char>v = {'h','e', 'l', 'l', 'o'};
void solve(){
    string s;cin>>s;
    int id = 0;
    int sz = s.length();
    int i=0;
    while(id < 5 && i<sz){
        if(s[i] == v[id])id++;
        i++;
    }
    if(id >= 5){
        cout<<"YES";
        return;
    }
    cout<<"NO";
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}