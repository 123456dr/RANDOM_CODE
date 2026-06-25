// https://leetcode.com/problems/minimum-element-after-replacement-with-digit-sum

class Solution {
public:
    int minElement(vector<int>& nums) {
        int mn=1e9;
        for(auto i:nums){
            string s=to_string(i);
            int len = s.length();
            int sum=0;
            if(i==0)return 0;
            for(int j=0;j<len;j++){
                sum+=s[j]-'0';
            }
            mn=min(mn, sum);
        }
        return mn;
    }
};