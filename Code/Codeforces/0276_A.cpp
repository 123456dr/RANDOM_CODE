// https://codeforces.com/contest/276/problem/A
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    int n,k;cin>>n>>k;
    int mx = -1e10;
    while(n--){
        int f, t;
        cin>>f>>t;
        if(t>k)mx = max(mx, f-(t-k));
        else mx = max(mx, f);
    }
    cout<<mx;

    return 0;
}
