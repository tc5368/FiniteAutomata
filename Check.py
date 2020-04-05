
import copy

def get_machine_info():
	d1 = open('D1.txt','r')
	d2 = open('D2.txt','r')
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
		print(self.label,self.start,self.accept,self.a_transistion.get_label(),self.b_transistion.get_label())

	def get_label(self):
		return self.label

	def get_transistions(self):
		return self.a_transistion, self.b_transistion

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

	print('Reading in the 2 machines in D1.txt and D2.txt\n')
	machine_one,machine_two = get_machine_info()
	DFAs = [create_DFA(machine_one),create_DFA(machine_two)]
	for FA in DFAs:
		FA.show()
	# DFAs[0].test('aba')
	# DFAs[1].test('abbbbbbbba')

	task_one(DFAs)
	task_two()
	

def task_one(DFAs):
	print('\nStarting task 1 Complementation\n')
	for FA in DFAs:
		compliment_machine = copy.deepcopy(FA)
		compliment_machine.invert_accept_states()
		print('Compliment machine is: ')
		compliment_machine.encode_print()

def task_two(DFAs):
	print('\nStarting task 2 Intersection\n')

	#Create a hybrid machine so if 1 machine as states 1,2,3 and another a,b,c
	#then the machine will have states a1,a2,a3,b1,b2,b3,c1,c2,c3 and links between then
	#nightmare....















if __name__ == '__main__':
	main()