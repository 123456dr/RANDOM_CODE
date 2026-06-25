// 1752. Check if Array Is Sorted and Rotated
// 髒扣但我不想打掃🧹
class Solution {
public:
    bool check(vector<int>& nums) {
        int mxt=0;
        int mx=0;
        int sum=0;
        for(int i=1;i<nums.size();i++){
            if(nums[i-1] >nums[i]){
                if(mxt ){
                    return false;
                }
                mxt=1;
                mx=nums[i-1];
                sum=0;
            }
            else sum++;
        }
        if(mxt){
            if(mxt && nums[0]<nums[nums.size()-1])return false;
        }
        return true;
    }
};