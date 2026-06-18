/*
新:
單調棧 (Monotonic Stack)
1. 建立單調棧 st 存放「(高度, 數量)」對組，採【由右向左】逆序掃描。
2. 每次以當前元素作為發射跳板，維護棧頂到棧底「由小到大」的嚴格單調遞增性質。
3. 若棧不為空且棧頂高度「大於」當前跳板，代表引發連鎖塌陷（高牆被削平）：
   - 觸發【整包帶走】機制，將被削平的高牆數量累加至計數器 cnt（計數器初始為 1，含跳板自身）。
   - 持續 pop 棧頂，直到遇見更矮的牆（即破壞穿透機制時）或棧空為止。
4. 將合體後的新牆狀態 push 回單調棧 st 內，繼續往左遞迴模擬。
5. 【時間複雜度 O(n)】：每座塔至多進出棧各一次。
6. 最終將棧內殘留的所有「高度 × 數量」進行線性加總，即為總和之最小值。

舊思路:
建立stack st由右到左掃描，每次模擬跳板，
如果st有東西則pop比較有沒有大於跳板，
- 沒有的話跳出往左換下一個跳板
- 否則累加當前消除成語跳板同高度的計數並且在繼續pop st直到沒有大於跳板值，
    然後st push累加計數個+1(加上當前跳板1)高度等於當前跳板高度，接著往左模擬下一個跳板，最後把所有st內的數值乘以個數後加總等於答案
*/

#include <bits/stdc++.h>
using namespace std;
#define int long long
signed main(){

    int t;cin>>t;
    while(t--){
        int n;cin>>n;
        vector<int>v(n);
        for(int &i:v)cin>>i;

        stack<pair<int, int>>st;
        for(int i=n-1;i>=0;i--){
            int cnt = 1;
            while(!st.empty()){
                if(st.top().first > v[i]){
                    cnt+=st.top().second;
                    st.pop();
                }
                else break;
            }
            st.push({v[i], cnt});
        }
        
        int ans = 0;
        while(!st.empty()){
            ans += st.top().first * st.top().second;
            st.pop();
        }
        cout<<ans<<endl;
    }

    return 0;
}