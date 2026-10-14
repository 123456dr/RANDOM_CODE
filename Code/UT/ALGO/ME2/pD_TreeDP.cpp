// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

vector<int>isP;
vector<int>notP(1e5+5, 0);
void build_notP(){
    notP[0] = notP[1] = 1;
    for(int i=2;i<1e5+4;i++){
        if(notP[i] == 0){
            isP.push_back(i);
            for(int j=i+i;j<1e5+4;j+=i){
                notP[j] = 1;
            }
        }
    }
}

int check(int num){
    if(num < 2)return false;
    for(int i : isP){
        if(i * i > num)break;
        if(num % i == 0) return 0;
    }
    return 1;
}

void solve(){
    int n;
    while(cin>>n){
        if(n % 2 == 1){
            if(n - 2 > 2 && check(n-2)){
                cout<<n<<" is the sum of 2 and "<<n-2<<".\n";
            }
            else{
                cout<<n<<" is not the sum of two primes!\n";
            }
        }
        else{
            int tt = 0;
            int i = n/2;
            if(i % 2 == 0)i--;
            else i -= 2;
            for(i;i>2;i-=2){
                if(check(i) && check(n-i)){cout<<n<<" is the sum of "<<min(i, n-i)<<" and "<<max(i, n-i)<<".\n";tt = 1;break;}
            }
            if(!tt)cout<<n<<" is not the sum of two primes!\n";
        }
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    build_notP();
    while(t--)solve();
    return 0;
}