// https://codeforces.com/contest/3/problem/C
// 還是要先打好稿再寫扣 好亂

#include <bits/stdc++.h>
using namespace std;
#define int long long

signed main(){

    vector<string>v(3);
    int hasdot = 0;
    int xwin = 0;
    int owin = 0;
    int xcont = 0;
    int ocont = 0;
    int winnx = 0;
    int winno = 0;
    for(int i=0;i<3;i++){
        cin >> v[i];
        for(int j=0;j<v[i].length();j++){
            if(v[i][j] == '.')hasdot = 1;
            else if(v[i][j] == 'X')xwin++,xcont++;
            else owin++,ocont++;
        }
        
        if(xwin == 3){
            winnx++;//cout<<"the first player won"<<endl;
            //break;
        }
        else if(owin == 3){
            winno++;//cout<<"the second player won"<<endl;
            //break;
        }
        owin=0;
        xwin=0;
    }
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            if(v[j][i] == 'X')xwin++;
            else if(v[j][i] == '0')owin++;
        }
        
        if(xwin == 3){
            winnx++;//cout<<"the first player won"<<endl;
            //break;
        }
        else if(owin == 3){
            winno++;//cout<<"the second player won"<<endl;
            //break;
        }
        owin=0;
        xwin=0;
    }

    if(v[0][0] == 'X' && v[1][1] == 'X' && v[2][2] == 'X') winnx++;
    if(v[0][2] == 'X' && v[1][1] == 'X' && v[2][0] == 'X') winnx++;
    if(v[0][0] == '0' && v[1][1] == '0' && v[2][2] == '0') winno++;
    if(v[0][2] == '0' && v[1][1] == '0' && v[2][0] == '0') winno++;

    if((winnx != 0 && winno != 0) || ocont > xcont || !(abs(xcont-ocont)<=1)) cout<<"illegal";
    else if(winnx != 0 && xcont != ocont + 1) cout<<"illegal";
    else if(winno != 0 && xcont != ocont) cout<<"illegal";
    else if(winnx != 0) cout<<"the first player won";
    else if(winno != 0) cout<<"the second player won";
    else if(hasdot == 0) cout<<"draw";
    else{
        if(xcont > ocont) cout<<"second";
        else cout<<"first";
    }

/*
    if((winnx!=0 && winno != 0) || ocont > xcont || !(abs(xcont-ocont)<=1))cout<<"illegal";
    else if(winnx)cout<<(winnx != 0 ? "the first player won" : "the second player won");
    else if(v[0][0] == 'X' && v[1][1] == 'X' && v[2][2] == 'X')cout<<"the first player won"<<endl;
    else if(v[0][2] == 'X' && v[1][1] == 'X' && v[2][0] == 'X')cout<<"the first player won"<<endl;
    else if(v[0][0] == '0' && v[1][1] == '0' && v[2][2] == '0')cout<<"the second player won"<<endl;
    else if(v[0][2] == '0' && v[1][1] == '0' && v[2][0] == '0')cout<<"the second player won"<<endl;
    else if(hasdot == 0){
        if(abs(xcont-ocont)<=1)cout<<"draw";
        else cout<<"illegal";
    }
    else{
        if(xcont > ocont)cout<<"second";
        else cout<<"first";
    }

*/
    return 0;
}