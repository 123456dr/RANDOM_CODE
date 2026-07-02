// https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/description/
/*
分別紀錄字母a, b, c最後出現的index(初始化為-1，
當三者不為-1，此時最左的index～當前遍歷字母第i個一定保證至少含一組abc，
因為至少含一組，當前最左index到0皆可當子字串起始點➡️共有最左index+1種
*/
class Solution {
public:
    int numberOfSubstrings(string s) {
        int a=-1, b=-1, c=-1;
        int sz = s.length();
        int ans = 0;
        for(int i=0;i<sz;i++){
            if(s[i]=='a')a=i;
            if(s[i]=='b')b=i;
            if(s[i]=='c')c=i;
            if(a>=0 && b>=0 && c>=0){
                ans += min({a, b, c})+1;
            }
        }
        return ans;
    }
};