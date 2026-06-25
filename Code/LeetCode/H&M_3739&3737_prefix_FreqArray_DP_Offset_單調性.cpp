// https://leetcode.com/problems/count-subarrays-with-majority-element-i/?envType=daily-question&envId=2026-06-25

/*
新思路優化:
- nums[i] = target則得分+1，否則-1
- [計數陣列]cnt[]，紀錄有幾個樹小於得分，因為會有負得分狀況，平移(2 * sz + 1)預留0分
- 遍歷一次迴圈
    - smol_cnt 紀錄從頭到當前得分小於當前得分的個數，狀態轉移條件為[若當前值=target, +=cnt[當前]；否則-=cnt[當前]]
    - ans += smol_cnt,
    - 更新當前累積分數: 等於target, curr_cnt += 1； 否則 -=1

因為只要考慮nums陣列中的數值是否為target，所以具有單調性每次只會有+-1，smaller_count每次只會加減一組cnt[i]

*/

class Solution {
public:
    int countMajoritySubarrays(vector<int>& nums, int tar) {
        int sz = nums.size();
        int offset = sz;
        vector<int>cnt(2 * sz + 1, 0);
        int smol_cnt = 0;
        int ans = 0;
        int cur_cnt = 0;
        for(int i=0;i<sz;i++){
            cnt[cur_cnt + offset] ++;
            if(nums[i] == tar){
                smol_cnt += cnt[cur_cnt + offset];
                cur_cnt ++;
            }
            else{
                cur_cnt --;
                smol_cnt -= cnt[cur_cnt + offset];
            }
            ans += smol_cnt;
        }
        return ans;
    }
};


/*
優化概念
- 更快判別合法數是否大於半數 => cnt 遇到非法--, 合法++
- 如果是求「連續」區間，直接雙迴圈暴力就可以。本次程式碼的迴圈i=1~sz模擬子串長度是多餘的
*/
/*
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
*/