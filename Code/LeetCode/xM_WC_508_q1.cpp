// https://leetcode.com/contest/weekly-contest-508/problems/
/*
O(k) 先sort再跑前k個
- 在mul大於0的k次操作，貪心找不重複最大值乘以mul並加入sum
- mul 每次減一等於最後減k(共k次操作)
*/

#define ll long long
class Solution {
public:
    long long maxSum(vector<int>& nums, int k, int mul) {
        sort(nums.begin(), nums.end());
        ll ans = 0;
        ll i = nums.size()-1;
        while(k--){
            if(mul < 1)mul = 1;
            ans += (ll)nums[i--] * (ll)mul;
            mul --;
        }
        return ans;
    }
};©leetcode