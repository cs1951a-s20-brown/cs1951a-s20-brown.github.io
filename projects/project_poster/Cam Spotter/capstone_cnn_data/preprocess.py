import numpy as np
import tensorflow as tf
import os
import json
import requests
from remote_data_download import get_labelbox_data
from PIL import Image

num_channels = 3
img_width = 600
img_height = 800
first_rotation = 16
second_rotation = 338

def get_image_data():
	script_dir = os.getcwd() #<-- absolute dir the script is in
	project_data_path = os.path.join(script_dir, "project_data")

	f = []
	for (dirpath, dirnames, filenames) in os.walk(project_data_path):
		f.extend(filenames)
		break

	# print('filenames: %s' % f)

	# List of Images Schema: i (Image ID), image_data_url, image_label, filename
	with open('successful.txt', 'r') as filehandle:
	    image_data_list = json.load(filehandle)

	images = []
	labels = []
	for image_data in image_data_list:
		id = image_data[0]
		url = image_data[1]
		label = image_data[2]
		filename = image_data[3]

		# print('id: %d' % id)
		# print('url: %s' % url)
		# print('label: %s' % label)
		# print('filename: %s' % filename)

		if (label == 'Skip'):
			continue

		pixel_values = get_image_and_augmentations(os.path.join(project_data_path, filename)) # Returns a (600, 800, 3) array of pixel values.
		if pixel_values:
			images.extend(pixel_values)
			try:
				i_label = 0 if label['phone_exists'] == 'yes' else 1
				labels.extend(np.repeat(i_label, len(pixel_values)))
			except KeyError as e:
				# print('KeyError - reason: %s' % str(e))
				try:
					i_label = 0 if label['classify_the_image_as_\"is_there_a_smart_phone_in_this_image?\"'] == 'yes' else 1
					labels.extend(np.repeat(i_label, len(pixel_values)))
				except KeyError as e:
					continue
					# print('KeyError - reason: %s' % str(e))

	return (images, tf.one_hot(labels, depth=2))


def get_image_and_augmentations(image_path):
	"""Get a numpy array of an image so that one can access values[x][y]."""
	try:
		image = Image.open(image_path, 'r')
		image_flip = image.transpose(Image.FLIP_LEFT_RIGHT)
		image_rotate1 = image.rotate(first_rotation, expand=True)
		image_rotate2 = image.rotate(second_rotation, expand=True)
		images = [image, image_flip, image_rotate1, image_rotate2]

		pixel_values_list = []
		for i in images:
			image = i
			if image.mode != 'RGB':
				image = image.convert(mode='RGB')
			image = image.resize((img_width, img_height))
			pixel_values = list(image.getdata())
			pixel_values = np.array(pixel_values).astype(np.float32) / 255.0
			pixel_values = np.reshape(pixel_values, (img_width, img_height, num_channels))
			pixel_values_list.append(pixel_values)
		return pixel_values_list
	except IOError as err:
		return None

def get_next_batch(idx, inputs, labels, batch_size=100):
	"""
	Given an index, returns the next batch of data and labels. Ex. if batch_size is 5,
	the data will be a numpy matrix of size 5 * 32 * 32 * 3, and the labels returned will be a numpy matrix of size 5 * 10.
	"""
	return (inputs[idx*batch_size:(idx+1)*batch_size], np.array(labels[idx*batch_size:(idx+1)*batch_size]))
