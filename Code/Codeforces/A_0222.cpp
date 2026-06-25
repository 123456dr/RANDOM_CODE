// https://codeforces.com/contest/222/problem/A

/*
題目所求: 最少操作幾次後整串序列數字一樣
每次可以複製第k位到末端，並且刪除第一位數字
=> 如果第k到最後一位出現不一樣的數字則永遠不合法(會被複製)
=> 符合前項條件，則找數字第一個到第k-1間最後一個和k位後不一樣的數字位數(代表最少需要刪除幾次)
*/

#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int n, k;
    while(cin>>n>>k){
        vector<int>v(n);
        int same = 0;
        int tt = 1;
        for(int i=0;i<n;i++){
            cin>>v[i];
            if(i>=k-1){
                if(!same)same = v[i];
                else if(v[i] != same){
                    tt = 0;
                }
            }
        }
        if(!tt){cout<<"-1"<<endl; continue;}
        int ans = 0;
        for(int i=0;i<k-1;i++){
            if(v[i] != same)ans = i+1;
        }
        cout<<ans<<endl;
    }

    return 0;
}