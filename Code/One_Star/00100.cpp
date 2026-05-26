#include <bits/stdc++.h>
using namespace std;

#define int long long

signed main(){

    ios::sync_with_stdio(0);
    cin.tie(0);

    int a,b;
    while(cin>>a>>b){
        cout<<a<<" "<<b<<" ";
        if(max(a,b)!=b){int temp=a;a=b;b=temp;}
        int ans = 0;
        for(int i=a;i<=b;i++){
            int sum = 0;
            int I = i;
            while(I != 1){
                sum ++;
                if(I % 2 != 0)I = I*3 + 1;
                else I/=2;
            }
            ans = max(ans,sum);
        }
        cout<<ans+1<<endl;
    }

    return 0;
}

