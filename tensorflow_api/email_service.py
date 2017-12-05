from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

import argparse

def sendmail(to, subject, text):
	message = MIMEText(text, 'plain')
	sender = 'lyubomir.bachelors.degree@gmail.com'
	password = 'verysecurepassword'

	message['To'] = to
	message['From'] = sender
	message['Subject']= subject

	try:
		connection = SMTP('smtp.gmail.com')
		connection.login(sender, password)
		connection.sendmail(sender, to, message.as_string())
		connection.close()
		print('email sent')
	except Exception as e:
		print('exception occured')

if __name__ == "__main__":

	# some default values in case no arguments are given
	to = "slop3n@gmail.com"
	subject = "cat facts"
	message = "hello, you just subscribed to cat facts daily"

	parser = argparse.ArgumentParser()
	parser.add_argument("--to", help="the email of the receiver")
	parser.add_argument("--subject", help="email subject")
	parser.add_argument("--message", help="the message")
	args = parser.parse_args()
	
	if args.to:
		to = args.to
	if args.subject:
		subject = args.subject
	if args.message:
		message = args.message

	sendmail(to, subject, message)
