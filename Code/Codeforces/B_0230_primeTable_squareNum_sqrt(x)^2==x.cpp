/*
完全平方數並且剛好只有三個相異因數，只要檢查到sqrt(1e12) = O(1e6) => okk
*/
#include<bits/stdc++.h>
using namespace std;
#define int long long

vector<int>prime(1e6+5, 1);
void bprime(){
    prime[0] = 0;
    prime[1] = 0;
    for(int i = 2;i<1e6+5;i++){
        if(prime[i] == 1){
            for(int j=i+i;j<1e6+5;j+=i){
                prime[j] = 0;
            }
        }
    }
}

void solve(){
    int x;
    cin>>x;
    int k = sqrt(x);
    if(k*k == x && prime[k]){
        cout<<"YES";
    }
    else cout<<"NO";
    cout<<"\n";
    return;
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;cin>>t;
    bprime();
    while(t--)solve();
    return 0;
}