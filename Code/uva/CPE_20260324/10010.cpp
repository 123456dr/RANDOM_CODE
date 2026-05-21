// https://cpe.mcu.edu.tw/cpe/problems/CPE260324/CPE260324-P2.uva10010.pdf
// WA 直線行走不能轉彎 f(dir固定)

#include <bits/stdc++.h>
using namespace std;
#define int long long
int R,C;

int f(int ind, int r, int c, vector<string> v, string s){
    if(ind == -1)return 1;

    //上
    if(r-1>=0 && v[r-1][c] == s[s.length()-ind]){
        return f(ind-1, r-1, c, v, s);
    }//下
    else if(r+1<R && v[r+1][c] == s[s.length()-ind]){
        return f(ind-1, r+1, c, v, s);
    }//左
    else if(c-1>=0 && v[r][c-1] == s[s.length()-ind]){
        return f(ind-1, r, c-1, v, s);
    }//右
    else if(c+1<C && v[r][c+1] == s[s.length()-ind]){
        return f(ind-1, r, c+1, v, s);
    }
    return 0;
}


signed main(){

    ios::sync_with_stdio(0);
    cin.tie(0);

    int n;cin>>n;
    while(n--){
        int r,c;cin>>r>>c;
        R=r,C=c;
        vector<string>v(r);
        for(auto &i:v)cin>>i;
        for(int i=0;i<r;i++){
            string s = v[i];
            string temp = "";
            for(int j=0;j<c;j++){
                if(s[j]-'a'<26)temp+=s[j];
                else temp += s[j]-'A'+'a';
            }
            v[i] = temp;
        }
        
        int num;cin>>num;
        while(num--){
            string s;cin>>s;
            string temp = "";
            for(int i=0;i<s.length();i++){
                if(s[i]-'a'<26)temp+=s[i];
                else temp += s[i]-'A'+'a';
            }
            s = temp;
            int ans = 0;
            for(int i=0;i<c;i++){
                for(int j=0;j<r;j++){
                    temp = v[j];
                    if(temp[i] == s[0]){
                        if(f(s.length()-1, j, i, v, s)){
                            cout<<j<<" "<<i<<endl;
                            ans = 1;
                            break;
                        }
                    }
                }
                if(ans)break;
            }
        }
    }

    return 0;
}