// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, p;
    while(cin>>n>>p){
        vector<int>bl(n);
        vector<int>po(p);
        int mx = 0;
        for(auto &i:bl)cin>>i, mx = max(mx, i);
        for(auto &i:po)cin>>i;

        int l = 0, r = mx;
        int ans = 0;
        while(l <= r){
            int mid = l + (r - l)/2;
            int ind = 0;
            int cnt = 0;
            for(int i = 0;i<n;i++){
                if(mid <= bl[i]){
                    cnt++;
                }
                else {
                    cnt = 0;
                }
                if(cnt >= po[ind]){
                    while(ind < p && cnt >= po[ind])cnt-=po[ind++];
                    if(ind == p)break;
                    cnt = 0;
                }
            }
            if(ind == p){
                ans = mid;
                l = mid+1;
            }
            else{
                r = mid-1;
            }
        }
        cout<<ans<<endl;
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}

/*#include<bits/stdc++.h>
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
    */