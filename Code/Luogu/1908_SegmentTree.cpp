// https://www.luogu.com.cn/problem/P1908
/*
- 逆序對
- 線段樹 segment tree
- 離散化數據，因小於10^9個數且每筆數據小於5*10^5 => min = 10^5 => 把數據改成大小排名儲存
*/

#include <bits/stdc++.h>
using namespace std;
#define int long long

vector<int>tree;

int query(int node, int L, int R, int rangeL, int rangeR){
    if(rangeL > R || rangeR < L)return 0;
    if(rangeL <= L && rangeR >= R){
        return tree[node];
    }
    int mid = L + (R-L)/2;
    return query(node*2, L, mid, rangeL, rangeR) + query(node*2+1, mid+1, R, rangeL, rangeR);
}

int update(int node, int L, int R, int tar){
    if(L == R)return tree[node]++;
    
    int mid = L + (R-L)/2;
    if(mid>=tar)update(node*2, L, mid, tar);
    else update(node*2+1, mid+1, R, tar);
    
    //cout<<node<<" ";
    return tree[node] = tree[node*2] + tree[node*2+1];
}

signed main(){
    int n;cin>>n;
    tree.resize(4*n+1);
    vector<pair<int,int>>ori(n);
    for(int i=0;i<n;i++){
        cin>>ori[i].first;
        ori[i].second = i; // 原始index
    }
    sort(ori.begin(), ori.end());
    vector<int>v(n);
    int cont = 0;
    for(int i=0;i<n;){
        v[ori[i].second] = cont;
        int ind = i+1;
        while(ind<n && ori[ind].first==ori[i].first){
            v[ori[ind].second] = cont;
            ind++; // v[原始index] = 排名
        }
        i = ind;
        cont++;
    }
    //for(auto o:v)cout<<o<<" ";cout<<"x"<<endl;

    int ans = 0;
    for(int i=0;i<n;i++){
        ans += query(1, 0, cont, v[i]+1, cont);
        //cout<<ans<<" ";
        update(1, 0, cont, v[i]);
    }
    cout<<ans<<endl;

    return 0;
}