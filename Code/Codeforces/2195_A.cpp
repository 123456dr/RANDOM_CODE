// https://codeforces.com/problemset/problem/2195/A
// 三元運算子
#include<bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    int t;cin>>t;
    while(t--){
        int n;cin>>n;
        int ans = 0;
        while(n--){
            int x;cin>>x;
            if(x == 67)ans=1;
        }
        cout<< (ans == 1 ? "YES" : "NO")<<endl;
    }

    return 0;
}