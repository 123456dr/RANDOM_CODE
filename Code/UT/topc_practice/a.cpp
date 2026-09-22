#include<bits/stdc++.h>
using namespace std;
#define int long long


signed main(){
    int t;cin>>t;
    vector<int>prime(1e6+5, 1);
    prime[0] = 0, prime[1] = 0;
    for(int i=2;i<1e6+5;i++){
        if(prime[i] == 1){
            for(int j=i+i;j<1e6+5;j+=i){
                prime[j] = 0;
            }
        }
    }

    auto solve = [&]() -> void{
        int a, b;
        cin>>a>>b;
        if(a + 2 == b && prime[a] == prime[b] && prime[a] == 1){
            cout<<"Y\n";
        }
        else cout<<"N\n";
    };
    while(t--)solve();

    return 0;
}