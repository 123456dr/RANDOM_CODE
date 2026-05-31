// https://leetcode.com/problems/maximum-number-of-items-from-sale-i/description/
/*
新思路:
不同商品買一次為最佳效益，除了在荷包有剩餘的情況下可以 all in 最便宜的商品
- 預處理每個 item 真實價值 = 本身1 + 可觸發多少 free copies
- 0/1 背包問題: 針對當前物品買或不買
- dp 紀錄各種價錢下可以買的最大值
- 紀錄最便宜的 item price

舊思路:
如果用貪心法排序價錢由小到大，價錢最低的可purchase最多但不一定可以被多個其他item factor整除也就不一定拿到最多free copies，所以假設從價錢小的開始各買一個，直到荷包不夠，紀錄[當前最大copies數量+剩餘荷包全拿去買最便宜的]，然後倒退遞迴每次不拿最後一項最貴的商品更新最大值[當前最大copies數量+剩餘荷包全拿去買最便宜的]。
*/
class Solution {
public:
    int maximumSaleItems(vector<vector<int>>& items, int budget) {
        int sz = items.size();
        vector<int>dp(budget+1, 0);
        vector<int>w(sz, 1);
        int mn = 1e9;
        for(int i=0;i<sz;i++){
            int x = items[i][0];
            mn = min(mn, items[i][1]);
            for(int j=0;j<sz;j++){
                if(i == j)continue;
                if(items[j][0]>=x && items[j][0]%x == 0){
                    w[i]++;
                }
            }
        }
        for(int i=0;i<sz;i++){
            for(int j=budget;j>=items[i][1];j--){
                dp[j] = max(dp[j], dp[j-items[i][1]]+w[i]);
            }
        }

        int ans = 0;
        for(int i=0;i<=budget;i++){
            ans = max(ans, dp[i]+(budget-i)/mn);
        }
        return ans;
    }
};