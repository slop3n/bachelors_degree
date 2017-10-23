import os
import time
import decimal
import argparse
import datetime
import email_service
import label_image

def watch_folder(path):
	before = dict([(f, None) for f in os.listdir(path)])
	current_time = datetime.datetime.now().strftime('%Y-%d-%m %H:%m')

	print('as of {0} the files in the folder are: {1}'.format(current_time, ', '.join(before)))

	five_minutes = 5 # * 60
	existing_items = []
	
	while 1:
		time.sleep(five_minutes)
		after = dict([(f, None) for f in os.listdir(path)])
		added = [f for f in after if not f in before]
		removed = [f for f in before if not f in after]
		current_time = datetime.datetime.now().strftime('%Y-%d-%m %H:%m:%S')

		if added: 
			for image in added:
				categories = label_image.classify(image)
				most_likely = '{0}: {1}'.format(categories[0]['label'], categories[0]['probability'])

				if most_likely not in existing_items:
					existing_items.append(most_likely)
					text = 'a new image has been uploaded, it has a chance of being one of the follwing:\n'
					
					for category in categories:
						percentage = round(category['probability'] * 100, 2)
						text += '{0} with chance {1}'.format(category['label'], percentage)

					if categories[0]['probability'] < 0.40:
						text = 'image could not be classified correctly'

					email_service.sendmail('slop3n@gmail.com', 'new image', text)

			new_files = ', '.join(added)
			print('on {0} added the files: {1}'.format(current_time, new_files))

		if removed: 
			removed_files = ', '.join(removed)
			print('on {0} removed the files: {1}'.format(current_time, removed_files))

		before = after

if __name__ == "__main__":

	# some default values in case no arguments are given
	path = "."

	parser = argparse.ArgumentParser()
	parser.add_argument("--path", help="source folder to scan")
	args = parser.parse_args()

	if args.path:
		path = args.path

	watch_folder(path)
