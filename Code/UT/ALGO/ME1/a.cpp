#include <bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;
    while(cin>>n){
        vector<int>arr(n);
        for(auto &i:arr)cin>>i;
        auto m = [&](int l, int mid, int r) -> void{
            vector<int>larr(mid-l+1), rarr(r-mid);
            for(int i=0;i<(mid-l+1);i++)larr[i] = arr[l+i];
            for(int i=0;i<(r-mid);i++)rarr[i] = arr[mid+i+1];

            int ln = mid-l+1, rn = r-mid;
            int ll = 0, rr = 0; 
            int k = l;
            while(ll < ln && rr < rn){
                if(larr[ll] < rarr[rr]){
                    arr[k++] = larr[ll++];
                }
                else arr[k++] = rarr[rr++];
            }
            for(int i=ll;i<ln;i++)arr[k++] = larr[i];
            for(int i=rr;i<rn;i++)arr[k++] = rarr[i];
            for(auto i:arr)cout<<i<<" ";
            cout<<"\n";
            return;
        };

        auto ms = [&](auto &self, int l, int r) -> void{
            if(l >= r)return;
            int mid = l + (r-l)/2;
            self(self, l, mid);
            self(self, mid+1, r);

            m(l, mid, r);
        };
        ms(ms, 0, n-1);
    }
}

signed main(){
    solve();
    return 0;
}
