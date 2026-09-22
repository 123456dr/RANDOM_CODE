#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, m;
    while(cin>>n>>m){
        vector<int>w(n), p(m);
        int l = 0, r = 0;
        for(auto &i:w)cin>>i, r = max(r, i);
        for(auto &i:p)cin>>i;
        
        auto check = [&](int h) -> int{
            int cnt = 0;
            int ind = 0;
            for(auto i:w){
                if(i >= h){
                    cnt++;
                }
                else{
                    while(1){
                        if(ind >= m)return 1;
                        if(p[ind] <= cnt){
                            cnt -= p[ind++];
                        }
                        else break;
                    }
                    cnt = 0;
                }
            }
            while(1){
                if(ind >= m)return 1;
                if(p[ind] <= cnt){
                    cnt -= p[ind++];
                }
                else break;
            }
            if(ind >= m)return 1;
            else return 0;
        };

        int ans = 0;
        while(l<=r){
            int mid = l + (r-l)/2;
            if(check(mid)){
                ans = mid;
                l = mid+1;
            }
            else r = mid-1;
        }
        cout<<ans<<"\n";
    }
}


signed main(){
    solve();
    return 0;
}