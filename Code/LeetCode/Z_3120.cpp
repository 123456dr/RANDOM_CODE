// https://leetcode.com/problems/count-the-number-of-special-characters-i/
/*建立一個vector<pair<int,int>>v(26,pair<int,int>(0,0));

然後遍歷字串每個字母，如果當前字母是大寫則換算成0-25序號i,v[i].first=1;反之小寫則v[i].second=1;最後遍歷v看有first&second的cont++;
*/

class Solution {
public:
    int numberOfSpecialChars(string word) {
        vector<pair<int,int>> v(26, pair<int,int>(0,0));
        int cont = 0;
        int len = word.length();
        for(int i=0;i<len;i++){
            if(isupper(word[i]))v[(int)word[i]-'A'].first=1;
            else v[(int)word[i]-'a'].second=1;
        }
        for(auto i:v){
            if(i.first && i.second)cont++;
        }
        return cont;
    }
};