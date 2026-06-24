// https://www.luogu.com.cn/problem/P2613
/*
c mod P = [a mod P] * [b^(-1) mod P]
分子做同餘定理/ 分母做數論
- 同餘定理: 大數讀入技巧 => *10 後再 MOD 讀下一個字元轉數字 -'0'
- 數論 費馬小定理說：如果 P 是一個質數，任一非 P 倍數的整數 b
    - b^(P-1)%P == 1     // 手刻快速冪, pow回傳double會溢位且慢
    - 要找到 b^(-1)
        - 已知 b * b^(-1) = 1 ,且 b^(P-1) MOD P == 1     // \equiv
        - 推導   =>   b^(P-1) MOD P = b * b^(P-2)
        - 得到 b^(-1) == b^(P-2)


- Modular Inverse (模反元素 / 乘法逆元)
- Fermat's Little Theorem (費馬小定理)
- Exponentiation by Squaring (快速冪)
- Big Number Modulo (大數取模)
- Congruence (同餘)
*/
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define MOD 19260817

/* 快速冪: 
遇到次方為奇數次則把將被exp/=2給跳過的[當前base的一次方]*到res儲存 => 3^5 = 3 * (3^2)^2
base = 2, exp = 12
res1 base2 exp12, res1 base4 exp6, res1 base16 exp3, res16 base256 exp1, res16*256
*/
int fexp(int base, int exp){
    base %= MOD;
    if(exp == 1)return base;
    int res = 1;
    while(exp>0){
        if(exp %2 == 1)res *= base, res %= MOD; //不需要 exp-- 因為後面exp/2必變為偶數
        base = base * base % MOD;
        exp/=2;
    }
    return res;
}

void solve(){
    string sa;cin>>sa;
    string sb;cin>>sb;
    int ans = 0;
    int a=0, b=0;
    for(auto i:sa){
        a*=10;
        a += (i - '0');
        a %= MOD;
    }
    for(auto i:sb){
        b*=10;
        b += (i - '0');
        b %= MOD;
    }
    if(b == 0){
        cout<<"Angry!"; //分母為0
        return;
    }
    b = fexp(b, MOD - 2);
    
    ans = a * b % MOD;
    cout<<ans;
}


signed main(){

    solve();

    return 0;
}