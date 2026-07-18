// https://codeforces.com/contest/2247/problem/C
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;cin>>n;
    int diff10 = 0, diff01 = 0, same11 = 0, same00 = 0;
    vector<int>v1(n);
    vector<int>v2(n);
    for(auto &i:v1)cin>>i;
    for(auto &i:v2)cin>>i;
    int N = n;
    while(n--){
        int a = v1[N-n-1], b = v2[N-n-1];
        if(a != b){
            if(a == 1)diff10++;
            else diff01++;
        }
        else{
            if(a == 1)same11++;
            else same00++;
        }
    }
    if(diff01 == diff10 && diff01 == 0){cout<<"0\n";return;}
    if((diff10 & 1)){cout<<"1\n";return;}
    if(diff10){cout<<"2\n";return;}
    if(same00 && same11){cout<<"2\n";return;}
    cout<<"-1\n";
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}