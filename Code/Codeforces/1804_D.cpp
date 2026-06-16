/*
[貪心]
最少房間有人 => 1總數 - min(m/4, [11相鄰數])
最多房間有人 => 1總數 - max(0, [非11相鄰數] = m/4 - [11相鄰數])
因為是樓層 所以不會有上下只有左右
*/
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int n, m;
    while(cin>>n>>m){
        string s;
        int ansmx = 0;
        int ansmn = 0;
        while(n--){
            cin>>s;
            int cnt1 = 0;
            int cnt11 = 0;
            int cntx = 0;
            for(int j=0;j<m;j++){
                if(s[j] == '1'){
                    cnt1++;
                }
            }
            for(int j=0;j<m-1;j++){
                if(s[j] == '1' && s[j+1] == '1'){
                    cnt11++;
                    j++;
                }
            }
            for(int j=0;j<m-1;j++){
                if(!(s[j] == '1' && s[j+1] == '1')){
                    cntx++;
                    j++;
                }
            }
            ansmn += cnt1 - min(m/4, cnt11);
            ansmx += cnt1 - max((int)0, m/4 - cntx);
        }
        
        cout<<ansmn<<" "<<ansmx<<endl;
    }

    return 0;
}