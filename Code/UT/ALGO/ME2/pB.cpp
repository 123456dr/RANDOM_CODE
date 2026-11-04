// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

vector<int>isp(37, 1);
void build_p(){
    isp[1] = 0;
    for(int i=2;i<=6;i++){
        for(int j=i+i;j<=36;j+=i){
            isp[j] = 0;
        }
    }
}

void solve(){
    int n;
    int t = 1;
    while(cin>>n){
        cout<<"Case "<<t++<<":\n";
        vector<int>vis(n+1, 0);
        auto dfs = [&](auto &self, deque<int>dq, vector<int>vis) -> void{
            if(dq.size() == n){
                if(isp[dq.back() + 1] == 1){
                    while(!dq.empty()){
                        cout<<dq.front()<<" ";
                        dq.pop_front();
                    }
                    cout<<endl;
                }
                return;
            }
            for(int i=2;i<=n;i++){
                if(vis[i] == 0 && !dq.empty() && isp[dq.back() + i] == 1){
                    dq.push_back(i);
                    vis[i] = 1;
                    self(self, dq, vis);
                    dq.pop_back();
                    vis[i] = 0;
                }
            }
            return;
        };
        vis[1] = 1;
        deque<int>dq;
        dq.push_back(1);
        dfs(dfs, dq, vis);
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    build_p();
    while(t--)solve();
    return 0;
}

/*
// gcd == Greatest Common Divisor
// lcm == Least Common Multiple
#include<bits/stdc++.h>
using namespace std;
#define int long long

vector<int>isP(36, 1);
void build_isP(){
    for(int i = 2;i<6;i++){
        if(isP[i])
        for(int j = i+i;j<36;j+=i){
            isP[j] = 0;
        }
    }
    return;
}

void solve(){
    int t=1, n;
    while(cin>>n){
    cout<<"Case "<<t++<<":\n";
    auto check = [&](int a, int b) -> int{
        if(isP[a + b] == 1)return 1;
        else return 0;
    };
    auto dfs = [&](auto &self, vector<int>vis, vector<int>rem) -> void{
        if(vis.size() == n){
            for(auto i:vis)cout<<i<<" ";
            cout<<endl;
            return;
        }
        if(vis.size() == n-1){
            if(check(rem[0], vis[0]) != 1)return;
        }
        for(int i = 0;i<rem.size();i++){
            if(check(rem[i], vis.back()) == 1){
                vis.push_back(rem[i]);
                vector<int>backup;
                for(auto i:rem)backup.push_back(i);
                rem.erase(rem.begin()+i);
                self(self, vis, rem);
                vis.pop_back();
                rem.resize(0);
                for(auto i:backup)rem.push_back(i);
            }
        }
        return;
    };
    vector<int>tmp(n-1);
    int ind = 2;
    for(auto &i:tmp) i = ind++;
    dfs(dfs, {1}, tmp);
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);//int t = 1;
    //cin>>t;int T = t;
    //while(t--)
    build_isP();
    solve();
    return 0;
}
*/