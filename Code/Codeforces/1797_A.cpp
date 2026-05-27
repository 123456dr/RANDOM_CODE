// https://codeforces.com/contest/1797/problem/A
/*
組織細胞一和細胞二走任意路線相遇，求最少的放置阻礙數量，最快的方法就是圍堵有靠牆的細胞，若皆不靠牆則最壞答案就是4
*/
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

  int n;cin>>n;
  while (n--){
    int r, c;cin>>r>>c;
    int a, b, d;
    //cin>>a>>b;
    int ans=4;
    int tim=2;
    int mn=4;
    while (tim--){
      ans=4;cin>>a>>b;
      if (a==1)ans--;
      if (a==r)ans--;
      if (b==1)ans--;
      if (b==c)ans--;
      mn=min(mn,ans);//cout<<ans<<"."<<endl;
    }
    cout<<mn<<endl;
  }

  return 0;
}