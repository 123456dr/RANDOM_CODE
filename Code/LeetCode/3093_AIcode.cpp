// https://leetcode.com/problems/longest-common-suffix-queries/
/*

// 因為起點同，所以不用計算最大長度啦，查詢wordQuery走不下去直接輸出節點儲存的index就好

新思路：
建立 Trie 樹
遍歷每個 container 字串，把當前wordContainer[i]前後反轉(變成找最長前序)，建立樹，樹的規則為 遍歷wordContainer，一次處理一字串，遍歷該字串每個字母，每個節點為字母並儲存一個所有經過此節點的最短字串長度的index，從根節點開始比較，如果該字母等於當前節點則比較當前字串長度是否為經過此節點字串中之最短長度，若是則更新該節點index為該字串於wordContainer的索引，如果該字母不等於當前節點則加入新節點為該字母，重複直到遍歷完該字串，繼續處理剩餘未處理wordContainer。

開始比較wordQuery，先把字串反轉
從根節點開始如果比較的字串第一個字母和根節點相同則繼續往下走，直到不相同時回傳累積鄉圖字母計數，取最大計數的那個輸出該節點儲存的值(也就是wordContainer中有和query一樣後綴長度的最短字串index)
----
用 map<char,vector<char>>mp
wordContainer[i][ind] 第ind個字母
if ind+1小於wordContainer[i].length就 mp[ind].push_back(第ind+1個字母)

然後比較wordQuery，遞迴遍歷mp[x]的所有，return條件為比對字母不相同，把所有return時的比對長度取最長的那個輸出index
*/

/*
［:x:... 人家說最長後綴，不能在container字串找非末端的字母開始往前找最長子字串啦，下面全錯］
TLE 思路：
建立一個vector<pair<int,pair<int,int>>>v，然後遍歷每個wordsQuery，對於該字串，遍歷每個container裡的字串，先從wordsQuery[i]的最後一個字母看開始尋找有沒有對應container[j]的字母，找到對應字母就往前計數有幾個連續字母一樣，接著把計數數值和v.first比大小，如果比較大則更新first並把second.first更新為container的字串長度second.second記錄為container index，如果發現都沒有找到對應字母也就是計數為0，則v.push_back(make_pair(0,(min(mn,container字串的長度),container index)，最後sort一次v陣列，輸出第一個
*/

class Solution {
    // 1. 改造節點：不再使用指標，全部改用整數 int
    struct TrieNode {
        int children[26]; // 存的是下一個節點在陣列中的 index
        int best_idx;

        TrieNode(int idx) {
            best_idx = idx;
            // 初始化為 -1，代表這條路還沒通 (類似原本的 nullptr)
            for (int i = 0; i < 26; i++) {
                children[i] = -1;
            }
        }
    };

    // 2. 這就是我們的整棵字典樹！所有的節點都存在這個連續的陣列裡
    vector<TrieNode> trie;

    void insert(string& word, int word_idx, vector<string>& container) {
        int curr = 0; // 0 永遠是 root 的 index
        
        for (int j = word.length() - 1; j >= 0; j--) {
            int idx = word[j] - 'a'; 
            
            // 如果沒路了
            if (trie[curr].children[idx] == -1) {
                // 把新節點的 index 記錄下來 (新節點會放在 vector 的最尾端)
                trie[curr].children[idx] = trie.size();
                // 產生一個新節點塞進 vector 裡
                trie.push_back(TrieNode(word_idx));
            }
            
            // 走到下一個節點
            curr = trie[curr].children[idx];
            
            // 更新 best_idx
            int curr_best = trie[curr].best_idx;
            if (word.length() < container[curr_best].length() || 
               (word.length() == container[curr_best].length() && word_idx < curr_best)) {
                trie[curr].best_idx = word_idx; 
            }
        }
    }

    int search(string& word) {
        int curr = 0; // 從 root (index 0) 開始
        
        for (int j = word.length() - 1; j >= 0; j--) {
            int idx = word[j] - 'a';
            
            // 走到沒路就直接 break
            if (trie[curr].children[idx] == -1) {
                break; 
            }
            curr = trie[curr].children[idx];
        }
        return trie[curr].best_idx;
    }

public:
    vector<int> stringIndices(vector<string>& wordsContainer, vector<string>& wordsQuery) {
        int default_idx = 0;
        for (int i = 1; i < wordsContainer.size(); i++) {
            if (wordsContainer[i].length() < wordsContainer[default_idx].length()) {
                default_idx = i;
            }
        }
        
        // 初始化字典樹：清空上一組測資的殘留，並塞入 root 節點
        trie.clear();
        trie.push_back(TrieNode(default_idx)); 
        
        // 建樹
        for (int i = 0; i < wordsContainer.size(); i++) {
            insert(wordsContainer[i], i, wordsContainer);
        }
        
        // 查詢
        vector<int> ans;
        ans.reserve(wordsQuery.size()); // 小優化：預先保留記憶體空間，避免陣列重新配置
        for (string& q : wordsQuery) {
            ans.push_back(search(q));
        }
        
        return ans;
    }
};