from __future__ import absolute_import
from matplotlib import pyplot as plt
from preprocess import get_next_batch, get_image_data

import os
import tensorflow as tf
import numpy as np
import random

class Model(tf.keras.Model):
	def __init__(self):
		super(Model, self).__init__()

		# Model Hyperparameters
		self.train_test_split = .1
		self.batch_size = 64
		self.input_width = 600
		self.input_height = 800
		self.image_channels = 3
		self.num_classes = 2
		self.hidden_layer_size = 320
		self.optimizer = tf.keras.optimizers.Adam(lr=1e-3, beta_1=0.9, beta_2=0.999, epsilon=1e-8) # beta_1 is he exponential decay rate for the 1st moment estimates and beta_2 is the exponential decay rate for the 2nd moment estimates
		self.epsilon = 1e-3

		# Initialize all trainable parameters
		self.filters_1 = tf.Variable(tf.random.truncated_normal([5, 5, self.image_channels, 16],
								dtype=tf.float32,
								stddev=1e-1),
								name="filters_1")
		self.conv_bias_1 = tf.Variable(tf.random.truncated_normal([16]), name="conv_bias_1")

		self.filters_2 = tf.Variable(tf.random.truncated_normal([5, 5, 16, 20],
								dtype=tf.float32,
								stddev=1e-1),
								name="filters_2")
		self.conv_bias_2 = tf.Variable(tf.random.truncated_normal([20]), name="conv_bias_2")

		self.filters_3 = tf.Variable(tf.random.truncated_normal([5, 5, 20, 20],
								dtype=tf.float32,
								stddev=1e-1),
								name="filters_3")
		self.conv_bias_3 = tf.Variable(tf.random.truncated_normal([20]), name="conv_bias_3")

		self.weights_1 = tf.Variable(tf.random.truncated_normal([self.hidden_layer_size, self.hidden_layer_size], dtype=tf.float32,
								stddev=1e-1), name="weights_1")
		self.fc_bias_1 = tf.Variable(tf.random.truncated_normal([self.hidden_layer_size], dtype=tf.float32,
								stddev=1e-1), name="fc_bias_1") # fc here means fully connected

		self.weights_2 = tf.Variable(tf.random.truncated_normal([self.hidden_layer_size, self.hidden_layer_size], dtype=tf.float32,
								stddev=1e-1), name="weights_2")
		self.fc_bias_2 = tf.Variable(tf.random.truncated_normal([self.hidden_layer_size], dtype=tf.float32,
								stddev=1e-1), name="fc_bias_2")

		self.weights_3 = tf.Variable(tf.random.truncated_normal([self.hidden_layer_size, self.num_classes], dtype=tf.float32,
								stddev=1e-1), name="weights_3")
		self.fc_bias_3 = tf.Variable(tf.random.truncated_normal([self.num_classes], dtype=tf.float32,
								stddev=1e-1), name="fc_bias_3")

	def call(self, inputs):
		"""
		Runs a forward pass on an input batch of images.
		:param inputs: images, shape of (num_inputs, 600, 800, 3)
		:return: logits - a matrix of shape (num_inputs, num_classes); during training, it would be (batch_size, 2)
		"""
		# Remember that
		# shape of input = (num_inputs (or batch_size), in_height, in_width, in_channels)
		# shape of filter = (filter_height, filter_width, in_channels, out_channels)
		# shape of strides = (batch_stride, height_stride, width_stride, channels_stride)

		# First convolution layer
		conv = tf.nn.conv2d(inputs, self.filters_1, [1, 2, 2, 1], padding="SAME")
		conv_with_bias = tf.nn.bias_add(conv, self.conv_bias_1)
		batch_mean_1, batch_var_1 = tf.nn.moments(conv_with_bias,[0, 1, 2])
		batch_norm_1 = tf.nn.batch_normalization(conv_with_bias,batch_mean_1,batch_var_1,None,None,self.epsilon)
		conv_1 = tf.nn.relu(batch_norm_1, name="conv1")
		pooled_conv_1 = tf.nn.max_pool(conv_1,
										ksize=[1, 3, 3, 1], # the size of the window for each dimension of the input tensor
										strides=[1, 2, 2, 1], # the stride of the sliding window for each dimension of the input tensor
										padding="SAME",
										name="pool1")

		# Second convolution layer
		conv = tf.nn.conv2d(pooled_conv_1, self.filters_2, strides=[1, 1, 1, 1], padding="SAME")
		conv_with_bias = tf.nn.bias_add(conv, self.conv_bias_2)
		batch_mean_2, batch_var_2 = tf.nn.moments(conv_with_bias,[0, 1, 2])
		batch_norm_2 = tf.nn.batch_normalization(conv_with_bias,batch_mean_2,batch_var_2,None,None,self.epsilon)
		conv_2 = tf.nn.relu(batch_norm_2, name="conv2")
		pooled_conv_2 = tf.nn.max_pool(conv_2,
										ksize=[1, 2, 2, 1],
										strides=[1, 2, 2, 1],
										padding="SAME",
										name="pool2")


		# Third convolution layer
		conv = tf.nn.conv2d(pooled_conv_2, self.filters_3, [1, 1, 1, 1], padding="SAME")
		conv_with_bias = tf.nn.bias_add(conv, self.conv_bias_3)
		batch_mean_3, batch_var_3 = tf.nn.moments(conv_with_bias,[0, 1, 2])
		batch_norm_3 = tf.nn.batch_normalization(conv_with_bias,batch_mean_3,batch_var_3,None,None,self.epsilon)
		conv_3 = tf.nn.relu(batch_norm_3, name="conv3")
		conv_3 = tf.reshape(conv_3, [len(inputs), -1]) # We want to reshape to (len(inputs), hidden layer size), during traing, len(inputs) == batch_size

		fc_1 = tf.matmul(conv_3, self.weights_1) + self.fc_bias_1
		fc_1 = tf.nn.relu(fc_1, name="fc_1")
		fc_1 = tf.nn.dropout(fc_1, rate=0.3) # Dropout helps with preventing overfitting here!

		fc_2 = tf.matmul(fc_1, self.weights_2) + self.fc_bias_2
		fc_2 = tf.nn.relu(fc_2, name="fc_2")
		fc_2 = tf.nn.dropout(fc_2, rate=0.3)

		out = tf.matmul(fc_2, self.weights_3) + self.fc_bias_3
		return out

	def loss(self, logits, labels):
		"""
		Calculates the model cross-entropy loss after one forward pass.
		:param logits: A matrix of shape (batch_size, self.num_classes) containing the result of
		multiple convolution and feed forward layers
		Softmax is applied in this function!!!!
		:param labels: A matrix of shape (batch_size, self.num_classes) containing the train labels
		:return: the loss of the model as a Tensor
		"""
		loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels))
		return loss

	def accuracy(self, logits, labels):
		correct_predictions = tf.equal(tf.argmax(logits, 1), tf.argmax(labels, 1))
		return tf.reduce_mean(tf.cast(correct_predictions, tf.float32))

