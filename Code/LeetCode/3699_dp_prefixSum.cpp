/*
嚴格交替轉為狀態動態規劃，先後利用前綴和與一維滾動排除時空的雙重爆炸（TLE/MLE），
最終透過鏡像對稱（reverse）與原地變數累加（curr）體會將重複狀態與記憶體配置徹底降維打擊的優化美學。

新:
狀態擴展 DP[length, value, type當前步和前一步比較大/小(嚴格交替)]
- dp 初始化: 長度2時，兩數字不同就符合嚴格交替 => dp[2, x, 0/1]
- 後續 dp 邏輯: 
    - 如果前者 type 為遞增1則當前處理的數字必須小於前者value 也就是有 前value-l 種選擇；否則有r-value種選擇
    - dp[len+1, value, abs(1-前type)] = 
        - 前type ==0, 加總 [i = 前value ~ r] => dp[len, ivalue, itype]
        - 前type ==1, 加總 [i = l ~ 前value] => dp[len, ivalue, itype]
- arr = move(next_arr) => O(1) [vs. arr = next_arr O(N)]

舊思路:
bFS 遍歷 l~r 個數字當開頭，遍歷 l~r 不等於前者的數字做組合，不合法就剪枝，當長度等於 n 就計數+1
*/

#define MOD (1e9+7)
#define ll long long
class Solution {
public:
    int zigZagArrays(int n, int l, int r) {
        r -= l;
        l = 0;
        //vector<vector<ll>> dp(r+1, vector<ll>(2));
        vector<ll>udp(r+1);
        vector<ll>ddp(r+1);
        vector<ll>uprefix(r+2, 0);
        vector<ll>dprefix(r+2, 0);
        vector<ll>next_udp(r+1);
        vector<ll>next_ddp(r+1);

        for(int i=l;i<=r;i++){
            ddp[i] = r-i;
            udp[i] = i-0;
        }

        for(int i=3;i<=n;i++){
            //vector<vector<ll>> prefix(r+2, vector<ll>(2, 0)); // 第0為0
            uprefix[0] = dprefix[0] = 0;

            for(int u=0;u<=r;u++){
                uprefix[u+1] = (uprefix[u] + udp[u]) % (ll)MOD;
                dprefix[u+1] = (dprefix[u] + ddp[u]) % (ll)MOD;
            }
                
            //vector<vector<ll>> next_dp(r+1, vector<ll>(2));
            
            for(int o=0;o<=r;o++){
                ll cal0 = MOD + uprefix[r+1] - uprefix[o+1]; // pre上一個大  // 因為index0為預設0, o+1為不含o
                ll cal1 = MOD + dprefix[o]; // pre上一個小    // 因為index0為預設0, 右借o去扣為不含o
                /*for(int u=0;u<=r;u++){
                    if(o == u)continue;
                    if(u>o)cal0 += dp[i-1][u][1];  // j[u][1] 上一個數比這個大
                    else cal1 += dp[i-1][u][0];
                }
                */
                next_ddp[o] = cal0 % (ll)MOD;
                next_udp[o] = cal1 % (ll)MOD;
            }
            udp.swap(next_udp);
            ddp.swap(next_ddp);
        }

        ll ans = 0;
        for(int i = 0;i<=r;i++){
            ans += (udp[i] % (ll)MOD + ddp[i] % (ll)MOD) % (ll)MOD;
        }
        return ans % (ll)MOD;
    }
};

/* 再次TLE: 未平面化(陣列們)
#define MOD (1e9+7)
#define ll long long
class Solution {
public:
    int zigZagArrays(int n, int l, int r) {
        r -= l;
        l = 0;
        vector<vector<ll>> dp(r+1, vector<ll>(2));

        for(int i=l;i<=r;i++){
            dp[i][0] = r-i;
            dp[i][1] = i-0;
        }

        for(int i=3;i<=n;i++){
            vector<vector<ll>> prefix(r+2, vector<ll>(2, 0)); // 第0為0
            for(int u=0;u<=r;u++){
                prefix[u+1][0] = (prefix[u][0] + dp[u][0]) % (ll)MOD;
                prefix[u+1][1] = (prefix[u][1] + dp[u][1]) % (ll)MOD;
            }
                
            vector<vector<ll>> next_dp(r+1, vector<ll>(2));
            for(int o=0;o<=r;o++){
                ll cal0 = MOD + prefix[r+1][1] - prefix[o+1][1]; // pre上一個大  // 因為index0為預設0, o+1為不含o
                ll cal1 = MOD + prefix[o][0]; // pre上一個小    // 因為index0為預設0, 右借o去扣為不含o
                /*for(int u=0;u<=r;u++){
                    if(o == u)continue;
                    if(u>o)cal0 += dp[i-1][u][1];  // j[u][1] 上一個數比這個大
                    else cal1 += dp[i-1][u][0];
                }
                * /
                next_dp[o][0] = cal0 % (ll)MOD;
                next_dp[o][1] = cal1 % (ll)MOD;
            }
            dp = move(next_dp);
        }

        ll ans = 0;
        for(int i = 0;i<=r;i++){
            ans += (dp[i][0] % (ll)MOD + dp[i][1] % (ll)MOD) % (ll)MOD;
        }
        return ans % (ll)MOD;
    }
};
*/

