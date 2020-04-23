import copy

def get_machine_info(filename1, filename2):
	d1 = open(filename1+'.txt','r')
	d2 = open(filename2+'.txt','r')
	FA_one = d1.read().split('\n')
	FA_two = d2.read().split('\n')
	d1.close()
	d2.close()
	return FA_one, FA_two


def create_DFA(machine_info):
	num_nodes    = int(machine_info[0])
	node_labels  = machine_info[1].split(' ')
	start_state  = machine_info[-3]
	if machine_info[-2] != 0:
		accept_nodes = machine_info[-1].split(' ')
	alphabet 	 = machine_info[3]

	FA = []
	for i in range(num_nodes):
		creating_node = node(node_labels[i],(node_labels[i] == start_state), (node_labels[i] in accept_nodes))
		FA.append(creating_node)

	FA = DFA(FA, alphabet)

	transistions = machine_info[4:-3]

	for i in range(num_nodes):
		a,b  = transistions[i].split(' ')
		FA.get_node(node_labels[i]).set_transistions([FA.get_node(a),FA.get_node(b)])

	FA.setup()
	return FA


class node():
	def __init__(self, label, start, accept):
		self.label         = label
		self.start         = start
		self.accept        = accept
		self.a_transistion = None
		self.b_transistion = None
		self.reachable     = False
	

	def set_transistions(self,transistions):
		self.a_transistion = transistions[0]
		self.b_transistion = transistions[1]


	def a_t(self):
		return self.a_transistion


	def b_t(self):
		return self.b_transistion


	def show(self):
		print(self.label, self.start, self.accept, self.a_transistion.get_label(), self.b_transistion.get_label())


	def get_label(self):
		return self.label


	def get_transistions(self):
		return self.a_transistion, self.b_transistion


	def is_start(self):
		return self.start


	def is_accept(self):
		return self.accept


	def is_reachable(self):
		return self.reachable


	def found(self):
		self.reachable = True


class DFA():
	def __init__(self, nodes, alphabet):
		self.nodes         = nodes
		self.start         = None
		self.accept        = []
		self.accept_labels = []
		self.alphabet      = alphabet


	def delete(self,node):
		self.nodes.remove(node)
		if node in self.accept:
			self.accept.remove(node)
			self.accept_labels.remove(node.get_label())


	def get_node(self,to_find_label):
		for i in self.nodes:
			if i.label == to_find_label:
				return i


	def get_start(self):
		return self.start


	def get_all_nodes(self):
		return self.nodes


	def get_alphabet(self):
		return self.alphabet


	def get_accept_states(self):
		return self.accept


	def set_accept(self,node):
		node.accept = True
		self.accept.append(node)
		self.accept_labels.append(node.get_label())


	def invert_accept_states(self):
		for node in self.nodes:
			node.accept = not node.accept
		self.setup()


	def setup(self):
		self.accept = []
		self.accept_labels = []
		for i in self.nodes:
			if i.accept:
				self.accept.append(i)
				self.accept_labels.append(i.get_label())
			if i.start:
				self.start = i


	def show(self):
		print('This FA has %s nodes with a start node of %s' %(len(self.nodes),self.start.get_label()))
		print('and %s as accept states' %self.accept_labels)
		print('It\'s nodes are')
		for i in self.nodes:
			i.show()	
		print('')


	def test(self,test_string):
		current_node   = self.start
		for i in range(len(test_string)):
			if test_string[i] == 'a':
				current_node = current_node.a_t()
			else:
				current_node = current_node.b_t()
		if current_node in self.accept:
			print(test_string,'Valid String')


	def label_list(self):
		outString = ''
		for node in self.nodes:
			outString += node.label + " "
		return outString


	def print_transistions(self):
		for node in self.nodes:
			print(node.a_t().label+' '+node.b_t().label)


	def encode_print(self):
		print(len(self.nodes))
		print(self.label_list())
		print(len(self.alphabet.split(' ')))
		print(self.alphabet)
		self.print_transistions()
		print(self.start.label)
		print(len(self.accept))
		print(' '.join(self.accept_labels))
		print('')


