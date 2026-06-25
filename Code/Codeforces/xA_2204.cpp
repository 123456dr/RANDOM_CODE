// https://codeforces.com/contest/2204/problem/A
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    int t;cin>>t;
    while(t--){
        int n;cin>>n;
        string s;cin>>s;
        int ans = 0;
        int ind = 0;
        while(n-- && ind>=0){
            if(s[ind] == 'R')ind++;
            else ind--;
            ans = max(ans, ind);
        }
        cout<<ans+1<<endl;
    }

    return 0;
}