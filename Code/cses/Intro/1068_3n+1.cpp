#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    while(n != 1){
        cout<<n<<" ";
        if(n & 1)n *= 3, n++;
        else n/=2;
    }
    cout<<1;
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}