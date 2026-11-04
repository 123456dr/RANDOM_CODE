// 
#include<bits/stdc++.h>
using namespace std;
#define int long long

void solve(){
    int t;cin>>t;
    int N = t;
    while(t--){
        int n, m, a, b;
        cin>>n>>m>>a>>b;
        vector<vector<char>>v(n, vector<char>(m, '0'));
        deque<pair<int, int>>vp;
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                char x;cin>>x;
                if(x == 'V')vp.push_back({i, j}), v[i][j] = 'V';
            }
        }
        while(!vp.empty()){
            auto [x, y] = vp.back();
            vp.pop_back();
            v[x][y] = 'V';
            if(x - 1 >= 0){
                if(y - 1 >= 0 && v[x-1][y-1] != 'V' && v[x-1][y-1] != char('0'+a))v[x-1][y-1] = char('0'+b);
                if(y + 1 <m && v[x-1][y+1] != 'V' && v[x-1][y+1] != char('0'+a))v[x-1][y+1] = char('0'+b);
                if(v[x-1][y] != 'V')v[x-1][y] = char('0'+a);
            }
            if(y - 1 >= 0 && v[x][y-1] != 'V')v[x][y-1] = char('0'+a);
            if(y + 1 < m && v[x][y+1] != 'V')v[x][y+1] = char('0'+a);
            if(x+1 < n){
                if(y-1 >= 0 && v[x+1][y-1] != 'V' && v[x+1][y-1] != char('0'+a))v[x+1][y-1] = char('0'+b);
                if(y+1 < m && v[x+1][y+1] != 'V' && v[x+1][y+1] != char('0'+a))v[x+1][y+1] = char('0'+b);
                if(v[x+1][y] != 'V')v[x+1][y] = char('0'+a);
            }
        }
        cout<<"Airplane #"<<N-t<<":\n";
        for(auto i:v){
            for(auto j:i){
                cout<<j;
            }cout<<endl;
        }
    }
}

signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);int t = 1;
    //cin>>t;
    while(t--)solve();
    return 0;
}