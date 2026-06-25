/*
新思路:
貪心法，先建立好初始亮暗狀態陣列後，從左到右掃描，當遇到暗點則貪心往其右側建立燈泡(只能點亮+-1)
- 前綴和 & 差分 => 優化點亮區段時的 O(n^2)
- 差分紀錄區段l到r間[l+1, r-1]，前綴和時為點亮區段大於1，跳出區段-1

舊思路:
照亮所有點求最小燈泡安裝數，根據現有點之燈泡數值v可照亮範圍+-v區間
先掃一遍並點亮現有燈泡可照亮區間，再次掃描時紀錄當前子間段直到斷掉，根據當前子間段找中位並記錄數值區間長度/2
- 但如果安裝新燈泡只能照亮+-1且不能累加，就不合法
*/


class Solution {
public:
    int minLights(vector<int>& lights) {
        int sz = lights.size();
        vector<int>vt(sz, 0);
        vector<int>diff(sz+1, 0);
        for(int i=0;i<sz;i++){
            if(lights[i] != 0){
                int l = max(0, i-lights[i]);
                int r = min(sz-1, i+lights[i]);
                //for(int j=l;j<=r;j++)vt[j]=1; 改成差分
                diff[l]+=1; //lights[i];
                diff[r+1]-=1; //lights[i];
            }
        }
        
        int sum = 0;
        for(int i=0;i<sz;i++){
            sum+=diff[i];
            if(sum>0)vt[i]=1;
        }
        
        int ans = 0;
        for(int i=0;i<sz;i++){
            if(vt[i] == 0)vt[min(sz-1, i+1)] = 1, vt[min(sz-1, i+2)] = 1, ans++, i++;
        }

        return ans;
    }
};©leetcode