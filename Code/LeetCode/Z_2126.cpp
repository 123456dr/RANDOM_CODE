// https://leetcode.com/problems/destroying-asteroids/description/
class Solution {
public:
    bool asteroidsDestroyed(int mass, vector<int>& asteroids) {
        sort(asteroids.begin(), asteroids.end());
        long long sum = mass;
        for(auto i:asteroids){
            if(sum<i)return false;
            sum+=i;
        }
        return true;
    }
};