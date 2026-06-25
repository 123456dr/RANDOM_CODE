// https://codeforces.com/contest/25/problem/A
// 找奇或偶陣列中哪個是奇葩
/* 讀錯題目 BELIKE:
遍歷元素陣列，當index大於0時，在index=1時只紀錄公差d並且建立變數last設為該id的值，接著大於1後，每次檢查last+d有沒有等於第i項，如果不等於就把變數notE+1，並把last+=d，且在下一次迴圈也就是notE等於1的情況下，若last+d還是不等於第i項，則輸出i-2為答案，否則輸出i-1為答案
*/

#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

  int n;cin>>n;
  int ec=0,oc=0;
  int N=n;
  while (n--){
    int x;cin>>x;
    if (x%2==0)ec++;
    else oc++;
    if (oc && ec){
      if (oc==ec){
        int y;
        cin>>y;
        if (y%2==0 && x%2==0)cout<<N-n-1;
        else if (y%2!=0 && x%2!=0)cout<<N-n-1;
        else cout<<N-n;
      }
      else cout<<N-n;
      break;
    }
  }

  return 0;
}