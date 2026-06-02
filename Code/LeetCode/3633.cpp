// https://leetcode.com/problems/earliest-finish-time-for-land-and-water-rides-i/?envType=daily-question&envId=2026-06-02
// 1.5h
/*
沒有類別限制，目標是在關園前「玩到最多數量的設施」？

對應概念：區間排程問題 (Interval Scheduling) / 貪心法 (Greedy)

這會變成極度經典的活動選擇問題。策略會變成：永遠優先挑選「結束時間最早」的設施，這樣才能保留最多的時間給後面的設施。這跟你的「理想結束時間」直覺不謀而合！
*/
class Solution {
public:
    int earliestFinishTime(vector<int>& landStartTime, vector<int>& landDuration, vector<int>& waterStartTime, vector<int>& waterDuration) {
        vector<pair<int,int>>vL;
        vector<pair<int,int>>vW;
        for(int i=0;i<landStartTime.size();i++){
            vL.push_back({landStartTime[i]+landDuration[i], landStartTime[i]});
        }
        for(int i=0;i<waterStartTime.size();i++){
            vW.push_back({waterStartTime[i]+waterDuration[i], waterStartTime[i]});
        }

        sort(vL.begin(), vL.end());
        sort(vW.begin(), vW.end());

        int ans = 1e9;
        for(int i=0;i<waterStartTime.size();i++){
            if(waterStartTime[i] <= vL[0].first) ans = min(ans, vL[0].first + waterDuration[i]);
            else{
                ans = min(ans, waterStartTime[i] + waterDuration[i]);
            }
        }
        for(int i=0;i<landStartTime.size();i++){
            if(landStartTime[i] <= vW[0].first) ans = min(ans, vW[0].first + landDuration[i]);
            else{
                ans = min(ans, landStartTime[i] + landDuration[i]);
            }
        }
        return ans;

    }
};