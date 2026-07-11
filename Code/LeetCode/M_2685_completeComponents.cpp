// https://leetcode.com/problems/count-the-number-of-complete-components/description/

/*
component => 連通塊
complete component => 同連通塊內個點都存在相連邊
因為單個連通塊 [總邊數*2 = 總節點數 * 總節點數-1(與自己外所有節點都有邊)] // *2因為每個邊都連接兩個節點會double
所以 dfs 每個點，每次走訪到未走過的點 e+=1, 邊數+=連接節點數
再確認是否符合公式 好耶好耶
*/
class Solution {
public:
    int countCompleteComponents(int n, vector<vector<int>>& edges) {
        vector<vector<int>>v(n);
        for(auto i:edges){
            v[i[0]].push_back(i[1]);
            v[i[1]].push_back(i[0]);
        }

        int ans = 0;
        vector<int>vis(n, 0);
        int e = 0;
        int node = 0;
        
        auto dfs = [&](auto &self, int x) -> void{
            vis[x] = 1;
            node ++;
            e += v[x].size();
            for(auto i:v[x]){
                if(vis[i] == 0){
                    self(self, i);
                }
            }
            return;
        };

        for(int i=0;i<n;i++){
            if(vis[i] == 0){
                e = 0, node = 0;
                dfs(dfs, i);
                if(e == node * (node-1))ans++;
            }
        }
        return ans;
    }
};