/* dp 未降維
#define MOD (1e9+7)
#define ll long long
class Solution {
public:
    int zigZagArrays(int n, int l, int r) {
        r -= l;
        l = 0;
        vector<vector<vector<ll>>> dp(n+1, vector<vector<ll>>(r+1, vector<ll>(2)));

        for(int i=l;i<=r;i++){
            dp[2][i][0] = r-i;
            dp[2][i][1] = i-0;
        }

        for(int i=3;i<=n;i++){
            vector<vector<ll>> prefix(r+2, vector<ll>(2, 0)); // 第0為0
            for(int u=0;u<=r;u++){
                prefix[u+1][0] = (prefix[u][0] + dp[i-1][u][0]) % (ll)MOD;
                prefix[u+1][1] = (prefix[u][1] + dp[i-1][u][1]) % (ll)MOD;
            }
            
            for(int o=0;o<=r;o++){
                ll cal0 = MOD + prefix[r+1][1] - prefix[o+1][1]; // pre上一個大  // 因為index0為預設0, o+1為不含o
                ll cal1 = MOD + prefix[o][0]; // pre上一個小    // 因為index0為預設0, 右借o去扣為不含o
                /*for(int u=0;u<=r;u++){
                    if(o == u)continue;
                    if(u>o)cal0 += dp[i-1][u][1];  // j[u][1] 上一個數比這個大
                    else cal1 += dp[i-1][u][0];
                }
                * /
                dp[i][o][0] = cal0 % (ll)MOD;
                dp[i][o][1] = cal1 % (ll)MOD;
            }
        }

        ll ans = 0;
        for(int i = 0;i<=r;i++){
            ans += (dp[n][i][0] % (ll)MOD + dp[n][i][1] % (ll)MOD) % (ll)MOD;
        }
        return ans % (ll)MOD;
    }
};
*/

/* 缺少 prefix sum 優化
#define MOD (1e9+7)
#define ll long long
class Solution {
public:
    int zigZagArrays(int n, int l, int r) {
        r -= l;
        l = 0;
        vector<vector<vector<ll>>> dp(n+1, vector<vector<ll>>(r+1, vector<ll>(2)));

        for(int i=l;i<=r;i++){
            dp[2][i][0] = r-i;
            dp[2][i][1] = i-0;
        }
        for(int i=3;i<=n;i++){
            for(int o=0;o<=r;o++){
                ll cal0 = 0; // 當前要新增的數比較小
                ll cal1 = 0; // ..大
                //for(auto j:dp[i-1]){
                    for(int u=0;u<=r;u++){ ==========================================> 可prefix sum
                        if(o == u)continue;
                        if(u>o)cal0 += dp[i-1][u][1];  // j[u][1] 上一個數比這個大
                        else cal1 += dp[i-1][u][0];
                    }
                //}
                dp[i][o][0] = cal0 % (ll)MOD;
                dp[i][o][1] = cal1 % (ll)MOD;
            }
        }

        ll ans = 0;
        for(int i = 0;i<=r;i++){
            ans += (dp[n][i][0] % (ll)MOD + dp[n][i][1] % (ll)MOD) % (ll)MOD;
        }
        return ans % (ll)MOD;
    }
};
*/

/* brain rot 不知道在寫啥毀 假dp 實則真bfs
class Solution {
public:
    int zigZagArrays(int n, int l, int r) {
        vector<vector<pair<int, int>>> dp(n+1);
        for(int i=l;i<=r;i++){
            for(int j=l;j<=r;j++){
                if(i == j)continue;
                dp[2].push_back({i,)});
            }
        }
        for(int i=3;i<=n;i++){
            for(auto last:dp[i-1]{
                int type = 0;
                if(last.second == 0){ //當前要變大
                    for(int j=last.first+1;j<=r;j++){
                        dp[i].push_back({j, 1});
                    }
                }
                else{
                    for(int j=l;j<last.first;j++){
                        dp[i].push_back({j, 0};)
                    }
                }
            }
        }
    }
};
*/