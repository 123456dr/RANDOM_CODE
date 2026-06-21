// 
/*
新:
ans = 9 + (n/10 - 1) + (末位是否大於等於首位 ? +1 : 0)

舊思路:
數學邏輯
l~r
1~9 => 9個
11~99 => 9個
101~999 =>看頭尾=[11~99]9個*中間一位數有10種可能 = 90個
1001~9999 => [11~99]9個*中間位數有10^2個可能
*/

#include <bits/stdc++.h>
using namespace std;
#define int long long

int f(int num){
    int last = num%10;
    if(num<10)return num;
    int n = num;
    while(n>=10)n/=10;
    return 9 + num/10 - 1 + (n<=last ? 1:0);
}

signed main(){
    int l, r;
    while(cin>>l>>r){
        int ans = 0;
        ans = f(r)-f(l-1);
        cout<<ans<<"\n";
    }

    return 0;
}

/*
signed main(){

    int l, r;
    while(cin>>l>>r){
        int rans = 9;
        int lans = 9;
        if(l<10)lans-=l+1;
        if(r<10)rans-=(9-r);
        else{
            int rdigits = 1;
            int ldigits = 1;
            // rnum-(l-1)num
            while(r>0)r/=10, rdigits*=10;
            while(l>0)l/=10, ldigits*=10;
            rdigits/=10, ldigits/=10;
            if(rdigits == 10){
                ans+=9;
            }
        }
    }

    return 0;
}*/