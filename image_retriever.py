from urllib import request
import glob, os
import argparse

def download_files(source, target):
	attempted = 0
	success = 0
	failed = 0
	for file in glob.glob(source + '*.txt'):
		array = []
		if file.endswith('.txt'):
			with open(file) as fileToRead:
				array = fileToRead.readlines()
			fileToRead.closed

		array = [x.strip() for x in array]
		lastSlash = file.rfind('/') + 1
		dot = file.rfind('.txt')

		filename = file[lastSlash:dot]
		folder = target + filename

		if not os.path.exists(folder):
			os.makedirs(folder)

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

	print('tried to download ' + str(attempted) + ' images')
	print('finished with ' + str(success) + ' new images and, ' + str(failed) + ' download errors')

if __name__ == "__main__":

	# some default values in case no arguments are given
	source = "url_files_test/"
	target = "datasets_test/"

	parser = argparse.ArgumentParser()
	parser.add_argument("--source", help="the email of the receiver")
	parser.add_argument("--target", help="email subject")
	args = parser.parse_args()

	if args.source:
		source = args.source
	if args.target:
		target = args.target

	download_files(source, target)
