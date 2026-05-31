// https://leetcode.com/problems/digit-frequency-score/description/
class Solution {
public:
    int digitFrequencyScore(int n) {
        string s = to_string(n);
        vector<int>v(10,0);
        for(int i=0;i<s.length();i++){
            v[s[i]-'0']++;
        }

        int sum = 0;
        for(int i=1;i<10;i++){
            sum+=i*v[i];
        }
        return sum;
    }
};