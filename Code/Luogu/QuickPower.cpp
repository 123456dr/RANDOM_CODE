// 快速快速冪:
int qu(int base, int exp){
    int res = 1;
    base %= MOD;
    while(exp > 0){
        if(exp & 1)res *= base, res %= MOD;  // exp 和 1 做交集, 因為 1 的二進位為個位一前導零所以交集後取結果最後一位
        base = base * base % MOD;
        exp >>= 1;   // 右移等於除 2
    }
    return res;
}


/* 快速冪_慢: 
遇到次方為奇數次則把將被exp/=2給跳過的[當前base的一次方]*到res儲存 => 3^5 = 3 * (3^2)^2
*/
int fexp(int base, int exp){
    base %= MOD;
    if(exp == 1)return base;
    int res = 1;
    while(exp>0){
        if(exp %2 == 1)res *= base, res %= MOD; //不需要 exp-- 因為後面exp/=2
        base = base * base % MOD;
        exp/=2;
    }
    return res;
}