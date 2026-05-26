// https://codeforces.com/contest/26/problem/A
// 暫且根本跨謀 codeforces 怎麼選題/找題/比賽(??? 蛤蛤蛤ㄍㄜˊ

#include<bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
  int n;
  while (cin>>n){
    vector<int> prime;
    prime.push_back(2);
    for (int i=3;i<=3000;i++){
      int f=1;
      for (int j=2;j<i;j++){
        if (i%j==0){f=0;continue;}
      }
      if (f)prime.push_back(i);
    }
    int ans=0;
    for (int i=4;i<=n;i++){
      int cont=0;
      for (auto x:prime){
        if (x>i || cont>2)continue;
        if (i%x==0){
          cont++;//cout<<i<<": "<<x<<endl;
        }
      }//cout<<endl;
      if (cont == 2){
        ans++;
      }
    }

    cout<<ans<<endl;

  }

  return 0;
}
