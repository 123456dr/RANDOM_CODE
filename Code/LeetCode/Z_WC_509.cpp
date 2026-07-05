class Solution {
public:
    int maxDigitRange(vector<int>& nums) {
        int mxrg = 0;
        vector<pair<int, int>>v;
        for(auto i:nums){
            int mx = 0, mn = 1e9;
            int I = i;
            while(i>0){
                int x = i%10;
                mx = max(mx, x);
                mn = min(mn, x);
                i/=10;
            }
            v.push_back({mx - mn, I});
            mxrg = max(mxrg, mx-mn);
        }
        int ans = 0;
        for(auto i:v){
            if(i.first == mxrg)ans += i.second;
        }
        return ans;
    }
};©leetcode