// https://leetcode.com/contest/weekly-contest-507/problems/valid-subarrays-with-matching-sum-digits-i/description/
/*
建立前綴和陣列，雙迴圈遍歷區間段 O(1500*1500)OK
*/

#define ll long long
class Solution {
public:
    int countValidSubarrays(vector<int>& nums, int x) {
        vector<ll>v; // 首項為零
        v.push_back(0);
        int sz = nums.size();

        ll sum = 0;
        for(int i=0;i<sz;i++){
            sum+=nums[i];
            v.push_back(sum);
        }

        int ans = 0;
        // 求[l ,r] => v[r]-v[l-1] 第零項為0
        for(int i=1;i<sz+1;i++){
            for(int j=i;j<sz+1;j++){
                ll cul = v[j]-v[i-1];
                if(cul%10 == x){
                    ll temp = cul;
                    while(temp>=10)temp/=10;
                    if(temp == x){
                        ans++;
                    }
                }
            }
        }
        return ans;
        
    }
};©leetcode