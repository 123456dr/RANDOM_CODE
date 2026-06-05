// https://codeforces.com/contest/2204/problem/B
/*
數學(?)跳脫題
- [新]: 從左到右掃描若當前數字比前面最大值還大則一定會被輸出，第0項為一定會
- [舊]: 從右到左每次掃描更新當前長度O(n^2);
*/

#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    int t;cin>>t;
    while(t--){
        int n;cin>>n;
        vector<int>v(n);
        int cnt = 0;
        int mx = 0;
        for(int i=0;i<n;i++){
            cin>>v[i];
            if(mx<=v[i])mx = v[i],cnt++;
        }
        cout<<cnt<<endl;
    }

    return 0;
}
/*
signed main(){

    int t;cin>>t;
    while(t--){
        int n;cin>>n;
        vector<int>v(n);
        for(int &i:v)cin>>i;
        int sz = n-1;
        int cnt = 0;
        while(sz>=0){
            int mx = 0;
            int mxid = 0;
            for(int i=sz;i>=0;i--){
                if(v[i] > mx)mx = v[i], mxid = i;
            }
            cnt++;
            sz = mxid-1;
        }
        cout<<cnt<<endl;
    }

    return 0;
}*/