// https://codeforces.com/gym/106084/problem/D
/*
- 遍歷可能的長度2~n
- 紀錄各種長度下區間 DP

區間 DP => dp[i][j]最少需要改動幾次
- dp[0][0] = 0
- dp[i][j] 
    - 如果字母i == 字母j => dp[i][j] = 0
    - 否則 dp[i][j] = min(1+dp[i][j-1]刪右, 1+dp[i+1][j]刪左, dp[i+1][j-1]替換 也就是強迫改成i, j一樣)
*/
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int n;cin>>n;
    while (n--){
        string s;cin>>s;
        int sz = s.length();
        vector<vector<int>>dp(sz+2, vector<int>(sz+2, 0));
        for(int len=2;len<=sz;len++){
            for(int i=0;i+len<=sz;i++){
                int j = i+len-1;
                if(s[i] == s[j])dp[i][j] = dp[i+1][j-1];
                else dp[i][j] = min(1 + dp[i][j-1], min(1 + dp[i+1][j], 1 + dp[i+1][j-1]));
            }
        }
        cout<<dp[0][sz-1]<<"\n";
    }
    
    
    return 0;
}