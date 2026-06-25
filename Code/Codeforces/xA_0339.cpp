// https://codeforces.com/problemset/problem/339/A
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    string s;cin>>s;
    int cont = 1;
    vector<int>v;
    for(auto i:s){
        if(i == '+')cont++;
        else{
            v.push_back(i-'0');
        }
    }
    sort(v.begin(), v.end());
    int head = 0;
    for(auto i:v){
        if(!head)head = 1;
        else cout<<"+";
        cout<<i;
    }
    return 0;
}