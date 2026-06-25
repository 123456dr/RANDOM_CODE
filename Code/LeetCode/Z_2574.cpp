// https://leetcode.com/problems/left-and-right-sum-differences
class Solution {
public:
    vector<int> leftRightDifference(vector<int>& nums) {
        int lSum = 0;
        int rSum = 0;
        int sz = nums.size();
        for(auto i:nums)rSum+=i;

        rSum -= nums[0];
        vector<int>ans;
        for(int i=0;i<sz;i++){
            ans.push_back(abs(lSum - rSum));
            lSum+=nums[i];
            if(i+1<sz)rSum-=nums[i+1];
            else rSum = 0;
        }
        return ans;
    }
};