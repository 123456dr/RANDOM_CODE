// https://codeforces.com/gym/106084/problem/A
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int x, d;
    while (cin>>x>>d){
        if(x*2<=d)cout<<"double it";
        else cout<<"take it";
        cout<<"\n";
    }
    
    
    return 0;
}