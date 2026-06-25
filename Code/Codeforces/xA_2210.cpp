#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){
    int n;cin>>n;
    while(n--){
        int x;cin>>x;
        vector<int>v(x);
        int id =1;
        for(int &i:v)i=id++;
        sort(v.begin(), v.end());
        for(int i = v.size()-1;i>=0;i--){
            cout<<v[i]<<" ";
        }
        cout<<endl;
    }

    return 0;
}