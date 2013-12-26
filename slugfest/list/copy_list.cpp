//
//  main.cpp
//  Deep Copy of a Linked List with Random Node
//
//  Created by Zhongmin Yu on 12/24/13.
//  Copyright (c) 2013 Healer. All rights reserved.
//

#define NULL    0

struct RandomListNode {
    
    int label;
    RandomListNode *next, *random;
    RandomListNode(int x) : label(x), next(NULL), random(NULL) {}
    
};

class Solution {
public:
    
    RandomListNode *copyList(RandomListNode* head) {
        RandomListNode* s = NULL;
        RandomListNode* last = NULL;

        RandomListNode* p = head;
        while (p) {
            RandomListNode* n = new RandomListNode(p->label);
            
            if (last) {
                last->next = n;
            }
            last = n;
            if (!s) {
                s = n;
            }
            
            p = p->next;
        }
        return s;
    }
    
    void InterLeaving(RandomListNode *h1, RandomListNode *h2) {
        RandomListNode* p1 = h1;
        RandomListNode* p2 = h2;
        while (p1) {
            RandomListNode* next1 = p1->next;
            RandomListNode* next2 = p2->next;
            p1->next = p2;
            p2->next = next1;
            p2 = next2;
            p1 = next1;
        }
    }
    
    void copyRandomNodes(RandomListNode* h)
    {
        RandomListNode* p = h;
        while (p) {
            if (p->random) {
                p->next->random = p->random->next;
            }
            p = p->next->next;
        }
    }
    
    void restore(RandomListNode* h)
    {
        RandomListNode* p1 = h;
        RandomListNode* p2 = p1->next;
        while (p2) {
            RandomListNode* n1 = p1->next->next;
            p1->next = n1;
            
            RandomListNode* n2 = NULL;
            if (p2->next) {
                n2 = p2->next->next;
            } else {
                break;
            }
            
            
            p2->next = n2;
            p1 = n1;
            p2 = n2;
        }
    }
    

    
    RandomListNode *copyRandomList(RandomListNode *head) {
        RandomListNode* newHead = copyList(head);
        if (newHead) {
            InterLeaving(head, newHead);
            copyRandomNodes(head);
            restore(head);
        }
        return newHead;
    }
};

////////////////////////////////////////////////////
int main(int argc, const char * argv[])
{
    return 0;
}

