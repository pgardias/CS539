import math
import numpy as np
from collections import Counter

# Note: please don't add any new package, you should solve this problem using only the packages above.
# -------------------------------------------------------------------------
'''
    Part 1: Decision Tree (with Discrete Attributes) -- 40 points --
    In this problem, you will implement the decision tree method for classification problems.
    You could test the correctness of your code by typing `nosetests -v test1.py` in the terminal.
'''


# -----------------------------------------------
class Node:
	'''
		Decision Tree Node (with discrete attributes)
		Inputs:
			X: the data instances in the node, a numpy matrix of shape p by n.
			   Each element can be int/float/string.
			   Here n is the number data instances in the node, p is the number of attributes.
			Y: the class labels, a numpy array of length n.
			   Each element can be int/float/string.
			i: the index of the attribute being tested in the node, an integer scalar
			C: the dictionary of attribute values and children nodes.
			   Each (key, value) pair represents an attribute value and its corresponding child node.
			isleaf: whether or not this node is a leaf node, a boolean scalar
			p: the label to be predicted on the node (i.e., most common label in the node).
	'''

	def __init__(self, X, Y, i=None, C=None, isleaf=False, p=None):
		self.X = X
		self.Y = Y
		self.i = i
		self.C = C
		self.isleaf = isleaf
		self.p = p


