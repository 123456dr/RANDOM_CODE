// https://leetcode.com/contest/weekly-contest-509/problems/subsequence-after-one-replacement/description/
/*
可更改一字母，求s是否全存在t並且照字母順序出現，
建立pref和suff儲存由前由後第一次合法(照順序)出現的index，
最後遍歷一次s，當r-l大於1代表有空間替換字母

- 子序列 (Subsequence): 不改變相對順序擷取出的字串片段。
- 前/後綴陣列 (Prefix / Suffix Array): 預先記錄左右兩側的匹配進度，以便後續用 $O(1)$ 時間查表。
- 貪婪演算法 (Greedy Algorithm): 比對時只要字元相同就立刻配對，採取當下最直接的最佳解。
- 雙指標 (Two Pointers): 使用兩個獨立變數（`i`, `j`）分別走訪字串 `s` 與 `t` 進行進度追蹤。
- 空間換取時間 (Space-Time Tradeoff): 額外消耗記憶體建立陣列，成功將整體時間複雜度壓低至 $O(N)$。
- 哨兵值與邊界條件 (Sentinel Values & Edge Cases): 刻意設定 `-1` 與 `tz` 等虛擬邊界，讓頭尾極端情況也能套用同一套數學公式（`r - l >= 2`）。
*/
class Solution {
public:
    bool canMakeSubsequence(string s, string t) {
        int sz = s.length();
        int tz = t.length();
        vector<int>pref(sz, -1);
        vector<int>suff(sz, -1);
        if(sz>tz)return false;
        int j = 0;
        for(int i=0;i<sz;i++){
            while(j<tz && s[i] != t[j]){
                j++;
            }
            if(j<tz && s[i] == t[j]){
                pref[i] = j++;
            }
        }
        j = tz-1;
        for(int i=sz-1;i>=0;i--){
            while(j>=0 && s[i] != t[j]){
                j--;
            }
            if(j>=0 && s[i] == t[j]){
                suff[i] = j--;
            }
        }
        // 0 2 3, 0 2 3
        // 1 3 0 -1 4, 2 3 0 -1 4
        for (int i = 0; i < sz; i++) {
            int l = (i == 0) ? -1 : pref[i - 1];
            int r = (i == sz - 1) ? tz : suff[i + 1];

            bool left_valid = (i == 0 || pref[i - 1] != -1);
            bool right_valid = (i == sz - 1 || suff[i + 1] != -1);

            if (left_valid && right_valid && (r - l >= 2)) {
                return true;
            }
        }
        return false;
    }
};