#include<bits/stdc++.h>
using namespace std;
#define int long long
int MOD = 1e9+7;

int power(int base, int exp) {
    int res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}

void solve(){
    int n;cin>>n;
    vector<int>v(n);
    int cnt1 = -1;
    for(int i=0;i<n;i++){cin>>v[i];if(v[i]!=-1 && cnt1==-1)cnt1 = i;}

    cnt1 = (cnt1 == -1) ? n : cnt1; 
    int num = n - cnt1; //灰零個數
    int d = 0; // 異數量      
    int k = 0; // 對數量     

    if (num > 0) {
        d = 1; 
        for (int i = cnt1 + 1; i < n; i++) {
            if (v[i] != v[i-1]) {
                d++;
                if (v[i] == v[i-1] + 1) k++;
            }
        }
    }

    int A = 0, B = 0;
    if (num > 0) {
        A = power(2, num - d);
        B = (k * A) % MOD;
    }
    else {
        A = 1; 
        B = 0; 
    }
    
    int e = (cnt1 == 0) ? 1 : power(2, cnt1 - 1);
    int odd  = (cnt1 == 0) ? 0 : power(2, cnt1 - 1);

    int ans = (e * A % MOD + odd * B % MOD) % MOD;
    cout<<ans<<'\n';
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}