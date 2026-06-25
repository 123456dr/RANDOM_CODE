// https://leetcode.com/problems/total-waviness-of-numbers-in-range-ii/
/*
digit dp
所求 = dp(num2) - dp(num1-1);
從 001 開始遞增，每次檢查個位數
*/

#include <iostream>
#include <string>
#include <vector>

using namespace std;

struct result {
    long long cnt;
    long long waves;
};

result memo[20][11][11];

result dfs(const string& s, long long pos, long long prev2, long long prev1, bool is_limit, bool is_lead) {
    if (pos == s.length()) return {1, 0};
    
    // 查表
    if (!is_limit && !is_lead && memo[pos][prev2][prev1].cnt != -1) {
        return memo[pos][prev2][prev1];
    }

    long long up;
    if (is_limit) up = s[pos] - '0';
    else up = 9;
    
    result total = {0, 0};
    for (long long i = 0; i <= up; ++i) {
        bool next_lead = is_lead && (i == 0);
        bool next_limit = is_limit && (i == up);

        int next_prev2 = is_lead ? 10 : prev1;
        int next_prev1 = next_lead ? 10 : i;

        result res = dfs(s, pos + 1, next_prev2, next_prev1, next_limit, next_lead);

        total.cnt += res.cnt;
        total.waves += res.waves;

        if (!is_lead && prev2 != 10 && prev1 != 10) {
            bool isPeak = (prev2 < prev1) && (prev1 > i);
            bool isValley = (prev2 > prev1) && (prev1 < i);
            
            if (isPeak || isValley) {
                total.waves += res.cnt; 
            }
        }
    }
    
    if (!is_limit && !is_lead) {
        memo[pos][prev2][prev1] = total;
    }

    return total;
}

long long solve(long long num) {
    if (num < 100) return 0;
    string s = to_string(num);
    
    for (int i = 0; i < 20; i++)
        for (int j = 0; j < 11; j++)
            for (int k = 0; k < 11; k++)
                memo[i][j][k] = {-1, -1};
                
    return dfs(s, 0, 10, 10, true, true).waves;
}

class Solution {
public:
    long long totalWaviness(long long num1, long long num2) {
        return solve(num2) - solve(num1 - 1);
    }
};