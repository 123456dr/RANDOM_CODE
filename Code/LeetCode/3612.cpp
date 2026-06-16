// https://leetcode.com/problems/process-string-with-special-operations-i
class Solution {
public:
    string processStr(string s) {
    int len = s.length();
    string result= "";
        for(int i=0;i<len;i++){
            if(s[i] == '*'){
                if(result.length()){
                    result.pop_back();
                }
            }
            else if(s[i] == '#'){
                result+=result;
            }
            else if(s[i] == '%'){
                string temp="";
                for(int j=result.length()-1;j>=0;j--){
                    temp+=result[j];
                }
                result = temp;
            }
            else{
                result+=s[i];
            }
        }
        return result;
    }
};