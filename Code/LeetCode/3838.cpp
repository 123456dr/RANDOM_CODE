class Solution {
public:
    string mapWordWeights(vector<string>& words, vector<int>& weights) {
        string ans="";
        for(auto i:words){
            int sz = i.length();
            int sum = 0;
            for(int j=0;j<sz;j++){
                sum += weights[i[j] - 'a'];
            }
            ans.push_back('a'+(25-sum%26));
        }
        return ans;
    }
};
/*
25 -> 0
0  -> 25
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
*/