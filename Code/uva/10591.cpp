// unordered_set 無序 & insert(x) & s.find() == s.end()判定未找到
// AC at ZERO Judge

#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int n;cin>>n;
    int N=n;
    while(n--){
        int sum = 0;
        int x;cin>>x;
        int X = x;
        unordered_set<int>v;
        int ans = 0;
        while(v.find(x) == v.end()){
            v.insert(x);
            sum = 0;
            while(x>0){
                sum+=(x%10)*(x%10);
                x/=10;
            }
            if(sum == 1){
                ans = 1;
                break;
            }
            x = sum;
        }
        if(ans)cout<<"Case #"<<N-n<<": "<<X<<" is a Happy number."<<endl;
        else cout<<"Case #"<<N-n<<": "<<X<<" is an Unhappy number."<<endl;
        
    }

    return 0;
}