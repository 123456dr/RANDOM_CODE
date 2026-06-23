// https://codeforces.com/problemset/problem/231/A

#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int t;cin>>t;
    int ans = 0;
    int cul = 0;
    for(int i=0;i<3*t;i++){
        int x;cin>>x;
        cul += x;
        if(i%3 == 2){
            if(cul >= 2)ans++;
            cul = 0;
        }
    }
    
    cout<<ans;
}


signed main(){
    
    solve();
    cout<<"\n";

    return 0;
}