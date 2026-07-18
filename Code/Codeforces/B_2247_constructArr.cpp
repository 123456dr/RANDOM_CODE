// https://codeforces.com/contest/2247/problem/B
/*
模擬長度1~k並且透過前綴和建立V陣列每項元素值等於pref[x] % m，
如果模擬時出現v[r]-v[l-1] == 0就NO
- 也就是 V 中不能有連續 1~K 個相同，也就是[完全不]連續相同
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, m, k;cin>>n>>k>>m;
    if(k > m){
        cout << "NO\n";
        return;
    }
    /*vector<int>pref(n+1, 0);
    vector<int>v(n, 0);
    int tt = 1;
    for(int i=1;i<=n;i++){
        int x;cin>>x;
        pref[i] = pref[i-1] + x;
        v[i-1] = pref[i] % m;
        if(i != 1 && (v[i] == v[i-1])){
            tt = 0;
        }
    }
    if(tt == 0){cout<<"NO\n";return;}
    */
    int id = 1;
    cout<<"YES\n";
    while(n--){
        if(id++ % k == 0){
            cout<<m - k + 1<<" ";
        }
        else{
            cout<<1<<" ";
        }
    }
    cout<<'\n';
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}