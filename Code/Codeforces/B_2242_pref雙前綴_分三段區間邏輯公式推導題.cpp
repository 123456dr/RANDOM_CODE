// // https://codeforces.com/contest/2242/B
/*
前綴和嗎?
2個前綴和陣列分別記錄每個位置有多少個(1)/(1,2)，
- 第一階段如果當前累積長度>前綴(1)個數*2，就歸零長度並記錄截斷尾
- 第二階段如果當前累積長度>前綴(1,2)個數*2，就歸零長度並記錄截斷尾
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    vector<int>pref1(n+1, 0);
    vector<int>pref12(n+1, 0);
    vector<int>v(n);for(auto &i:v)cin>>i;
    for(int i=1;i<=n;i++){
        pref1[i] = pref1[i-1];
        pref12[i] = pref12[i-1];
        if(v[i-1] == 1)pref1[i]++, pref12[i]++;
        if(v[i-1] == 2)pref12[i]++;
    }

    int lmn = 1e9;
    for(int i=2;i<n;i++){
        if(pref1[i-1] * 2 >= i-1){
            lmn = min(lmn, pref12[i-1] * 2 - (i-1));
        }
        if(pref12[i] * 2 - i >= lmn){
            cout<<"YES\n";
            return;
        }
    }
    cout<<"NO\n";

}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}