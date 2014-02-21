//
//  detectCycleNode.cpp
//  Deep Copy of a Linked List with Random Node
//
//  Created by Zhongmin Yu on 12/24/13.
//  Copyright (c) 2013 Healer. All rights reserved.
//
#include <iostream>
#include <vector>


using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};

ListNode* listFromVector(vector<int> const& v)
{
    ListNode* h = new ListNode(v[0]);
    ListNode* p = h;
    for (int i = 1; i < v.size(); ++i) {
        ListNode* n = new ListNode(v[i]);
        p->next = n;
        p = n;
    }
    return h;
}

ListNode* getNodeByIndex(ListNode *head, int n)
{
    int i = 0;
    ListNode* p = head;
    while (i < n)
    {
        p = p->next;
        i++;
    }
    return p;
}

void printList(ListNode *head)
{
    ListNode* p = head;
    while (p)
    {
        cout<<p->val<<" ";
        p = p->next;
    }
    cout<<endl;
}

//////////////////////////////////////////////
//////////////////////////////////////////////
class Solution {
public:
    ListNode* hasCycle(ListNode* head) {
        ListNode* p = head;
        ListNode* c = head;
        while (p != NULL && c != NULL) {
            c = c->next;
            if (c != NULL) {
                c = c->next;
            }
            
            if (c == p)
                return p;
            p = p->next;
        }
        return NULL;
    }
    
    ListNode *detectCycle(ListNode *head) {
        ListNode* m = hasCycle(head);
        if (m) {
            ListNode* p1 = head;
            ListNode* p2 = m->next;
            
            if (p2->next == p1)
                return p1;

            ListNode* p = p1;
            ListNode* n = p2;
            m->next = NULL;
            
            int len1 = 0;
            while (p) {
                p = p->next;
                len1++;
            }
            
            int len2 = 0;
            while (n) {
                n = n->next;
                len2++;
            }
            
            p = p1;
            n = p2;
            if (len1 > len2) {
                int l = len1 - len2;
                int i = 0;
                while (i < l) {
                    p = p->next;
                    i++;
                }
            } else {
                int l = len2 - len1;
                int i = 0;
                while (i < l) {
                    n = n->next;
                    i++;
                }
            }
            
            while (n != NULL && p != NULL && n != p) {
                p = p->next;
                n = n->next;
            }
            
            return p;
        }
        return NULL;
    }
};

////////////////////////////////////////////////////
int main(int argc, const char * argv[])
{
    Solution s;
    vector<int> v = { 1, 2, 3, 4,};
    ListNode* r = listFromVector(v);
    
    auto t = getNodeByIndex(r, 3);
    auto m = getNodeByIndex(r, 1);
    t->next = m;
    auto v1 = s.detectCycle(r);
    cout<< v1->val;
    return 0;
}