def train(model, train_inputs, train_labels):
	'''
	Trains the model on all of the inputs and labels for one epoch.
	:param model: the initialized model to use for the forward pass and backward pass
	:param train_inputs: train inputs, shape (num_inputs, width, height, num_channels)
	:param train_labels: train labels, shape (num_labels, num_classes)
	:return: train accuracy for this epoch
	'''
	batch_idx = 0
	sum_acc = 0
	indices = tf.range(start=0, limit=tf.shape(train_inputs)[0], dtype=tf.int32)
	shuffled_indices = tf.random.shuffle(indices)
	train_inputs = tf.gather(train_inputs, shuffled_indices)
	train_labels = tf.gather(train_labels, shuffled_indices)
	train_len = train_inputs.shape[0]
	while ((batch_idx+1)*model.batch_size) < train_len:
		imgs, anss = get_next_batch(batch_idx, train_inputs, train_labels, batch_size=model.batch_size)
		with tf.GradientTape() as tape:
				predictions = model(imgs)
				loss = model.loss(predictions, anss)
		gradients = tape.gradient(loss, model.trainable_variables)
		model.optimizer.apply_gradients(zip(gradients, model.trainable_variables))
		sum_acc += model.accuracy(model(imgs), anss).numpy()
		batch_idx += 1
	return sum_acc