# -----------------------------------------------
class Tree(object):
	'''
		Decision Tree (with discrete attributes).
		We are using ID3(Iterative Dichotomiser 3) algorithm. So this decision tree is also called ID3.
	'''

	# --------------------------
	@staticmethod
	def entropy(Y):
		'''
			Compute the entropy of a list of values.
			Input:
				Y: a list of values, a numpy array of int/float/string values.
			Output:
				e: the entropy of the list of values, a float scalar
			Hint: you could use collections.Counter.
		'''
		c = Counter()
		for y in Y:
			c[y] += 1

		e = 0
		for _, count in c.most_common():
			e -= count / len(Y) * math.log(count / len(Y), 2)
		return e

	# --------------------------
	@staticmethod
	def conditional_entropy(Y, X):
		'''
			Compute the conditional entropy of y given x. The conditional entropy H(Y|X) means average entropy of children nodes, given attribute X. Refer to https://en.wikipedia.org/wiki/Information_gain_in_decision_trees
			Input:
				X: a list of values , a numpy array of int/float/string values. The size of the array means the number of instances/examples. X contains each instance's attribute value.
				Y: a list of values, a numpy array of int/float/string values. Y contains each instance's corresponding target label. For example X[0]'s target label is Y[0]
			Output:
				ce: the conditional entropy of y given x, a float scalar
		'''
		c = Counter()
		for x in X:
			c[x] += 1

		ce = 0
		l = list(c)
		dv = []
		for j in range(len(l)):
			dv.append([])
		for i in range(len(X)):
			dv[l.index(X[i])].append(Y[i])
		for k in range(len(dv)):
			ce += c[l[k]] / len(X) * Tree.entropy(dv[k])
		return ce

	# --------------------------
	@staticmethod
	def information_gain(Y, X):
		'''
			Compute the information gain of y after splitting over attribute x
			InfoGain(Y,X) = H(Y) - H(Y|X)
			Input:
				X: a list of values, a numpy array of int/float/string values.
				Y: a list of values, a numpy array of int/float/string values.
			Output:
				g: the information gain of y after splitting over x, a float scalar
		'''
		g = Tree.entropy(Y) - Tree.conditional_entropy(Y, X)
		return g

	# --------------------------
	@staticmethod
	def best_attribute(X, Y):
		'''
			Find the best attribute to split the node.
			Here we use information gain to evaluate the attributes.
			If there is a tie in the best attributes, select the one with the smallest index.
			Input:
				X: the feature matrix, a numpy matrix of shape p by n.
				   Each element can be int/float/string.
				   Here n is the number data instances in the node, p is the number of attributes.
				Y: the class labels, a numpy array of length n. Each element can be int/float/string.
			Output:
				i: the index of the attribute to split, an integer scalar
		'''
		i = 0
		max_gain = 0
		for j in range(len(X)):
			x_gain = Tree.information_gain(Y, X[j])
			if x_gain > max_gain:
				max_gain = x_gain
				i = j
		return i

	# --------------------------
	@staticmethod
	def split(X, Y, i):
		'''
			Split the node based upon the i-th attribute.
			(1) split the matrix X based upon the values in i-th attribute
			(2) split the labels Y based upon the values in i-th attribute
			(3) build children nodes by assigning a submatrix of X and Y to each node
			(4) build the dictionary to combine each  value in the i-th attribute with a child node.

			Input:
				X: the feature matrix, a numpy matrix of shape p by n.
				   Each element can be int/float/string.
				   Here n is the number data instances in the node, p is the number of attributes.
				Y: the class labels, a numpy array of length n.
				   Each element can be int/float/string.
				i: the index of the attribute to split, an integer scalar
			Output:
				C: the dictionary of attribute values and children nodes.
				   Each (key, value) pair represents an attribute value and its corresponding child node.
		'''
		C = dict()
		x = np.array(X)
		labels = x[i, :]
		x = x.transpose()
		dict_X = dict()
		dict_Y = dict()

		for label in np.unique(labels):
			dict_X[label] = x[labels == label].transpose()
		for label in np.unique(labels):
			dict_Y[label] = Y[labels == label].transpose()
		# dict_Y = {label: Y[labels == label] for label in np.unique(labels)}
		for label in dict_X:
			C[label] = Node(dict_X[label], dict_Y[label])
		# for label in np.unique(labels):
		# 	C[label] = Node(dict_X[label], x[labels == label])

		return C

	# --------------------------
	@staticmethod
	def stop1(Y):
		'''
			Test condition 1 (stop splitting): whether or not all the instances have the same label.

			Input:
				Y: the class labels, a numpy array of length n.
				   Each element can be int/float/string.
			Output:
				s: whether or not Condition 1 holds, a boolean scalar.
				True if all labels are the same. Otherwise, false.
		'''
		for y in Y:
			for i in range(len([y])):
				if y[i] != Y[0][i]:
					return False
		return True

	# --------------------------
	@staticmethod
	def stop2(X):
		'''
			Test condition 2 (stop splitting): whether or not all the instances have the same attribute values.
			Input:
				X: the feature matrix, a numpy matrix of shape p by n.
				   Each element can be int/float/string.
				   Here n is the number data instances in the node, p is the number of attributes.
			Output:
				s: whether or not Condition 2 holds, a boolean scalar.
		'''
		for x in X:
			if not Tree.stop1(x):
				return False
		return True

	# --------------------------
	@staticmethod
	def most_common(Y):
		'''
			Get the most-common label from the list Y.
			Input:
				Y: the class labels, a numpy array of length n.
				   Each element can be int/float/string.
				   Here n is the number data instances in the node.
			Output:
				y: the most common label, a scalar, can be int/float/string.
		'''
		c = Counter()
		for y in Y:
			c[y] += 1
		return c.most_common(1)[0][0]

	# --------------------------
	@staticmethod
	def build_tree(t):
		'''
			Recursively build tree nodes.
			Input:
				t: a node of the decision tree, without the subtree built.
				t.X: the feature matrix, a numpy float matrix of shape n by p.
				   Each element can be int/float/string.
					Here n is the number data instances, p is the number of attributes.
				t.Y: the class labels of the instances in the node, a numpy array of length n.
				t.C: the dictionary of attribute values and children nodes.
				   Each (key, value) pair represents an attribute value and its corresponding child node.
		'''
		if not Tree.stop1(t.Y) and not Tree.stop2(t.X):
			t.i = Tree.best_attribute(t.X, t.Y)
			t.p = Tree.most_common(t.Y)
			t.C = Tree.split(t.X, t.Y, t.i)
			for attr in t.C:
				Tree.build_tree(t.C[attr])
		else:
			t.isleaf = True
			t.p = Tree.most_common(t.Y)

	# --------------------------
	@staticmethod
	def train(X, Y):
		'''
			Given a training set, train a decision tree.
			Input:
				X: the feature matrix, a numpy matrix of shape p by n.
				   Each element can be int/float/string.
				   Here n is the number data instances in the training set, p is the number of attributes.
				Y: the class labels, a numpy array of length n.
				   Each element can be int/float/string.
			Output:
				t: the root of the tree.
		'''
		t = Node(X, Y)
		Tree.build_tree(t)
		return t

	# --------------------------
	@staticmethod
	def inference(t, x):
		'''
			Given a decision tree and one data instance, infer the label of the instance recursively.
			Input:
				t: the root of the tree.
				x: the attribute vector, a numpy vectr of shape p.
				   Each attribute value can be int/float/string.
			Output:
				y: the class labels, a numpy array of length n.
				   Each element can be int/float/string.
		'''
		try:
			if not t.isleaf:
				return Tree.inference(t.C[x[t.i]], x)
			else:
				return t.p
		except KeyError:
			# In class professor suggested we use the most common case if the key does not exist
			return t.p


	# --------------------------
	@staticmethod
	def predict(t, X):
		'''
			Given a decision tree and a dataset, predict the labels on the dataset.
			Input:
				t: the root of the tree.
				X: the feature matrix, a numpy matrix of shape p by n.
				   Each element can be int/float/string.
				   Here n is the number data instances in the dataset, p is the number of attributes.
			Output:
				Y: the class labels, a numpy array of length n.
				   Each element can be int/float/string.
		'''
		l = list()
		for i in range(len(X[0])):
			l.append(Tree.inference(t, X[:, i]))
		return np.array(l)

	# --------------------------
	@staticmethod
	def load_dataset(filename='data1.csv'):
		'''
			Load dataset 1 from the CSV file: 'data1.csv'.
			The first row of the file is the header (including the names of the attributes)
			In the remaining rows, each row represents one data instance.
			The first column of the file is the label to be predicted.
			In remaining columns, each column represents an attribute.
			Input:
				filename: the filename of the dataset, a string.
			Output:
				X: the feature matrix, a numpy matrix of shape p by n.
				   Each element can be int/float/string.
				   Here n is the number data instances in the dataset, p is the number of attributes.
				Y: the class labels, a numpy array of length n.
				   Each element can be int/float/string.
		'''
		x = list()
		y = list()
		with open(filename, 'r') as f:
			for line in f.readlines():
				elements = line.rstrip().split(",")
				x.append(elements[1:])
				y.append(elements[0])

		X = np.delete(np.array(x), 0, 0).transpose()
		Y = np.delete(np.array(y), 0, 0).transpose()
		return X, Y
