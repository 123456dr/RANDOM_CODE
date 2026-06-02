// https://codeforces.com/problemset/problem/2204/D
/*
題目設定a->b<-c為兩組beautiful，其中b節點只有向內邊而a, c只有向外邊
所以也就是
- 遍歷節點，上色各節點(上色分為向內/外節點)，並看當前節點鄰居有沒有同色，若同色則為不合法，若無上色則將該鄰點上為異色
- 計算有幾個合法的點
- 二分圖
- 三角關係為否
*/

#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int t;cin>>t;
    while(t--){
        int n, m;cin>>n>>m;
        vector<vector<int>> v(n+1);
        for(int i=0;i<m;i++){
            int x, y;
            cin>>x>>y;
            v[x].push_back(y);
            v[y].push_back(x);
        }

        // 遍歷
        int ans = 0;
        vector<int>color(n+1, -1);
        for(int i=1;i<=n;i++){ // 題目給的節點index-1
            queue<int>q;
            int cont[2] = {0}; // 紀錄兩種顏色各個數
            int okk = 1;
            if(color[i] == -1){ // 未塗色當起點
                q.push(i);
                color[i] = 0;

                cont[0]++;
                while(!q.empty()){
                    int k = q.front();
                    q.pop();

                    for(auto u:v[k]){
                        if(color[u] == -1){
                            color[u] = 1-color[k];
                            cont[color[u]]++;
                            q.push(u);
                        }
                        else if(color[u] == color[k]){
                            okk = 0;
                        }
                    }
                }
            }
            if(okk)ans+=max(cont[0], cont[1]);
        }
        cout<<ans<<endl;
    }

    return 0;
}

/*
[1-2-3]
1-2
2-3
3-2
*/



/*
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;

int main() {
    // 1. 優化輸入輸出速度 (處理大量測資時非常重要)
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    // 讀取節點數(n)與邊數(m)
    if (!(cin >> n >> m)) return 0;

    // 建立鄰接串列 (Adjacency List) 來儲存這張無向圖
    // 節點編號通常為 1 ~ n，所以大小開 n + 1
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // color 陣列用來記錄每個節點被染成的顏色。
    // -1: 尚未走訪過, 0: 顏色A (如 Source), 1: 顏色B (如 Sink)
    vector<int> color(n + 1, -1);
    
    int max_beautiful = 0; // 記錄最多可以有幾個美麗的節點

    // 2. 遍歷所有節點，逐一處理每個「連通分塊 (Connected Component)」
    for (int i = 1; i <= n; ++i) {
        // 如果這個節點還沒被塗色，代表我們發現了一個新的連通分塊
        if (color[i] == -1) {
            
            queue<int> q;
            q.push(i);
            color[i] = 0; // 第一個點先強制染成顏色 0

            // 準備一個陣列記錄這個分塊中，顏色 0 和顏色 1 分別有幾個點
            int cnt[2] = {0, 0}; 
            cnt[0]++; // 顏色 0 的數量 + 1
            
            bool isBipartite = true; // 預設這個分塊是二分圖

            // 3. 開始 BFS 進行交替染色
            while (!q.empty()) {
                int u = q.front();
                q.pop();

                // 檢查與 u 相連的所有鄰居 v
                for (int v : adj[u]) {
                    if (color[v] == -1) {
                        // 狀況 A：鄰居還沒走訪過 -> 染上與自己相反的顏色
                        color[v] = 1 - color[u];
                        cnt[color[v]]++; // 對應顏色的計數器 + 1
                        q.push(v);
                    } 
                    else if (color[v] == color[u]) {
                        // 狀況 B：鄰居已經走訪過，而且顏色竟然跟我一樣！
                        // 發生衝突，這代表圖裡面有「奇數環」，絕對不是二分圖
                        isBipartite = false;
                    }
                }
            }

            // 4. 結算這個連通分塊的貢獻
            if (isBipartite) {
                // 如果是完美的二分圖，我們取點數比較多的那群當作 Source
                // 這樣產生的美麗節點就會最多
                max_beautiful += max(cnt[0], cnt[1]);
            } else {
                // 如果不是二分圖，不管怎麼指方向都會衝突
                // 這個分塊無法產生任何美麗節點，貢獻為 0 (所以不加東西)
            }
        }
    }

    // 5. 輸出最終答案
    cout << max_beautiful << "\n";

    return 0;

    */