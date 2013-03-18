# references: http://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/

import datetime
import time
import random

weather = []
name = []
timeArr = []
dateArr = []

# weather questions
weather.append("what's the weather")
weather.append("what's the weather like")
weather.append("how's the weather")
weather.append("what's the weather outside")
weather.append("what is the weather")
weather.append("what is the weather like")
weather.append("how is the weather")
weather.append("what is the weather outside")
weather.append("whats the weather")
weather.append("whats the weather like")
weather.append("hows the weather")
weather.append("whats the weather outside")

weather_response = ["It's winter, so probably cold ...", "I know you have a smart phone","Check the weather channel","I really don't go outside","Wait check me check the thermostat...","Cloudy with a chance of meatballs?"]

# name questions
name.append("what is your name")
name.append("whats your name")
name.append("what's your name")
name.append("what are you called")
name.append("what should I call you")
name.append("who are you")
name.append("what do you go by")

name_response = ["They call me Perlisbot","My name is Perlisbot, nice to meet you!", "I am Perlisbot, fear me", "Perlisbot"]

# time questions
timeArr.append("what's the time")
timeArr.append("whats the time")
timeArr.append("what's the time right now")
timeArr.append("what's the time now")
timeArr.append("whats the time right now")
timeArr.append("whats the time now")
timeArr.append("what is the time right now")
timeArr.append("what is the time now")
timeArr.append("what is the time")
timeArr.append("do you know what the time is")
timeArr.append("what time is it")
timeArr.append("do you know what time is it")
timeArr.append("do you know what time it is")
dateArr.append("what day is it")
dateArr.append("what day is today")
dateArr.append("what is today's date")
dateArr.append("today is what day")
dateArr.append("what is todays date")
dateArr.append("what is the date")
dateArr.append("what's the date")
dateArr.append("whats the date")
dateArr.append("today is what")
dateArr.append("what is today")
dateArr.append("whats is today")
dateArr.append("what's is today")

time_response = ["Right now its ", "The current time is ", "To be perfectly accurate it is "]
date_response = ["Todays date is ", "Today is ", "Its "]

# startTime is in this format "time.mktime(time.gmtime())"
def hardCode(sentence, startSecs, startTime, question):

	if question:

		split = sentence.lower().split()
		converTime = []

		if (sentence.lower() in weather):
                        str_ = random.choice(weather_response)
			return [True, str_]

		elif (sentence.lower() in name):
                        str_ = random.choice(name_response)
			return [True, str_]

		elif (sentence.lower() in timeArr):
			now = time.strftime("%I:%M %p",time.localtime())
                        str_ = random.choice(time_response) +str(now)
			return [True, str_]
       
                elif (sentence.lower() in dateArr):
			now = time.strftime("%A, %B %Y",time.localtime())
                        str_ = random.choice(date_response) +str(now)
			return [True, str_]

		elif (("conversation" in split or "talking" in split or "chatting" in split) and ("going" in split or "long" in split or "length" in split or "duration" in split)):
			now = time.mktime(time.gmtime())
                        num = str(now - startSecs)
                        str_ = "We have been talking for %s second(s)!" %num
			return [True, str_]

                else: 
                    return [False]
        else:
             return [False]


