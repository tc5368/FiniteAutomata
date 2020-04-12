
# Questions about the code to email to the professor
#  1. When finding the intersection do we assume both FA's will use the same alphabet.





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
		FA.get_node(node_labels[i]).set_transistions([FA.get_node(transistions[i][0]),FA.get_node(transistions[i][2])])
	FA.setup()
	return FA


class node():
	def __init__(self, label, start, accept):
		self.label         = label
		self.start         = start
		self.accept        = accept
		self.a_transistion = None
		self.b_transistion = None
	
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

class DFA():
	def __init__(self, nodes, alphabet):
		self.nodes         = nodes
		self.start         = None
		self.accept        = []
		self.accept_labels = []
		self.alphabet      = alphabet

	def get_node(self,to_find_label):
		for i in self.nodes:
			if i.label == to_find_label:
				return i

	def get_all_nodes(self):
		return self.nodes

	def get_alphabet(self):
		return self.alphabet

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
			for i in self.nodes:
				a,b = i.get_transistions()

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
			print('Valid String')

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

def main():

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
				# Add here when needed
				user_choice = str(input('> ')).upper()
				if user_choice not in ['A','B','C']:
					print('Invlid input please retry')
				else:
					break

	if input_type == 'D':
		print("Loading machine information")
		machine_one,machine_two = get_machine_info("D1","D2")
		DFAs = [create_DFA(machine_one),create_DFA(machine_two)]
		for FA in DFAs:
			FA.show()
	else:
		# If time implement checking using against array of subprocess (ls *.txt)
		print("Finding the intersection of two given FA's please do not include .txt at the end of the filename")
		first  = str(input("First file name: "))
		second = str(input("Second file name: "))

		print("Loading machine information")
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

	# DFAs[0].test('aba')
	# DFAs[1].test('abbbbbbbba')

	# task_one(DFAs)
	# task_two_part_one(DFAs)
	# task_two_part_two()
	

def task_one(DFAs):
	print('\nStarting task 1 Complementation\n')
	# Instructions unclear, this currently will return 2 encoded machines for 2 given FA's
	for FA in DFAs:
		compliment_machine = compliment(FA)
		print('Compliment machine is: ')
		compliment_machine.encode_print()


def task_two(DFAs):
	Intersecion = combine('I', DFAs)
	print("Machine for the Intersection of the FA's:")
	Intersection.encode_print()


def task_three(DFAs):
	machine_one, machine_two = DFAs
	# On the right track with the combinational, maybe check and do by hadn first
	# axax probably shouldn't be a node

	first  = combine('I',[compliment(machine_one), machine_two])
	second = combine('I',[machine_one, compliment(machine_two)])
	full   = combine('U',[first,second])

	first.show()
	second.show()
	full.show()

def compliment(FA):
	compliment_machine = copy.deepcopy(FA)
	compliment_machine.invert_accept_states()
	return compliment_machine


def combine(I_or_U, DFAs):
	# I_or_U is intersection ou union.
	machine_one, machine_two = DFAs
	# Takes the two input FA's and then makes hybrid nodes for them combined, eg: ax,ay,az,bx,by,bz
	# I am calling the first letter pre and the second suf.
	alphabet = machine_one.get_alphabet() #assumes machines use the same alphabet
	Combined_FA = []
	transistions = []

	for pre in machine_one.get_all_nodes():
		for suf in machine_two.get_all_nodes():
			if I_or_U == 'I':
				creating_node = node((pre.get_label()+suf.get_label()), (pre.is_start() == suf.is_start() == True), (pre.is_accept() == suf.is_accept() == True))
			else:
				creating_node = node((pre.get_label()+suf.get_label()), (pre.is_start() == suf.is_start() == True), (pre.is_accept() or suf.is_accept()))
			transistions.append(pre.a_t().get_label()+suf.a_t().get_label()+' '+pre.b_t().get_label()+suf.b_t().get_label())
			Combined_FA.append(creating_node)

	Combined_FA = DFA(Combined_FA, alphabet)

	for n in Combined_FA.get_all_nodes():
		t = transistions.pop(0).split(' ')
		n.set_transistions([Combined_FA.get_node(t[0]),Combined_FA.get_node(t[1])])

	Combined_FA.setup()
	return Combined_FA




























if __name__ == '__main__':
	main()