def test(model, test_inputs, test_labels):
	"""
	:param test_inputs: test data, shape (num_inputs, width * height * num_channels)
	:param test_labels: test labels, shape (num_labels, num_classes)
	:return: test accuracy
	"""
	sum_acc = 0
	batch_idx = 0
	test_len = len(test_inputs)
	while ((batch_idx+1)*model.batch_size) < test_len:
		imgs, anss = get_next_batch(batch_idx, test_inputs, test_labels, batch_size=model.batch_size)
		curr_acc = model.accuracy(model(imgs), anss).numpy()
		sum_acc += curr_acc
		batch_idx += 1
	return sum_acc

def train_test_split(x, y, test_pct):
	"""input:
	x: list of x values, y: list of independent values, test_pct: percentage of the data that is testing data=0.2.
	output: x_train, x_test, y_train, y_test lists
	"""

	assert(len(x) == y.shape[0])
	zipped_pairs = list(zip(x, y))
	train_data_pairs, test_data_pairs = split_data(zipped_pairs, test_pct)
	x_train = [x[0] for x in train_data_pairs]
	y_train = [x[1] for x in train_data_pairs]
	x_test = [x[0] for x in test_data_pairs]
	y_test = [x[1] for x in test_data_pairs]
	return x_train, x_test, y_train, y_test


def split_data(data, prob):
	"""input:
	 data: a list of pairs of x,y values
	 prob: the fraction of the dataset that will be testing data, typically prob=0.2
	 output:
	 two lists with training data pairs and testing data pairs
	"""

	num_test = len(data) * prob
	num_train = 1 - num_test
	train_data = []
	test_data = []
	random_vals = [random.random() for i in range(len(data))]
	for i in range(len(data)):
		if random_vals[i] < prob:
 			test_data.append(data[i])
		else:
			train_data.append(data[i])
	return train_data, test_data


def visualize_results(image_inputs, probabilities, image_labels, first_label, second_label):
	"""
	Uses Matplotlib to visualize the results of our model.
	:param image_inputs: image data from get_data(), limited to 10 images, shape (10, 600, 800, 3)
	:param probabilities: the output of model.call(), shape (10, num_classes)
	:param image_labels: the labels from get_data(), shape (10, num_classes)
	:param first_label: the name of the first class, "yes"
	:param second_label: the name of the second class, "no"
	:return: doesn't return anything, a plot should pop-up
	"""
	predicted_labels = np.argmax(probabilities, axis=1)
	num_images = image_inputs.shape[0]

	fig, axs = plt.subplots(ncols=num_images)
	fig.suptitle("PL = Predicted Label\nAL = Actual Label")
	for ind, ax in enumerate(axs):
			ax.imshow(image_inputs[ind], cmap="Greys")
			pl = first_label if predicted_labels[ind] == 0.0 else second_label
			al = first_label if np.argmax(image_labels[ind], axis=0) == 0 else second_label
			ax.set(title="PL: {}\nAL: {}".format(pl, al))
			plt.setp(ax.get_xticklabels(), visible=False)
			plt.setp(ax.get_yticklabels(), visible=False)
			ax.tick_params(axis='both', which='both', length=0)
	plt.show()


def main():
	inputs, labels = get_image_data()
	# TODO: Try with different train-test splits.
	train_inputs, test_inputs, train_labels, test_labels = train_test_split(inputs, labels, 0.2)
	print('train inputs: %d; train labels: %d' % (len(train_inputs), len(train_labels)))
	print('test inputs: %d; test labels: %d' % (len(test_inputs), len(test_labels)))

	model = Model()
	num_epochs = 20

	for epoch in range(num_epochs):
		train_acc = train(model, train_inputs, train_labels)
		test_acc = test(model, test_inputs, test_labels)
		checkpoint_data = {"Epoch": epoch, "Train Accuracy": train_acc/(train_len/model.batch_size), "Test Accuracy": (test_acc/(test_len/model.batch_size))}
		with open('checkpoint.txt', 'w') as outfile:
			json.dump(checkpoint_data, outfile)

	test_acc = test(model, test_inputs, test_labels)
	test_checkpoint_data = {"Test accuracy:", test_acc/(test_len/model.batch_size)}

	with open('checkpoint.txt', 'w') as outfile:
		json.dump(test_checkpoint_data, outfile)

	return


if __name__ == '__main__':
	main()
