// https://leetcode.com/contest/biweekly-contest-185/problems/finish-time-of-tasks-i/description/
/*
v[i][j] 陣列存 i點連結的子節點，但第一個值存子節點個數(可能大於2)
- 排序子節點數小到大，從子節點少的開始處理
- 每次處理把該點的finish time另外儲存到陣列fin

舊版: 少了樹狀層級順序處理 => DFS

- 樹狀動態規劃 (Tree DP)：由子節點狀態往上推導父節點狀態。
- 深度優先搜尋 (DFS)：用遞迴深入葉子節點後回溯。
- 後序遍歷 (Post-order Traversal)：確保處理當前節點前，所有子節點已優先處理完畢。
- 鄰接串列 (Adjacency List)：用以儲存與建構樹狀圖結構。
- 拓撲排序邏輯 (Topological Order)：解決節點間的有向依賴關係順序。
*/

class Solution {
public:
    vector<int> order;
    vector<vector<int>> v;

    void dfs(int id) {
        for (int i = 2; i < v[id].size(); i++) {
            dfs(v[id][i]);
        }
        order.push_back(id);
    }

    long long finishTime(int n, vector<vector<int>>& edges, vector<int>& baseTime) {
        v.resize(n);
        int id = 0;
        for (auto &i : v) i.push_back(0), i.push_back(id++);
        for (auto i : edges) {
            v[i[0]].push_back(i[1]);
            v[i[0]][0]++;
        }

        vector<long long> fin(n, 0);
        dfs(0);

        for (int i = 0; i < n; i++) {
            int curr = order[i];
            int sz = v[curr].size() - 2;
            long long ear = 1e18;
            long long last = 0;
            
            for (int j = 2; j < 2 + sz; j++) {
                ear = min(ear, fin[v[curr][j]]);
                last = max(last, fin[v[curr][j]]);
            }
            
            if (sz != 0) {
                fin[curr] = (last - ear) + baseTime[curr] + last;
            } else {
                fin[curr] = baseTime[curr];
            }
        }
        return fin[0];
    }
};


/*
class Solution {
public:
    long long finishTime(int n, vector<vector<int>>& edges, vector<int>& baseTime) {
        vector<vector<int>>v(n);
        int id = 0;
        for(auto &i:v)i.push_back(0), i.push_back(id++);
        for(auto i:edges){
            v[i[0]].push_back(i[1]); // 單向
            v[i[0]][0]++; //子節點計數
        }

        vector<int>fin(n, 0);
        sort(v.begin(), v.end());
        for(int i=0;i<n;i++){
            for(int j=0;j<v[i].size();j++){
                cout<<v[i][j]<<" ";
            }cout<<endl;
        }

        
        for(int i=0;i<n;i++){
            int sz = v[i].size()-2;
            int ear = 1e9;
            int last = 0;
            for(int j=2;j<2+sz;j++){
                ear = min(ear, fin[v[i][j]]);
                last = max(last, fin[v[i][j]]);
            }
            if(sz!=0){
                fin[v[i][1]] = (last - ear)+baseTime[v[i][1]]+last;
            }
            else fin[v[i][1]] = baseTime[v[i][1]];
        }
        return fin[0];
    }
};*/©leetcode