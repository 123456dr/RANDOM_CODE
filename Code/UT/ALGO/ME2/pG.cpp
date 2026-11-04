// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    string s;cin>>s;
    int ans = 0;
    int sf = 0;
    while(!s.empty()){
        int num = 0;
        stack<int>st;
        for(int i=0;i<3 && !s.empty();i++){
            char c = s.back();
            s.pop_back();
            st.push(c - '0');
        }
        while(!st.empty()){
            num *= 10;
            num += st.top();
            st.pop();
        }
        //cout<<num<<" ";
        if(!sf)ans+=num;
        else ans-=num;
        sf++;
        sf%=2;
    }
    cout<<abs(ans)<<" ";
    if(ans % 13 == 0){
        cout<<"YES\n";
    }
    else cout<<"NO\n";
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    cin>>t;
    while(t--)solve();
    return 0;
}