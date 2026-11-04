// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int w, n;
    cin>>w>>n;    
    int mod = (1e9+7);
    string s;getline(cin, s);
    vector<vector<int>>dp(w+1, vector<int>(n+1, 0));
    for(int i=0;i<w;i++){
        getline(cin, s);
        stringstream ss(s);
        int a, b;ss>>a;
        while(ss >> b){
            dp[a][b] = -1;
        }
    }
    for(int i=1;i<=w;i++){
        for(int j=1;j<=n;j++){
            if(dp[i][j] == -1)continue;
            if(i == 1 && j == 1){dp[i][j] = 1;continue;}
            if(dp[i-1][j] != -1)dp[i][j] += dp[i-1][j];
            if(dp[i][j-1] != -1)dp[i][j] += dp[i][j-1];
            dp[i][j] %= mod;
        }
    }
    cout<<max(dp[w][n], 0LL)<<endl;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}