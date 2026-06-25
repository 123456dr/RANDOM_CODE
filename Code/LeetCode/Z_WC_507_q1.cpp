// https://leetcode.com/contest/weekly-contest-507
/*
計算[l, r],[u, d]兩組抵銷後的組數，在計算_的個數後相加
*/
class Solution {
public:
    int maxDistance(string moves) {
        int ans = 0;
        int sz = moves.length();
        int lr = 0;
        int ud = 0;
        int line = 0;
        for(int i=0;i<sz;i++){
            if(moves[i] == 'R')lr++;
            else if(moves[i] == 'L')lr--;
            else if(moves[i] == 'U')ud--;
            else if(moves[i] == 'D')ud++;
            else line++;
        }
        ans = abs(lr)+abs(ud)+line;
        return ans;
    }
};©leetcode