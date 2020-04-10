
def remove_outermost_parenthesis(s):
  left_index = 0
  size = len(s)
  cnt = 0
  ans = ''
  for i in range(0, size):
    if cnt ==0:
      left_index = i
    cnt += 1 if s[i] == '(' else -1
    if cnt == 0:
      ans = ans + s[left_index+1:i] #one balanced paranthesis segment starts at left_index and ends at i
  return ans

def square_numbers(nums):
  size = len(nums)
  ans = []
  i = 0
  for i in range(0, size):
    if nums[i] >= 0:
      break
  if i==0:
    return [x*x for x in nums]
  j = i
  i -= 1
  while j < size and i>=0:
    if abs(nums[j]) > abs(nums[i]):
      ans.append(nums[i]*nums[i])
      i-=1
    else:
      ans.append(nums[j]*nums[j])
      j+=1
  while j<size:
    ans.append(nums[j]*nums[j])
    j+=1
  while i>=0:
    ans.append(nums[i]*nums[i])
    i -= 1
  return ans
class Node:
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right

def target_sum_bst(root, sum):
  if root == None:
    return False
  if root.left == None and root.right == None:
    return sum == root.val
  ans = False
  if root.left != None:
    ans = ans or target_sum_bst(root.left, sum - root.val)
  if root.right != None:
    ans = ans or target_sum_bst(root.right, sum - root.val)
  return ans

#      1
#    /   \
#   2     3
#    \     \
#     6     4
n6 = Node(6)
n4 = Node(4)
n3 = Node(3, None, n4)
n2 = Node(2, None, n6)
n1 = Node(1, n2, n3)

print(target_sum_bst(n1, 6))
