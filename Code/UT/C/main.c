#include <stdio.h>
#include <string.h>  // 提供 strtok, strcat, strcspn
#include <stdlib.h>  // 提供 atoi, atol
#include <time.h>

int dx[] = {0, 1, 0, -1};
int dy[] = {1, 0, -1, 0};
char toDirChar[] = {'N', 'E', 'S', 'W'};

int getDir(char c){
    if(c == 'N')return 0;
    if(c == 'E')return 1;
    if(c == 'S')return 2;
    if(c == 'W')return 3;
}

int main(){
    FILE *fin = fopen("robot.in", "r");
    if(fin == NULL) return 1;
    
    int testCase;
    fscanf(fin, "%d", &testCase);
    
    int maxX, maxY;
    fscanf(fin, "%d %d", &maxX, &maxY);
    
    int scent[55][55] = {0};
    
    for(int i=0;i<testCase;i++){
        int x, y;
        char dirChar;
        fscanf(fin, "%d %d %c", &x, &y, &dirChar);
        
        char cmds[105];
        fscanf(fin, "%s", cmds);
        
        int dir = getDir(dirChar);
        int isLost = 0;
        
        for(int j=0;cmds[j] != '\0';j++){
            if(cmds[j] == 'L'){
                dir = (dir-1+4)%4;
            }
            else if(cmds[j] == 'R'){
                dir = (dir+1)%4;
            }
            else if(cmds[j] == 'F'){
                int nx = x + dx[dir];
                int ny = y + dy[dir];
                
                if(nx < 0 || nx > maxX || ny < 0 || ny > maxY){
                    if(scent[x][y] == 0){
                        isLost = 1;
                        scent[x][y] = 1;
                        break;
                    }
                }
                else{
                    x = nx;
                    y = ny;
                }
            }
        }
        if(isLost){
            printf("%d %d %c LOST\n", x, y, toDirChar[dir]);
        }
        else{
            printf("%d %d %c\n", x, y, toDirChar[dir]);
        }
    }
    fclose(fin);
    return 0;
}




/*
#define int unsigned int
struct bitCard{
    int face : 4;
    int suit : 2;
    int color : 1;  // 1產生延伸位元辨別導致溢位
};

typedef struct bitCard Card; // 自定義

void fillDeck(Card * wDeck);
void shuffle(Card * wDeck);
void deal(Card * wDeck);

int main(){
    Card deck[52];
    srand(time(NULL));
    fillDeck(deck);
    shuffle(deck);
    
    deal(deck);
    
    return 0;
}

void fillDeck(Card * wDeck){
    for(int i = 0;i<52;i++){
        wDeck[i].face = i%13;
        wDeck[i].suit = i/13;
        wDeck[i].color = i/26;
    }
}

void shuffle(Card * wDeck){
    for(int i=0;i<52;i++){
        int j = rand() % 52;
        Card temp = wDeck[i];
        wDeck[i] = wDeck[j];
        wDeck[j] = temp;
    }
}

void deal(Card * wDeck){
    char *face[] = {"Ace", "Deuce", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"};
    char *suit[] = {"Hearts", "Diamonds", "Clubs", "Spades"};
    char *color[] = {"Red", "Black"};
    
    for(int i=0;i<26;i++){
        printf("%5s: %5s of %-8s     %5s: %5s of %-8s\n", 
        color[wDeck[i].color], face[wDeck[i].face], suit[wDeck[i].suit], 
        color[wDeck[i+26].color], face[wDeck[i+26].face], suit[wDeck[i+26].suit]);
    }
}
*/

// ---------------------------------------------------------------------------------------------------------------------------------------------

/* 電話號碼作業
int main(){
    char cs[20];
    char num[10]="";
    
    printf("Enter a phone number in the form (555) 555-5555:");
    fgets(cs, 20, stdin);
    cs[strcspn(cs, "\n")] = '\0';
    
    char *ss = "() -"; // (、)、 、- 四個
    printf("\nArea code: %d\n",atoi(strtok(cs, ss)));
    strcat(num, strtok(NULL, ss)); // 加判是否為空
    strcat(num, strtok(NULL, ss));
    printf("Phone number: %ld", atol(num));
    
    return 0;
}
*/