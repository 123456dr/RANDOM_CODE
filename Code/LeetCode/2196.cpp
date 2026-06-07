//https://leetcode.com/problems/create-binary-tree-from-descriptions/
/*
新思路:
- 與其先把資料存進二維陣列再慢慢轉成樹，不如「一邊讀資料，一邊直接把樹蓋起來」。
- 建構節點與連接關係： 準備一個 unordered_map<int, TreeNode*>。每次讀到一組 [parent, child, isLeft]，就去 map 裡面找這個節點存不存在。不存在就 new 一個出來。然後直接依照 isLeft 把 child 接到 parent 的 left 或 right 指標上。
- 尋找 Root： 準備一個 unordered_set<int> 用來記錄「誰當過小孩」。讀取過程中把所有的 child 都丟進去。
- 結算： 跑一次 map 裡的節點，只要那個節點不在「小孩集合」裡面，它就是整棵樹唯一的 Root！

舊思路:
vector<vector<pair<int,int>>>v;
- 把(parent, child, isLeft)改成v[parent].first儲存/(!isLeft), second儲存child
- 讀取每組資料時，第一次設rt(root)等於第一組的parent，之後每讀取一組就根據child是否為rt而修改rt為parent => 得到跟節點
- sort v的逐列達成先左節點在右節點
- 由v[rt]開始遍歷回傳左右節點，每回傳一次把當前子節點加入queue
*/

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    TreeNode* createBinaryTree(vector<vector<int>>& descriptions) {
        unordered_map<int, TreeNode*>nodeMap;
        unordered_set<int> children;
        for (const auto& desc : descriptions) {
            int parentVal = desc[0];
            int childVal = desc[1];
            bool isLeft = desc[2] == 1;

            // 如果字典裡沒有這個節點，就當場建立一個
            if (nodeMap.find(parentVal) == nodeMap.end()) {
                nodeMap[parentVal] = new TreeNode(parentVal);
            }
            if (nodeMap.find(childVal) == nodeMap.end()) {
                nodeMap[childVal] = new TreeNode(childVal);
            }

            // 直接將子節點掛上父節點
            if (isLeft) {
                nodeMap[parentVal]->left = nodeMap[childVal];
            } else {
                nodeMap[parentVal]->right = nodeMap[childVal];
            }

            // 將 childVal 加入小孩清單
            children.insert(childVal);
        }

        // 步驟 2：尋找 Root (存在於 map 中，但沒有出現在 children 清單裡的那個點)
        TreeNode* root = nullptr;
        for (const auto& pair : nodeMap) {
            if (children.find(pair.first) == children.end()) {
                root = pair.second;
                break; // 找到就提早結束
            }
        }

        return root;
    }
};