from django.core.management.base import BaseCommand, CommandError
from signupform.models import WeatherSubscription

from urllib2 import urlopen
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP, SMTPException
import json

class Command(BaseCommand):
	help = 'Sends a mass email to all subscribers based on the weather.'
	form = """<font color="green" family="KaiTi, Sans Serif">Current weather for %s, %s: %.0f<sup>o</sup>F, %s</font>"""
	form_image = """<br /> <br /><img src="cid:weather" alt="%s">"""
	
	image_fn = 'util/%d.png'
	wunderground_id = '77f11864d200c21d'


	def get_api(self, city, state):
		return (
			"http://api.wunderground.com/api/%s/conditions/almanac/q/%s/%s.json" % (wunderground_id, state, city)).replace(
			' ',
			'_')


	def handle(self, *args, **options):

		sender = 'gavinmccauley92@gmail.com'
		email_dict = {}
		is_day = datetime.now().time().hour in range(8, 20)
		almanac_temp = 'temp_high' if is_day else 'temp_low'
		
		for ws in WeatherSubscription.objects.all():
			location = ws.location.split(',')[0].split("/")
			# noinspection PyInterpreter
			print("*****************************")
			print(location)
			api_url_name = self.get_api(location[0], location[1])
			api_url_file = None
			try:
				api_url_file = urlopen(api_url_name)
			except IOError as e:
				print(ws.location + ' not providing a valid URL, continuing without email')
				continue
			
			weather_dict = json.loads(urlopen(api_url_name).read().decode('utf-8'))
			if 'error' in weather_dict:
				print(ws.location + ' not providing a proper JSON response from Wunderground, continuing without email')
				continue
			print(weather_dict)
			current_temp = float(weather_dict['current_observation']['temp_f'])
			normal_temp = float(weather_dict['almanac'][almanac_temp]['normal']['F'])
			weather_description = weather_dict['current_observation']['weather']
			
			subject = "Enjoy a discount on us."
			
			# http://www.wunderground.com/weather/api/d/docs?d=resources/phrase-glossary&MR=1#current_condition_phrases
			if any(w in weather_description for w in {'Drizzle', 'Rain', 'Snow', 'Ice', 'Hail', 'Mist', 'Thunderstorm', 'Squalls', 'Sandstorm' }) \
				or current_temp - normal_temp <= -5.0:
				subject = "Not so nice out? That's okay, e" + subject[1:]
			elif weather_description == 'Clear' or current_temp - normal_temp >= 5.0:
				subject = "It's nice out! " + subject
			
			# index of image in util folder
			i_index = 0
			if 'Thunderstorm' in weather_description:
				i_index = 6
			elif 'Rain' in weather_description or 'Drizzle' in weather_description:
				i_index = 7 if 'Freezing' in weather_description else (5 if is_day else 11)
			elif 'Snow' in weather_description:
				i_index = 8 if is_day else 12
			elif weather_description == 'Clear':
				i_index = 1 if is_day else 9
			elif 'Cloud' in weather_description:
				i_index = 3 if is_day else 10
			elif weather_description == 'Overcast':
				i_index = 2
			
			m = MIMEMultipart()
			m['from'] = sender
			m['to'] = ws.email
			m['subject'] = subject
			
			m.attach(MIMEText((self.form % (city, state, current_temp, weather_description)) + self.form_image % weather_description if i_index else '', 'html'))
			if i_index:
				i = MIMEImage(open(self.image_fn % i_index, 'rb').read())
				i.add_header('Content-ID', '<weather>')
				m.attach(i)
			
			email_dict[ws.email] = m
		
		s = SMTP('smtp.gmail.com', 587)
		try:
			s.ehlo()
			s.starttls()
			s.ehlo()
			s.login('gavinmccauley92', 'kktirhhyypxbublz')	# app-specific verification code
		except SMTPException as se:
			print('Unable to set up smtp connection, due to:\n' + str(se))
			s.close()
			return
		
		for e in email_dict.keys():
			try:
				s.sendmail(sender, (e,), str(email_dict[e]))
				print('email to ' + str(e) + ' sent.')
			except SMTPException as se:
				print('email to ' + str(e) + ' not sent, due to:\n' + str(se))
				continue
		s.close()

