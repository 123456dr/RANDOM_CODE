// https://codeforces.com/contest/27/problem/A
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int n;cin>>n;
    vector<int>v;
    while(n--){
        int x;cin>>x;
        v.push_back(x);
    }
    sort(v.begin(),v.end());
    int ans =1;
    for(auto i:v){
        if(i==ans)ans++;
        else {
            cout<<ans<<endl;
            return 0;
        }
    }
    return 0;
}