#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int a, b;
    while(cin>>a>>b){
        cout<<a<<" "<<b;
        if(a>b)swap(a, b);
        map<int, int>mp;
        int ans = 0;

        auto build = [&](int num) -> void{
            int cnt = 1;
            int ori = num;
            while(num != 1){
                ((num % 2 )== 1)? (num*=3, num++) : num/=2;
                cnt++;
            }
            mp[ori] = cnt;
            return;
        };

        for(int i=a;i<=b;i++){
            if(mp.find(i) == mp.end()){
                build(i);
            }
            
            ans = max(ans, mp[i]);
        }
        cout<<" "<<ans<<"\n";
    }
}

signed main(){
    solve();
    return 0;
}