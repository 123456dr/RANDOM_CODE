// https://codeforces.com/contest/22/problem/A
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int n;cin>>n;
    set<int>st;
    while(n--){
        int x;cin>>x;
        st.insert(x);
    }
    if(st.size()>=2){
        cout<<*(++st.begin())<<endl;
    }
    else cout<<"NO"<<endl;

    return 0;
}