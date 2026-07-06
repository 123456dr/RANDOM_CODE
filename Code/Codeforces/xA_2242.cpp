// https://codeforces.com/contest/2242/A
/*
- 一種字母數量大於等於3 => xxx
- 兩種字母數量大於等於2 => ABxAB
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    int cnt2 = 0, cnt3 = 0;
    while(n--){
        int x;cin>>x;
        if(x>=3)cnt3++;
        if(x>=2)cnt2++;
    }
    cout<<(cnt2>=2 || cnt3 ? "YES" : "NO");
    cout<<"\n";
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}