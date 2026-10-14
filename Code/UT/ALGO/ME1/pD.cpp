// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;
    while(cin>>n && n){
        map<string, int>mp;
        for(int i=0;i<n;i++){
            string s;int x;
            cin>>s>>x;
            mp[s] = x;
        }
        map<string, vector<string>>val;
        set<string>st;
        for(int i=0;i<n-1;i++){
            string a, b;
            cin>>a>>b;
            val[a].push_back(b);
            st.insert(b);
        }
        string root;
        for(auto i:mp){
            if(st.find(i.first) == st.end()){
                root = i.first;
                break;
            }
        }
        auto dfs = [&](auto &self, string s) -> pair<int, int>{
            int take = mp[s];
            int ntake = 0;
            for(auto i:val[s]){
                auto [dtake, dntake] = self(self, i);
                take += dntake;
                ntake += max(dtake, dntake);
            }
            return {take, ntake};
        };
        auto [a, b] = dfs(dfs, root);
        cout<<max(a, b)<<endl;
    }  
    
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}

/*// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int n;
    while(cin>>n && n){
    map<string, vector<string>> mp;
    map<string, int>val;
    for(int i=0;i<n;i++){
        string x;int y;
        cin>>x>>y;
        val[x] = y;
    }
    set<string>nroot;
    for(int i=0;i<n-1;i++){
        string x, y;
        cin>>x>>y;
        mp[x].push_back(y);
        nroot.insert(y);
    }
    string rot;
    for(auto i:val){
        if(nroot.find(i.first) == nroot.end()){
            rot = i.first;
            break;
        }
    }

    auto dfs = [&](auto &self, string r) -> pair<int, int>{
        int rskip = 0;
        int rtake = val[r];
        for(auto i:mp[r]){
            auto [cskip, ctake] = self(self, i);
            rskip += max(cskip, ctake);
            rtake += cskip;
        }
        return {rskip, rtake};

    };
    auto [a, b] = dfs(dfs, rot);
    cout<<max(a, b)<<endl;
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}*/