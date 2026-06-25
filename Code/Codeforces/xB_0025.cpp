// https://codeforces.com/contest/25/problem/B
#include<bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
  int n;cin>>n;
  string s;cin>>s;
  for(int i=0;i<n-1;i+=2){
    if(i==0 && n%2!=0){
      
        cout<<s[0]<<s[1]<<s[2];
        
        i=1;
      }
      else{
        cout<<s[i]<<s[i+1];
        }
      if(i!=n-2)cout<<"-";
    
    }
  
  
  return 0;
  }