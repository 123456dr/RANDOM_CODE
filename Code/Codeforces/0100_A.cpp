#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int n, k, n1;
    while(cin>>n>>k>>n1){
        if(n*n<=n1*n1*k)cout<<"YES";
        else cout<<"NO";
        cout<<endl;
    }
    return 0;
}