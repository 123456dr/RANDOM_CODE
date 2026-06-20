// https://codeforces.com/gym/106084/problem/B
#include <bits/stdc++.h>
using namespace std;
#define int long long

int ck(int num){
    if(num<=1)return 0;
    if(num%2 == 0)return 0;

    for(int i=3;i*i<=num;i++){
        if(num%i == 0)return 0;
    }
    return 1;
}

signed main(){
    int t;cin>>t;
    while(t--){
        int a, b;cin>>a>>b;
        if(abs(a-b) == 2 && ck(a) && ck(b))cout<<"Y";
        else cout<<"N";

        cout<<"\n";
    }
    
    
    return 0;
}