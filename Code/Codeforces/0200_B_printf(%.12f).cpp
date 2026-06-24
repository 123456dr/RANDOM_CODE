// https://codeforces.com/problemset/problem/200/B
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    int N = n;
    double sum = 0.0;
    while(n--){
        double x;cin>>x;
        sum += x*0.01;
    }
    printf("%.12f",sum * 100/(double)N);
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}