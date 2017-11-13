from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from urllib2 import urlopen
from signupform.models import WeatherSubscription
from emailUtil import emailUtility as emailUtil
from emailMessageTemplate import MessageTemplate as template
import json

class Command(BaseCommand):

	def __init__(self):
		self.email_util = emailUtil()
		self.message_template = template()
		self.help = self.message_template.get_help()
		self.form = self.message_template.get_form()
		self.form_image = self.message_template.get_form_image()

		self.wunderground_id = self.message_template.get_wunderground_id()

	#create the wunderground api URL based on city and state
	def get_api(self, city, state):
		return (
			"http://api.wunderground.com/api/%s/conditions/almanac/q/%s/%s.json" % (self.wunderground_id, city, state)).replace(
			' ',
			'_')

	#get weather data from the wunderground API based on city and state
	#uses a preconfigured wunderground api key
	def fetch_weather_data(self, city, state):
		api_url_name = self.get_api(city, state)
		print(api_url_name)
		weather_res = json.loads(urlopen(api_url_name).read().decode('utf-8'))
		if 'error' in weather_res:
			print(ws.location + ' not providing a proper JSON response from Wunderground, continuing without email')

		return weather_res

	#creates the subject line based on the weather data
	def get_subject_line(self, weather_description, current_temp, normal_temp):
		subject = "Enjoy a discount on us."

		# http://www.wunderground.com/weather/api/d/docs?d=resources/phrase-glossary&MR=1#current_condition_phrases
		#the subject message should be ideally kept in a separate constants file, for easier change and maintainence purposes.
		#  Because of small size and demo I am leaving these messages in line.
		if any(w in weather_description for w in
			   {'Drizzle', 'Rain', 'Snow', 'Ice', 'Hail', 'Mist', 'Thunderstorm', 'Squalls', 'Sandstorm'}) \
				or current_temp - normal_temp <= -5.0:
			subject = "Not so nice out? That's okay, e" + subject[1:]
		elif weather_description == 'Clear' or current_temp - normal_temp >= 5.0:
			subject = "It's nice out! " + subject
		return subject

	def get_email_message_image(self, weather_description, is_day):
		image_index = 0
		if 'Thunderstorm' in weather_description:
			image_index = 6
		elif 'Rain' in weather_description or 'Drizzle' in weather_description:
			image_index = 7 if 'Freezing' in weather_description else (5 if is_day else 11)
		elif 'Snow' in weather_description:
			image_index = 8 if is_day else 12
		elif weather_description == 'Clear':
			image_index = 1 if is_day else 9
		elif 'Cloud' in weather_description:
			image_index = 3 if is_day else 10
		elif weather_description == 'Overcast':
			image_index = 2
		return image_index


	#send email function. It fetches the wetaher information, creates the body of email message and sends it the user.
	def send_email(self, subscriptions):
		sender = 'kumar.ro@husky.neu.com'
		email_dict = {}
		is_day = datetime.now().time().hour in range(8, 20)
		almanac_temp = 'temp_high' if is_day else 'temp_low'
		
		for subcription in subscriptions:
			location = subcription.split(',')[1].split("/")
			email = subcription.split(',')[0]

			state = location[1]
			city = location[0]

			weather_dict = self.fetch_weather_data(city, state)

			current_temp = float(weather_dict['current_observation']['temp_f'])
			normal_temp = float(weather_dict['almanac'][almanac_temp]['normal']['F'])
			weather_description = weather_dict['current_observation']['weather']

			subject = self.get_subject_line( weather_description, current_temp,normal_temp)

			image_index = self.get_email_message_image(weather_description, is_day)

			m = self.email_util.get_email_header(sender, email, subject)

			m['from'] = sender
			m['to'] = email
			m['subject'] = subject

			m = self.email_util.attach_text(m, self.form % (city, state, current_temp, weather_description),
										   self.form_image % weather_description if image_index else '')

			if image_index:
				m = self.email_util.attach_image(m, image_index)
			#the email message with email of subscribed user is stores in the dictionary.
			email_dict[email] = m


		self.email_util.send_email_to(sender, email_dict)

