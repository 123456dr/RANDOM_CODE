// https://cses.fi/problemset/task/1640
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n, x;cin>>n>>x;
    map<int, int>mp;
    int N = n;
    while(n--){
        int k;cin>>k;
        if(mp.find(x - k) != mp.end()){
            cout<<mp[x - k]<<" "<<N-n;
            return;
        }
        else{
            mp[k] = N - n;
        }
    }
    cout<<"IMPOSSIBLE";
    return;
}
/*
void solve(){
    int n, x;cin>>n>>x;
    unordered_map<int, int>mp;
    unordered_map<int, int>freq;
    int N = n;
    while(n--){
        int k;cin>>k;
        if(mp.find(k) != mp.end())freq[k] = mp[k];
        mp[k] = N-n;
    }
    for(auto i:mp){
        if(mp.find(x - i.first) != mp.end()){
            if(mp[x - i.first] == mp[i.first] && freq.find(i.first) != freq.end())cout<<freq[i.first]<<" "<<mp[i.first];
            else if(mp[x - i.first] != mp[i.first])cout<<mp[x - i.first]<<" "<<mp[i.first];
            else continue;
            return;
        }
    }
    cout<<"IMPOSSIBLE";
    return;
}*/

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}