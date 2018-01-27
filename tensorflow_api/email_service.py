from os.path import basename
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import argparse

# дефиниция на метода който праща имейли
def sendmail(to, subject, text, filepath=''):
	message = MIMEMultipart()
	# имейл и парола от който ще се изпрати съобщението
	sender = 'lyubomir.bachelors.degree@gmail.com'
	password = 'verysecurepassword'

	# параметри на съобщението
	message['To'] = to
	message['From'] = sender
	message['Subject']= subject

	try:
		message.attach(MIMEText(text,'plain'))
		
		# ако има подаден път на изображение то се опитва да бъде прикачено към имейла
		if filepath:
			attachment = open(filepath, 'rb')
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(attachment.read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % basename(filepath))
			message.attach(part)

		# прави се връзка със Google пощата и се упълномощява пощата от която ще се прати съобщението
		connection = SMTP('smtp.gmail.com')
		connection.login(sender, password)
		# изпращане на съобщението
		connection.sendmail(sender, to, message.as_string())
		# затваря се връзката с пощата
		connection.close()
	except Exception as e:
		# в случай на грешка не се случва нищо

if __name__ == "__main__":

	# стойности по подразбиране ако програмата се извика без параметри
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

	# извикване на метода който ще прати имейла
	sendmail(to, subject, message)
