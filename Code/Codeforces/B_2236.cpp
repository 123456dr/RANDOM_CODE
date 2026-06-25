// https://codeforces.com/contest/2236/problem/B
// F2改檔名 & ctrl+B關側目錄
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    int t;cin>>t;
    while(t--){
        int sz, k;
        cin>>sz>>k;
        string s;cin>>s;
        vector<int>v(sz, 0);
        for(int i=0;i+k<sz;i++){
            if((v[i]%2 == 0 && s[i] == '0') || (v[i]%2!=0 && s[i] == '1'))continue;
            v[i]++;
            v[i+k]++;
        }
        int ans = 1;
        for(int i=0;i<sz;i++){//cout<<v[i]<<" ";
            if(v[i]%2 == 0 && s[i] == '1')ans = 0;
            if(v[i]%2 != 0 && s[i] == '0')ans = 0;
        }//cout<<endl;
        cout<<(ans == 1 ? "YES" : "NO")<<endl;
    }
    return 0;
}

/*
陣列 v 紀錄該字母位置被反轉過幾次
可被反轉條件為 index+k<sz 
- 若反轉次數為單數且字母為0則否
- 若反轉次數為偶數且字母為1則否
*/