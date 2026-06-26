// https://codeforces.com/problemset/problem/112/A

#include <bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    string a, b;
    cin>>a>>b;
    int sz = a.length();
    int ans = 0;
    for(int i=0;i<sz;i++){
        int cal = a[i] - b[i];
        if(!(abs(cal) == 32 || cal == 0)){
            if(toupper(a[i]) - toupper(b[i]) > 0)ans++;
            else ans--;
            break;
        }
    }
    cout<<(ans > 0 ? 1 : ans < 0 ? -1 : 0);
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}