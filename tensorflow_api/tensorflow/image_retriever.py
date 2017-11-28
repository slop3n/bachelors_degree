from urllib import request

import glob
import os
import argparse

def download_files(source, target):
	attempted = 0
	success = 0
	failed = 0

	for file in glob.glob(source + '*.txt'):
		array = []

		# read .txt file and save all lines in array
		if file.endswith('.txt'):
			with open(file) as fileToRead:
				array = fileToRead.readlines()
			fileToRead.closed

		# remove empty lines
		array = [x.strip() for x in array]

		# extract only the filename from the current file's path
		lastSlash = file.rfind('/') + 1
		dot = file.rfind('.txt')
		filename = file[lastSlash:dot]
		folder = target + filename

		# create a folder for the corresponding file in the target folder
		if not os.path.exists(folder):
			os.makedirs(folder)

		# try to download all the elements from the array
		for element in array:
			index = element.rfind('/') + 1
			try:
				attempted += 1
				# most of the images not hosted on flickr are not accessible
				if 'flickr' in element:
					success += 1
					request.urlretrieve(element, target + filename + '/' + element[index:])
			except:
				failed += 1

	print('tried to download {0} images'.format(attempted))
	print('finished with {0} new images and, {1} download errors'.format(success, failed))

if __name__ == "__main__":

	# some default values in case no arguments are given
	source = "url_files_test/"
	target = "datasets_test/"

	parser = argparse.ArgumentParser()
	parser.add_argument("--source", help="source folder")
	parser.add_argument("--target", help="target folder")
	args = parser.parse_args()

	if args.source:
		source = args.source
		if not source.endswith('/'):
			source = source + '/'
	if args.target:
		target = args.target
		if not target.endswith('/'):
			target = target + '/'

	download_files(source, target)
