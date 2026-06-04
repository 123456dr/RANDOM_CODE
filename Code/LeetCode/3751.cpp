// https://leetcode.com/problems/total-waviness-of-numbers-in-range-i
// https://leetcode.com/problems/total-waviness-of-numbers-in-range-ii
/*
新思路:https://leetcode.com/problems/total-waviness-of-numbers-in-range-i
[digit dp]
所求[num1, num2] = dp[num2] - dp[num1-1]太難了下次做

舊思路: 
三個數字為組單位，每次比較中間數字有沒有高/低於外兩者
- 讀入左右界，遍歷含，每次將當前數值儲存為字串
- 其實建立指標指向要檢查的中間數就好不用左右指標，範圍1~len-2
- 建立左右指標滑動視窗，右指標初始化為字串index 2，當右指標>字串len-1則跳出比較
*/

class Solution {
public:
    int totalWaviness(int num1, int num2) {
        int ans = 0;
        for(int j=num1;j<=num2;j++){
            int i = j;
            while(i>100){
                if(i%10 > i/10%10 && i/100%10 >i/10%10)ans++;
                else if(i%10 < i/10%10 && i/100%10 <i/10%10)ans++;

                i/=10;
            }
        }
        return ans;
    }
};