#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    vector<int>v(n);
    for(auto &i:v)cin>>i;
    sort(v.begin(), v.end());
    int k;cin>>k;
    auto f = [&]() -> auto{
        int bud;cin>>bud;
        int ans = upper_bound(v.begin(), v.end(), bud) - v.begin();
        cout<<ans<<'\n';
        /* binary search
        int l = 0, r = n;
        while(l<r){
            int mid = l+(r-l)/2;
            if(v[mid] <= bud){
                l = mid+1;
            }
            else{
                r = mid;
            }
        }
        cout<<(v[0] <= bud ? l : 0)<<'\n';
        */
        return;
    };

    while(k--)f();

}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}