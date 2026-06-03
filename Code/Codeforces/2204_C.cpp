// https://codeforces.com/contest/2204/problem/C
// 5m
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define gcd lcm

signed main(){

    int t;cin>>t;
    while(t--){
        int a,b,c,m;
        cin>>a>>b>>c>>m;
        int Ca = m/a, Cb = m/b, Cc = m/c, Cab = m/gcd(a,b), Cac = m/gcd(a,c), Cbc = m/gcd(b,c), Cabc = m/gcd(a,gcd(b,c));
        cout<<6*(Ca-Cab-Cac+Cabc)+3*(Cab+Cac-2*Cabc)+2*(Cabc)<<" "<<6*(Cb-Cab-Cbc+Cabc)+3*(Cab+Cbc-2*Cabc)+2*(Cabc)<<" "<<6*(Cc-Cac-Cbc+Cabc)+3*(Cac+Cbc-2*Cabc)+2*(Cabc)<<endl;
    }

    return 0;
}