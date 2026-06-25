//https://codeforces.com/contest/2232/problem/A
#include<bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    int n;
    cin>>n;
    while(n--){
        int t;cin>>t;
        vector<int>v(t);
        for(auto &i:v){
            cin>>i;
        }
        sort(v.begin(), v.end());
        int L=0, R=0;
        for(auto i:v){
            if(i<v[t/2])L++;
            if(i>v[t/2])R++;
        }
        cout<<max(L,R)<<endl;
    }

    return 0;
}