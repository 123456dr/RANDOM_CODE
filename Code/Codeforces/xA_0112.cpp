#include<bits/stdc++.h>
using namespace std;
#define int long long

vector<int>v = {4, 7, 44, 77, 47, 74, 444, 777, 474, 747, 447, 477, 744, 774};

void solve(){
    int n;cin>>n;
    int ans = 0;
    for(int i:v){
        if(n % i == 0){
            ans = 1;
            break;
        }
    }
    cout<< (ans ? "YES" : "NO");
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    return 0;
}