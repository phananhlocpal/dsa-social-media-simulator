# Create a Node class to create a node
class UserNode:
	def __init__(self, name, fullname, gender, age):
		self.name = name
		self.fullname = fullname
		self.gender = gender
		self.age = age
		self.next = None

# Create a LinkedList class
class UserLinkedList:
	def __init__(self):
		self.head = None

	# Method to add a node at begin of LL
	def insertAtBegin(self, data: UserNode):
		new_node = data
		if self.head is None:
			self.head = new_node
			return
		else:
			new_node.next = self.head
			self.head = new_node

	# Method to add a node at any index
	# Indexing starts from 0.
	def insertAtIndex(self, data:UserNode, index):
		new_node = data
		current_node = self.head
		position = 0
		if position == index:
			self.insertAtBegin(data)
		else:
			while(current_node != None and position+1 != index):
				position = position+1
				current_node = current_node.next

			if current_node != None:
				new_node.next = current_node.next
				current_node.next = new_node
			else:
				print("Index not present")

	# Method to add a node at the end of LL

	def insertAtEnd(self, data: UserNode):
		new_node = data
		if self.head is None:
			self.head = new_node
			return

		current_node = self.head
		while(current_node.next):
			current_node = current_node.next

		current_node.next = new_node

	# Update node of a linked list
		# at given position
	def updateNode(self, val, index):
		current_node = self.head
		position = 0
		if position == index:
			current_node.data = val
		else:
			while(current_node != None and position != index):
				position = position+1
				current_node = current_node.next

			if current_node != None:
				current_node.data = val
			else:
				print("Index not present")

	# Method to remove first node of linked list

	def remove_first_node(self):
		if(self.head == None):
			return

		self.head = self.head.next

	# Method to remove last node of linked list
	def remove_last_node(self):

		if self.head is None:
			return

		current_node = self.head
		while(current_node.next.next):
			current_node = current_node.next

		current_node.next = None

	# Method to remove at given index
	def remove_at_index(self, index):
		if self.head == None:
			return

		current_node = self.head
		position = 0
		if position == index:
			self.remove_first_node()
		else:
			while(current_node != None and position+1 != index):
				position = position+1
				current_node = current_node.next

			if current_node != None:
				current_node.next = current_node.next.next
			else:
				print("Index not present")

	# Method to remove a node from linked list
	def remove_node(self, data):
		current_node = self.head

		if current_node.data == data:
			self.remove_first_node()
			return

		while(current_node != None and current_node.next.data != data):
			current_node = current_node.next

		if current_node == None:
			return
		else:
			current_node.next = current_node.next.next

	# Print the size of linked list
	def sizeOfLL(self):
		size = 0
		if(self.head):
			current_node = self.head
			while(current_node):
				size = size+1
				current_node = current_node.next
			return size
		else:
			return 0

	# print method for the linked list
	def printLL(self):
		current_node = self.head
		while current_node:
			print("Name:", current_node.name)
			print("Fullname:", current_node.fullname)
			print("Gender:", current_node.gender)
			print("Age:", current_node.age)
			current_node = current_node.next

	def avl_search(self, root, key):
		# If root is None
		if root is None:
			return False
	
		# If found, return True
		elif root.key == key:
			return True
	
		# Recur to the left subtree if
		# the current node's value is
		# greater than key
		elif root.key > key:
			return self.avl_search(root.left, key)
	
		# Otherwise, recur to the
		# right subtree
		else:
			return self.avl_search(root.right, key)
	
	# Method to merge two sorted linked lists
	def merge(self, left, right, key):
		result = UserNode(None, None, None, None)  # Tạo một nút mới để lưu trữ kết quả
		current = result

		# Trường hợp cơ bản
		if left is None:
			return right
		if right is None:
			return left

		# Chọn khóa so sánh
		while left is not None and right is not None:
			if key == 'age':
				if left.age <= right.age:
					current.next = left
					left = left.next
				else:
					current.next = right
					right = right.next
			elif key == 'username':
				if left.name <= right.name:
					current.next = left
					left = left.next
				else:
					current.next = right
					right = right.next

			current = current.next

		# Kiểm tra xem có bất kỳ nút nào còn lại không
		if left is not None:
			current.next = left
		elif right is not None:
			current.next = right

		return result.next  # Trả về nút bắt đầu của danh sách mới được sắp xếp

	# Method to perform merge sort
	def mergeSort(self, head, key):
		if head is None or head.next is None:
			return head

		# Splitting linked list into two halves
		middle = self.getMiddle(head)
		nextToMiddle = middle.next
		middle.next = None

		# Recursively sort two halves
		left = self.mergeSort(head, key)
		right = self.mergeSort(nextToMiddle, key)

		# Merge two sorted halves
		sortedList = self.merge(left, right, key)
		return sortedList

	# Method to find the middle element of linked list
	def getMiddle(self, head):
		if head is None:
			return head

		slow = head
		fast = head

		while fast.next is not None and fast.next.next is not None:
			slow = slow.next
			fast = fast.next.next

		return slow

	# Method to call merge sort
	def sort(self, key):
		self.head = self.mergeSort(self.head, key)
