from test1 import *

# indexes = []

def printTree(tree, level):
	for c in tree.C.keys():
		n = tree.C[c]
		if n.isleaf:
			print(level, indexes[tree.i], "=", c, ":", n.p)
		else:
			print(level, indexes[tree.i], "=", c)
			printTree(n, level + "|")

if __name__ == "__main__":
        # Print tree
	lists = []
	entries = []
	labels = []
	indexes = []
	with open('credit.csv', 'r') as inputFile:
		line = inputFile.readline()
		indexes = line.replace("\n", "").split(",")[1:]
		line = inputFile.readline()
		while line:
			entry = line.replace("\n", "").split(",")
			label = entry[-1]
			entry = entry[1:-1]
			line = inputFile.readline()
			lists.append(entry)
			labels.append(label)
	for i in range(len(lists[0])):
		templine = []
		for j in range(len(lists)):
			templine.append(lists[j][i])
		entries.append(templine)
	X = np.array(entries)
	Y = np.array(labels)
	t = Tree.train(X, Y)
	printTree(t, "")
	tom = np.array(['low', 'low', 'no', 'yes', 'male'])
	ana = np.array(['low', 'medium', 'yes', 'yes', 'female'])
	print(Tree.inference(t, tom))
	print(Tree.inference(t, ana))

        # Unit tests
	test_stop1()
	test_stop2()
	test_most_common()
	test_entropy()
	test_conditional_entropy()
	test_python_version()
	test_build_tree()
	test_inference()
	test_load_dataset()
	test_predict()
	test_information_gain()
	test_split()
	test_train()
	test_dataset1()
