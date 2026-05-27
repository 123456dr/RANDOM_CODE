// https://leetcode.com/problems/count-the-number-of-special-characters-ii
/*
建立一個map<char,pair<int,<int>>>mp;然後遍歷word的每個字母，先判斷mp[word[i]]存不存在，若存在如果該字母是大寫則把第一個值改成i否則第二個值改成i，若不存在則還是根據該字母把第一或第二值改成i但沒改的那個值要設定成-1，最後遍歷mp，遇到-1或是第二個值大於第一個值則跳過否則ans++

改成vector因為只有26個字母安餒，
還有只要紀錄第一個大寫位置不能覆寫
*/

class Solution {
public:
    int numberOfSpecialChars(string word) {
        vector<pair<int,int>> v(26,pair<int,int>(-1,-1));
        int len = word.length();
        for(int i=0;i<len;i++){
            if(isupper(word[i]) && v[word[i]-'A'].first == -1){
                v[word[i]-'A'].first=i;
            }
            else if(islower(word[i])){
                v[word[i]-'a'].second=i;
            }
        }
        int ans=0;
        for(auto i:v){
            if(i.first ==-1 || i.second == -1)continue;
            if(i.second>i.first)continue;
            ans++;
        }
        return ans;
    }
};