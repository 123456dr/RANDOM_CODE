// https://codeforces.com/problemset/problem/371/C
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    string s;cin>>s;
    int na, nb, nc, pa, pb, pc;
    cin>>na>>nb>>nc>>pa>>pb>>pc;
    int bud;cin>>bud;
    map<char, int>mp = {{'B', 0}, {'S', 0}, {'C', 0}};
    for(auto i:s)mp[i]++;
    
    int l = 0, r = 2e12;
    int ans = 0;
    while(l < r){
        int mid = l + (r-l)/2;
        int ra = max(0LL, mp['B'] * mid - na);
        int rb = max(0LL, mp['S'] * mid - nb);
        int rc = max(0LL, mp['C'] * mid - nc);
        int spend = ra * pa + rb * pb + rc * pc;
        if(spend <= bud){
            ans = mid;
            l = mid + 1;
        }
        else r = mid;
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