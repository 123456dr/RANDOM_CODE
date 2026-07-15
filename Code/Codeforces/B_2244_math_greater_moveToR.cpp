// https://codeforces.com/contest/2244/problem/B
/*
必須建造嚴格遞增的陣列，並且每次只能把該堆書拿到右邊堆
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    int sum = 0;
    int ans = 1;
    for(int i=0;i<n;i++){
        int x;cin>>x;
        sum += (x-(i+1));
        if (sum<0){
            ans = 0;
        }
    }
    cout<<(ans ? "YES\n" : "NO\n");
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}