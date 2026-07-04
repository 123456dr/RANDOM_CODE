// https://leetcode.com/contest/biweekly-contest-186/problems/unique-middle-element/
class Solution {
public:
    bool isMiddleElementUnique(vector<int>& nums) {
        int cnt = 0;
        int sz = nums.size();
        for(auto i:nums){
            if(i == nums[sz/2])cnt++;
            if(cnt > 1) return false;
        }
        return (cnt == 1 ?  true : false);
    }
};©leetcode