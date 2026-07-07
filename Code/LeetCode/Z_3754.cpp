#define ll long long
class Solution {
public:
    long long sumAndMultiply(int n) {
        ll sum = 0;
        string x;
        if(!n)return 0;
        while(n > 0){
            ll k = n%10;
            if(k)x+=to_string(k);
            sum += k;
            n /= 10;
        }
        reverse(x.begin(), x.end());
        return stoll(x) * sum;
    }
};