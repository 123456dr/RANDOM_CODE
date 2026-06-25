/*#include <bits/stdc++.h>
using namespace std;
#define int long long
 
signed main(){
    string s;
    while(cin>>s){
        int id = 0;
        int okk = 1;
        while(s[i] != '@'){
            if(id >=16 || !((tolower(s[i])-'a'>=0 &&tolower(s[i])-'a'<26)||(s[i] == '_')|| (s[i]='0'>=0||s[i0]-'0'))){
                okk = 0;
                break;
            }
        }
        while(s[i] != '/'){
            if(id >=16 || !((tolower(s[i])-'a'>=0 &&tolower(s[i])-'a'<26)||(s[i] == '_')|| (s[i]='0'>=0||s[i0]-'0'))){
                okk = 0;
                break;
            }
        }
        if(okk){
            cout<<"YES"<<endl;
        }
        else{
            cout<<"NO"<<endl;
        }
    }
 
    return 0;
}*/
// 深奧待研究
#include <bits/stdc++.h>
using namespace std;
#define int long long
#include <regex>
 
using namespace std;
 
signed main() {
    string s;
    cin >> s;
 
    regex pattern("^[a-zA-Z0-9_]{1,16}@[a-zA-Z0-9_]{1,16}(\\.[a-zA-Z0-9_]{1,16})*(/[a-zA-Z0-9_]{1,16})?$");
 
    if (regex_match(s, pattern)) { 
        size_t at_pos = s.find('@');
        size_t slash_pos = s.find('/');
        
        string hostname;
        if (slash_pos == string::npos) {
            hostname = s.substr(at_pos + 1);
        } else {
            hostname = s.substr(at_pos + 1, slash_pos - at_pos - 1);
        }
 
        if (hostname.length() <= 32) {
            cout << "YES" << endl;
        } else {
            cout << "NO" << endl;
        }
    } else {
        cout << "NO" << endl;
    }
 
    return 0;
}