def menu():
	print("DFA functionality program")
	user_choice = None
	while user_choice == None:
		print("Would you like to use the default filenames of D1.txt and D2.txt or custom (d/c)")
		input_type = str(input("> ")).upper()
		if input_type not in ['D','C']:
			print('Invlid input, please retry')
		else:
			while True:
				print('What functionality would you like to use')
				print('A. Complement')
				print('B. Intersection')
				print('C. Symetric Difference')
				print('D. Test Non emptyness')
				print('E. Test Equivalence of 2 FA\'s')
				# Add here when needed
				user_choice = str(input('> ')).upper()
				if user_choice not in ['A','B','C','D','E']:
					print('Invlid input please retry')
				else:
					break

	if input_type == 'D':
		machine_one,machine_two = get_machine_info("D1","D2")
		DFAs = [create_DFA(machine_one),create_DFA(machine_two)]
		# for FA in DFAs:
		# 	FA.show()

	else:
		# If time implement checking using against array of subprocess (ls *.txt)
		print("Finding the intersection of two given FA's please do not include .txt at the end of the filename")
		first  = str(input("First file name: "))
		second = str(input("Second file name: "))

		machine_one,machine_two = get_machine_info(first,second)
		DFAs = [create_DFA(machine_one),create_DFA(machine_two)]
		for FA in DFAs:
			FA.show()

	if user_choice == 'A':
		task_one(DFAs)
	if user_choice == 'B':
		task_two(DFAs)
	if user_choice == 'C':
		task_three(DFAs)
	if user_choice == 'D':
		task_four(DFAs)
	if user_choice == 'E':
		task_five(DFAs)

def task_one(DFAs):
	print('\nStarting task 1 Complementation\n')
	# Instructions unclear, this currently will return 2 encoded machines for 2 given FA's
	for FA in DFAs:
		compliment_machine = compliment(FA)
		print('Compliment machine is: ')
		compliment_machine.encode_print()


def task_two(DFAs):
	Intersection = intersection(DFAs)
	print("Machine for the Intersection of the FA's:")
	Intersection.encode_print()


def task_three(DFAs):
	SymDif = symetric_difference(DFAs)
	print('Machine for the Symetric Difference: ')
	SymDif.encode_print()


def task_four(DFAs):
	machine_one,machine_two = DFAs
	for i in DFAs:
		print('Testing is DFA has a language')
		out = non_emptyness(i)
		if out != None:
			print('Found accepted string',out)
		else:
			print('language empty')


def task_five(DFAs):
	machine_one,machine_two = DFAs
	SymDif = symetric_difference(DFAs)
	accepted_string = non_emptyness(SymDif)
	if accepted_string != None:
		print('Machines are not equvialent, found string',accepted_string,'which is only valid for 1 machine')


def compliment(FA):
	compliment_machine = copy.deepcopy(FA)
	compliment_machine.invert_accept_states()
	return compliment_machine

def symetric_difference(DFAs):
	machine_one, machine_two = DFAs
	first  = intersection([compliment(machine_one),machine_two])
	second = intersection([machine_one, compliment(machine_two)])
	SymDif = union([first,second])
	return SymDif


def union(DFAs):
	machine_one, machine_two = DFAs
	nodes_to_change = machine_two.get_accept_states()
	for i in nodes_to_change:
		machine_one.set_accept(i)
	return machine_one


def intersection(DFAs):
	machine_one, machine_two = DFAs
	Combined_FA = []
	transistions = []

	for pre in machine_one.get_all_nodes():
		for suf in machine_two.get_all_nodes():
			creating_node = node((pre.get_label()+suf.get_label()), (pre.is_start() == suf.is_start() == True), (pre.is_accept() == suf.is_accept() == True))
			transistions.append(pre.a_t().get_label()+suf.a_t().get_label()+' '+pre.b_t().get_label()+suf.b_t().get_label())
			Combined_FA.append(creating_node)

	Combined_FA = DFA(Combined_FA, machine_one.get_alphabet())

	for n in Combined_FA.get_all_nodes():
		t = transistions.pop(0).split(' ')
		n.set_transistions([Combined_FA.get_node(t[0]),Combined_FA.get_node(t[1])])
		Combined_FA.get_node(t[0]).found()
		Combined_FA.get_node(t[1]).found()

	Combined_FA.setup()

	unreachable_nodes = []
	for n in Combined_FA.get_all_nodes():
		if (n.is_reachable() == False) and (n.is_start() == False):
			unreachable_nodes.append(n)

	for i in unreachable_nodes:
		Combined_FA.delete(i)

	return Combined_FA


def non_emptyness(FA):
	outString = ''
	node = FA.get_start()
	route = [node]
	visited = []

	if node.is_accept():
		return 'e'

	count = 10
	while count != 0:
		count -= 1

		if node not in visited:
			visited.append(node)

		next = node.a_t()
		if next.is_accept():
			outString += 'a'
			return outString
		if next not in visited:
			route.append(next)
			node = next
			outString += 'a'
			continue

		next = node.b_t()
		if next.is_accept():
			outString += 'b'
			return outString
		if next not in visited:
			route.append(next)
			node = next
			outString += 'b'
			continue

		else:
			outString = outString[:-1]
			node = route.pop(-2)
			continue


if __name__ == '__main__':
	menu()

		