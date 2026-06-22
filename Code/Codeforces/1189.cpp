// https://leetcode.com/problems/maximum-number-of-balloons/?envType=daily-question&envId=2026-06-22
class Solution {
public:
    int maxNumberOfBalloons(string text) {
        map<char, int>mp = {
            {'b', 0},
            {'a', 0},
            {'l', 0},
            {'o', 0},
            {'n', 0},
        };
        for(auto i:text){
            mp[i] ++;
        }
        int ans = min({mp['a'], mp['b'],  mp['l']/2, mp['o']/2, mp['n']});
        return ans;
    }
};