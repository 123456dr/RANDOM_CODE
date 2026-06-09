// https://codeforces.com/contest/100/problem/A
int main(){
    int n,k,a;
    sscanf(Stdio.stdin.gets(),"%d %d %d",n,k,a);
    write(((n-1)/a+1)>sqrt(k)?"NO":"YES");
    return 0;
}
/*#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int n, k, n1;
    while(cin>>n>>k>>n1){
        if(n<=n1*sqrt(k))cout<<"YES";
        else cout<<"NO";
        cout<<endl;
    }
    return 0;
}
#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    int n, k, n1;
    while(cin>>n>>k>>n1){
        if(n*n<=n1*n1*k)cout<<"YES";
        else cout<<"NO";
        cout<<endl;
    }
    return 0;
}
*/