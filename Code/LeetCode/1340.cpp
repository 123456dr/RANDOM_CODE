// 1340. Jump Game V
// https://leetcode.com/problems/jump-game-v/?envType=daily-question&envId=2026-05-24
class Solution {
public:

    int dfs(int ind, vector<int> &arr, int d, vector<int> &dp){
        if(dp[ind])return dp[ind];
        int cont = 0;

        for(int i=ind+1;i<arr.size() && i<=ind+d;i++){ // 右
            if(arr[i] >= arr[ind])break; // 相等高度終止條件 => 否則無限遞迴
            cont = max(cont, dfs(i, arr, d, dp));
        }
        for(int i=ind-1;i>=0 && i>=ind-d;i--){ // 左
            if(arr[i] >= arr[ind])break;
            cont = max(cont, dfs(i, arr, d, dp));
        }

        dp[ind] = cont+1;
        return dp[ind];
    }

    int maxJumps(vector<int>& arr, int d) {
        int sz = arr.size();
        vector<int>dp(sz,0);

        int mx = 0;
        for(int i=0;i<sz;i++){
            mx = max(mx, dfs(i, arr, d, dp));
        }
        return mx;
    }
};