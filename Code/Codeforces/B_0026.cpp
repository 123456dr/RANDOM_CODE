// https://codeforces.com/contest/26/problem/B
// 若為計算最長連續合法括號，要記錄 index，pop一個左括號，該 index-右括號index相減之類的ㄇ (應該?!
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    string s;
    while(cin>>s){
        int len = s.length();
        int lcont = 0, rcont = 0;
        for(int i=0;i<len;i++){
            if(s[i] == '(')lcont++;
            else if(s[i] == ')' && lcont){
                rcont++;
                lcont--;
            }
        }
        cout<<rcont*2<<endl;
    }

    return 0;
}