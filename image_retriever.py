from urllib import request
import glob, os

folder_with_urls = 'url_files/'
target_folder = 'datasets/'

attempted = 0
success = 0
failed = 0
for file in glob.glob(folder_with_urls + '*.txt'):
	array = []
	if file.endswith('.txt'):
		with open(file) as fileToRead:
			array = fileToRead.readlines()
		fileToRead.closed

	array = [x.strip() for x in array]
	lastSlash = file.rfind('/') + 1
	dot = file.rfind('.txt')

	filename = file[lastSlash:dot]
	folder = target_folder + filename
	if not os.path.exists(folder):
		os.makedirs(folder)

	for element in array:
		index = element.rfind('/') + 1
		try:
			attempted += 1
			if 'flickr' in element:
				success += 1
				request.urlretrieve(element, target_folder + filename + '/' + element[index:])
		except:
			failed += 1

print('tried to download ' + str(attempted) + ' images')
print('finished with ' + str(success) + ' new images and, ' + str(failed) + ' download errors')
