// https://leetcode.com/problems/jump-game-vii
// dp[]紀錄該位置是否為合法跳板'0'
// 滑動視窗 合法範圍內累加跳板okCont，當剛超出左界的dp[i]為合法跳板則okCont--
// 直到i = len-1, okCont>0 則 return true

class Solution {
public:
    bool canReach(string s, int minJump, int maxJump) {
        int len = s.length();
        vector<int> dp (len,0);
        int okCont = 0;
        dp[0]=1;
        if(s[len-1] == '1')return false;
        for(int i=1;i<len;i++){
            if(i-minJump>=0){
                if(dp[i-minJump])okCont++;
            }
            if(i-maxJump-1>=0){
                if(dp[i-maxJump-1])okCont--;
            }
            if(okCont && s[i] == '0')dp[i] = 1;
        }
        if(okCont > 0)return true;
        else return false;
    }
};