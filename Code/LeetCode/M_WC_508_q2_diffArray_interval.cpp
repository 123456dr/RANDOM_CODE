// https://leetcode.com/contest/weekly-contest-508/problems/filter-occupied-intervals/

// 另解: 排序後分段處理（Sort, Merge, Filter）
/*
排序所有區間段的開頭，每次讀入一組區間段，因為起點以排序小到大
- 遇到新起點比上一段終點小者，直接更改上段終點為新終點(合併)
最後分三段處理: 終點小於fStart、起點大於fEnd、被切斷的
*/

// sweep line 掃描線
class Solution {
public:
    vector<vector<int>> filterOccupiedIntervals(vector<vector<int>>& ori, int fS, int fE) {
        vector<vector<int>> ans;
        map<int, int>mp;
        for(auto i:ori){
            mp[i[0]]++;
            mp[i[1]+1]--;
        }
        mp[fS] += 0;
        mp[fE+1] += 0;
        int sum = 0;
        int isF = 0;
        vector<int>temp;
        int last = 0;
        for(auto i:mp){
            sum += i.second;
            if(sum > 0 && !isF && (i.first > fE || i.first < fS)){
                isF = 1;
                temp.push_back(i.first);
            }
            else if((sum == 0 || i.first==fS) && isF){
                temp.push_back(i.first - 1);
                isF = 0;
                ans.push_back(temp);
                temp.clear();
            }
            last = i.first;
        }
        
        return ans;
    }
};©leetcode