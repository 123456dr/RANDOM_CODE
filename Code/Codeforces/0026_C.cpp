// https://codeforces.com/contest/26/problem/C
// 數學題
// 當 n*m 為奇數則 false (由於木板類型各位偶數面積)
// 當 n or m(不可能同時)為奇數，分別用 1*2 and 2*1 填滿多出的奇數列/行，如果木板個數不夠則 false
// 當奇數列行補足後，貪心法從最大面積開始排，若排不滿則 false

#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
  ios::sync_with_stdio(0);
  cin.tie(0);
  int n, m, a, b, c;
  while(cin>>n>>m>>a>>b>>c){
      if(n*m%2 !=0 || (m%2 != 0 && 2*b<n) || (n%2!=0 && 2*a<m )){
        cout<<"IMPOSSIBLE";
        continue;
        }
       if(n%2)n--,a-=m/2;
       if(m%2)m--,b-=n/2;
       for(int )
    }
  
  return 0;
  }