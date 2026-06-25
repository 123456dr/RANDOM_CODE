// https://codeforces.com/contest/2236/problem/C
// F2改檔名 & ctrl+B關側目錄
/* 
[數學邏輯題目]
先除再加一定為最少次數，紀錄每次A/x和B/x，求最佳交會點V=max(A/x/x..., B/x/x...)
ans = [A/x/x...的次數] + [B/x/x...的次數] + [V-A/x/x...] + [V-B/x/x...]
*/

#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    int t;cin>>t;
    while(t--){
        int a, b, x;
        cin>>a>>b>>x;
        int ans = 1e18;
        int at = 0, bt = 0;
        while(a>=0){
            int tb = b;
            bt = 0;
            while(tb>=0){
                int V = max(a, tb);
                ans = min(ans, at+bt+(V-a)+(V-tb));
                if(tb == 0 || x == 0)break;
                tb/=x;bt++;
            }
            if(a == 0 || x == 0)break;
            a/=x;at++;
        }
        cout<<ans<<endl;
    }
    return 0;
}
