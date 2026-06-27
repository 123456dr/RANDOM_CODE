/*
特判:
- 底數為1。奇數個1 ? len為1個數 : len為1個數-1

舊思路:
底數x，要找到x的2k次方前增後減規律陣列最長長度
- 次方規律 1, 2, 4, 8, 16,..., 2k, 2k-1,..., 4, 2, 1
    - x = 2; 2, 4, 16, 4, 2  => 前面一個平方
    - x = 3; 3, 9, 81, 9, 3  => 
- 建立mp(value, cnt)頻率陣列並記錄數字最大值mx，遍歷mp中cnt>=2者
    - 每次遍歷針對當前value當作x，x*=x並len+=2, if(mp[value] == 1)ans=len+1並結束;否則繼續檢查直到mp[value]<1
    - x<=mx 為另外終止條件

- mp.find(key) != mp.end()
*/

#define ll long long
class Solution {
public:
    int ans = 1;
    int maximumLength(vector<int>& nums) {
        unordered_map<ll, int>mp; // (value, cnt)
        int mx = 0;
        for(auto i:nums)mp[i]++, mx = max(mx, i);
        
        if(mp.count(1)){
            ans = (mp[1] % 2 == 0 ? mp[1]-1 : mp[1]);
        }

        for(auto i:mp){
            ll val = i.first, cnt = i.second;
            if(val == 1)continue;
            int len = 0;
            int isOk = 0;
            ll last = val;
            while(mp.find(val) != mp.end() && mp[val] >= 2){
                len += 2;
                last = val;
                val *= val;
                isOk++;
            }
            if (isOk == 0)len = 1;
            else if(mp.find(val) != mp.end() && mp[val] >= 1)len += 1;
            else len -= 1;
            ans = max(ans, len);
        }
        return ans;
    }
};

/*
class Solution {
public:
    int ans = 1;
    void solve(int x, map<int, int>mp){
        int len = 0;
        while(mp.find(x) != mp.end()){
            if(mp[x] >=2)len+=2;
            else{
                ans = max(ans, (mp[x] == 1 ? len +1 : len));
                return;
            }
            ans = max(ans, (mp[x] == 1 ? len +1 : len));
            x *= x;
        }
        return;
    }

    int maximumLength(vector<int>& nums) {
        map<int, int>mp; // (value, cnt)
        for(auto i:nums)mp[i]++;
        if(mp.size() == 1 && mp.find(1) != mp.end()){
            return (mp[1] % 2 == 0 ? mp[1]-1 : mp[1]);
        }

        for(auto i:mp){
            if(i.second >= 2){
                solve(i.first, mp);
            }
        }
        return ans;
    }
};
*/