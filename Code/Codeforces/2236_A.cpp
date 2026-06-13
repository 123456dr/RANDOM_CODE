#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    int t;cin>>t;
    while(t--){
        int x;cin>>x;
        int mx = 0, mn = 1e9;;
        while(x--){
            int temp;
            cin>>temp;
            mx = max(mx, temp);
            mn = min(mn, temp);
        }
        cout<<mx+1-mn<<endl;
    }

    return 0;
}