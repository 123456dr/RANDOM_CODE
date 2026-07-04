// https://leetcode.com/contest/biweekly-contest-186/problems/maximum-valid-pair-sum/description/
class Solution {
public:
    int maxValidPairSum(vector<int>& nums, int k) {
        int sz = nums.size();
        int r = k, l = 0;
        int mx = 0;
        int mxl = 0;
        for(int i=k;i<sz;i++){
            mxl = max(mxl, nums[i-k]);
            mx = max(mx, nums[i] + mxl);
        }
        
        return mx;
    }
};©leetcode