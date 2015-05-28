# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    # @param {ListNode} head
    # @param {integer} val
    # @return {ListNode}
    def removeElements(self, head, val):
        if head == None:
            return None
        if head.val == val:
            return self.removeElements(head.next, val)
        else:
            current_node = head
            while current_node != None and current_node.next != None:
                next_node = current_node.next
                if next_node.val == val:
                    current_node.next = next_node.next
                else:
                    current_node = next_node
        return head

head = ListNode(9)
current = head
for x in range(10):
    current.next = ListNode(9)
    current = current.next

my_solution = Solution()
print mysolution.removeElements(head,9)
