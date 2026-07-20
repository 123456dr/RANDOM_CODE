// https://codeforces.com/problemset/problem/466/C
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    vector<int>v(n);
    vector<int>pref;
    int sum = 0;
    for(auto &i:v)cin>>i, sum += i, pref.push_back(sum);
    if(sum % 3 != 0){cout<<"0";return;}
    int cnt = 0;
    int ans = 0;
    int k = (sum == 0 ? 0 :sum/3);
    for(int t = 0;t<n-1;t++){
        int i = pref[t];
        if(i == 2*k)ans += cnt;
        if(i == k)cnt++;
    }
    cout<<ans;
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}