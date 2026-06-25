/*
https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/
新思路:
快慢指標，快指標一次走兩格，慢指標一次一格，等快指標到尾時慢指標剛好在中間，修改當下慢指標的next達成題目要求

舊思路:
改動兩個節點的前後指標就好 (但根據給定 ListNode 結構只記錄後指標所以只要改前指標後指向就好
走訪一次串列才知道節點總個數，但其實節點總個數從範例來看，就是 val 最大值，但不一定
*/
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* deleteMiddle(ListNode* head) {
        
        if(head == nullptr || head->next == nullptr){
            return nullptr;
        }
        if(head->next->next == nullptr){
            head->next = nullptr;
            return head;
        }
        ListNode* slow = head;
        ListNode* fast = head->next->next;

        while(fast!=nullptr && fast->next != nullptr){
            fast = fast->next->next;
            slow = slow->next;
        }
        slow->next = slow->next->next;
        
        return head;
    }
};