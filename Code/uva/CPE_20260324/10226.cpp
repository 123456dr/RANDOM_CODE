// https://cpe.mcu.edu.tw/cpe/problems/CPE260324/CPE260324-P3.uva10226.pdf
// 好 隨便 要躺平
#include<iostream>
#include<string>
#include<map>
using namespace std;
int main(){
  string s;int cas=0;
  getline(cin,s);getline(cin,s);
  map<string,int>msi;int all=0;
  while(cin){
    getline(cin,s);
    if(!cin||s==""){if(cas++)cout<<endl;
      for(auto&si:msi){
        printf("%s %.4lf\n",si.first.data(),si.second*100./all);
      }
      msi.clear();all=0;continue;
    }
    msi[s]++;all++;
  }
  return 0;
}



/*

#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int t;
    cin>>t;
    
    cin.ignore();
    while(t--){
        string s;
        getline(cin, s);
        map<string,float>mp;
        int cont = 0;
        while(getline(cin, s) && s!=""){
            mp[s]+=1;
            cont++;
        }
        for(auto i:mp){
            printf("%s %.4f\n",i.first.c_str(),i.second/cont*100);
        }
        if(t)printf("\n");
    }


    return 0;
}

*/