// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

vector<int>isP(2002, 1);

void build_isP(){
    isP[1] = 0;//cout<<isP[1];
    for(int i=2;i<=2001;i++){
        for(int j=i+i;j<=2001;j+=i){
            isP[j] = 0;
        }
    }
}

void solve(){
    int n;cin>>n;
    int N = n;
    while(n--){
        cout<<"Case "<<N-n<<": ";
        string s;cin>>s;
        map<char, int>mp;
        for(auto i:s){
            mp[i]++;
        }
        int tt = 0;
        for(auto i:mp){
            if(isP[i.second] == 1){
                cout<<i.first;//<<":"<<i.second<<"  ";
                tt = 1;
            }
        }
        if(tt == 0)cout<<"empty";
        cout<<endl;
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    build_isP();
    while(t--)solve();
    return 0;
}