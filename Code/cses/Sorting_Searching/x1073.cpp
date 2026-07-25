// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    multiset<int>mst;
    int ans = 0;
    while(n--){
        int x;cin>>x;
        auto it = mst.upper_bound(x);
        if(it != mst.end()){
            mst.erase(it);
            mst.insert(x);
        }
        else{
            mst.insert(x);
            ans++;
        }
    }
    cout<<ans;
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}