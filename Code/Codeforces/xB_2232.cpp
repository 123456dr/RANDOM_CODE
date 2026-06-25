//https://codeforces.com/contest/2232/problem/B
#include<bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    int n;
    cin>>n;
    while(n--){
        int t;
        cin>>t;
        vector<int>v(t,0);
        for(auto &i:v)cin>>i;
        int ans = 1e9;
        int sum = 0;
        for(int i=0;i<t;i++){
            sum+=v[i];
            ans = min(ans,sum/(i+1));
            cout<<ans<<" ";
        }
        cout<<endl;
    }

    return 0;
}
