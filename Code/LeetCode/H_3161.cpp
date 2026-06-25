// https://leetcode.com/problems/block-placement-queries/?envType=daily-question
/*
- 線段樹為切地盤(區段)，相比二分搜要使用左界[L, mid]和右界[mid+1, R]不可捨棄mid => (X mid-1)
- 樹開大小4*N (1~8 => 2^4, 1~9 => 2^5)
- .upper_bound(x) => 回傳第一個大於x的元素位址(查無則回傳.end())
- prev(x) => 回傳指標x的前一項位址

新思路:
重點在 [type 2] 查詢時一維陣列O(N) v.s. 線段樹O(log N) 
[建立線段樹] 
- 一個 set s儲存所有障礙位置 (更新完線段樹在加入x到s)
- 一個 vector v線段樹儲存區間段長度，每新增障礙 x ，v[x]設為與前一個障礙間區段大小，若x右邊有障礙則v[x右邊障礙]更新為與x間區段大小
- 判斷 [type 2] 邏輯，找到小於x的最大障礙L，如果max(v線段樹0~L最大值, x-L區段大小) 大於sz回傳true(代表可放置該連續區段)否則false

加入v[x] = (x-s.lower_bound(x))，如果x有右邊障礙，v[*]


原始思路:
根據給定數列最大只會有 5*10^4 ，
- X 但建立 vector<int>儲存，做遍歷搜尋 O(queries.length * 5*10^4) = O(15*10^4 * 5*10^4) => O(10^9)
- O 有沒有可能根據每次 [type 1] 放置障礙時，儲存當前分割段，比如(1,3) => 分割段為0~3 & 3~♾️
從所有分割段中找到符合 [type 2] 範圍的並檢查區間大小有沒有合法
*/

class Solution {
    int mx = 0;
    vector<int> tree;
    vector<bool> ans;

    void add(int tarx, int L, int R, int node, int val){ // tarx點數值, node為儲存範圍的節點
        if(L==R){
            tree[node] = val; // node 樹節點為tarx座標
            return;
        }

        int mid = L + (R-L)/2;
        int nodeL = node*2;
        int nodeR = node*2 + 1;
        if(tarx > mid){
            add(tarx, mid+1, R, nodeR, val);
        }
        else{
            add(tarx, L, mid, nodeL, val);
        }

        tree[node] = max(tree[nodeL], tree[nodeR]);
        return;
    }

    int check(int L, int R, int node, int x){
        if(L > x) return 0;
        if(R <= x)return tree[node];
        int ans = 0;
        int mid = L + (R-L)/2;
        int nodeR = 2*node+1;
        int nodeL = 2*node;

        ans = max(check(mid+1, R, nodeR, x), check(L, mid, nodeL, x));

        return ans;
    }

public:
    vector<bool> getResults(vector<vector<int>>& queries) {
        for(auto i:queries){
            mx = max(mx, i[1]);
        }
        tree.resize(mx*4+1, 0);
        set<int> s;
        s.insert(0);
        for(vector<int> i:queries){
            if(i.size() == 2){ // type 1
                int x = i[1];
                
                auto R = s.upper_bound(x);
                int L = *prev(R);
                // 左
                add(x, 0, mx, 1, x-L);

                // 右
                if(R != s.end()){
                    add(*R, 0, mx, 1, *R-x);
                }

                s.insert(x);
            }
            else{ // type 2
                int x = i[1];
                int sz = i[2];
                auto it = s.upper_bound(x);
                //x左障礙到0
                if(max(check(0, mx, 1 , *prev(it)), x-*prev(it)) >= sz){
                    ans.push_back(true);
                }
                else{
                    ans.push_back(false);
                }
                //左障礙到x
            }
        }
        return ans;
    }
};