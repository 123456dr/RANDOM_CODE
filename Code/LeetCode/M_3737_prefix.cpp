// https://leetcode.com/problems/count-subarrays-with-majority-element-i/?envType=daily-question&envId=2026-06-25
/*
優化概念
- 更快判別合法數是否大於半數 => cnt 遇到非法--, 合法++
- 如果是求「連續」區間，直接雙迴圈暴力就可以。本次程式碼的迴圈i=1~sz模擬子串長度是多餘的
*/

class Solution {
public:
    int countMajoritySubarrays(vector<int>& nums, int target) {
        int sz = nums.size();
        int ans = 0;
        vector<int>v(sz+1, 0);
        int sum = 0;
        for(int i=1;i<=sz;i++){
            if(nums[i-1] == target)sum+=1;
            v[i] = sum;
            //cout<<v[i]<<" ";
        }//cout<<endl;

        for(int i=1;i<=sz;i++){
            int half = i/2+1;
            for(int j=1;j+i-1<=sz;j++){
                if(v[j+i-1]-v[j-1] >= half){
                    ans++;
                }//cout<<v[j+i-1]<<" "<<v[j-1]<<endl;
            }
        }

        return ans;
    }
};