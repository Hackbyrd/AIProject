# Project 4
# TEAM 1
# Aroh, Kosi
# Block, Peter
# Chen, Jonathan
# Chen, Vincent
# Chiosi, Brian

import random
import sys
import shlex
import re
import string
import hardcode
import datetime
import time
import en
import thread
import threading

#Knowledge Base
dic = {}
dic['greetings'] = ['hey','hello', 'hi','howdy', 'greetings', 'hi there', 'hello there'] 
dic['exits'] = ['cya', 'bye', 'goodbye','sayonara','adios','later']
dic['proper noun']=['Sue','John','Fido', 'sue', 'john', 'fido', 'Don', 'don', 'Perlis', 'perlis'] 
dic['pronoun'] = ['he','she','i','you','we','what','they','this','that','there', 'what','who','it','them', 'me', 'everyone', 'everything', 'something']
dic['determiner'] = ['a','an','the']
dic['noun'] = ['people','children','cat','dog','pet','mat','idea','cats','dogs','pets','mats','ideas']
dic['verb'] = ['is', 'go','are','am','was','were','ate','sleep','do','like','can','may','will','did','does','has','have','mean','means']
dic['advanced noun'] = []
dic['advanced verb'] = ['is', 'go']
dic['adverb'] = ['furiously','where']
dic['adjective'] = ['green','colorless','this','that','those']
dic['preposition'] = ['of','on','in','at','of','to','by','with','among','along','before','around']
dic['connective'] = ['not','and','or']
dic['unknown'] = []
dic['question'] = ['what', 'whats','who', 'whos', 'where', "wheres", 'when', "whens", 'how', "hows", 'can','may','will', 'did', 'were', 'was', 'is', 'are', 'does']
linking_verb = ['am', 'is', 'are', 'was', 'were','become','seem']


special_questions = ['can','may','will', 'did', 'does']
# Conversation log
conversation = []

# time and date
start_date = ""
start_time_sec = ""

# Associations
assoc = {} # maps a subject to adjectives , save user's name in assoc['user__']
kb ={} # maps subject to list of hashes({verb,object})
noun_phrases = {}

# topic string - stores what the current conversation is about
topic = ""

# possible ways to start a yes no question
yes_no_question = ['can','may','will', 'did', 'were', 'was', 'is', 'are', 'does']

# possible ways to introduce yourself
introduce_name = ["Im","i am","I am","I go by","i go by","My name is","my name is", "is what they call me","I am called"]  

# possible ways to ask about user name
user_name_question = ["what is my name","whats my name", "my name", "do you know my name","tell me my name"]
tell_user_their_name = ["well its ", "you told me it was ", "", "your name is ", "its "]

# possible ways of saying yes
confirmations=["yup","yes","yea","ok","of course","definitely","mmhmm","(nod)","yeah","right","true","sure","no problem","indeed","affirmative","definetly","all right","okay","why not?","agreed","fair enough","certainly", "positive", "by all means","absolutely", "guaranteed", "clearly","very","totally","heck yes","duh"] 

yes = ["yup","yes","yea","of course","definitely","(nod)","yeah","indeed","affirmative","definetly", "absolutely","totally","heck yes","duh"]

ok_response = ["Ok","Alright","Got it","okey dokey", "i'll remember that"]
# possible ways of saying no
answer_is_no = ["no","nope","not in a million years","i don't believe so","not according to my knowledge"]
no = ["no","nope","not in a million years","i don't believe so","not according to my knowledge"]

# possible ways to respond to reduandant information
repeated_input_reponse=["do you enjoy repeating yourself?","what else is new?","heard you the first time","are you just going to repeat your self all day?","thank you captain repeats alot","again?...","is there a parrot in room?","ok... apprently I'm talking to a broken tape recorder"]

# sentences that ask about the topic
topic_sentence = ["what are we talking about", "what is the current topic","what is the main point","what is the topic of this conversation"]
topic_response = ["the current topic is", "well right now we are talking about", "we are currently discussing", "the main idea is on", "I guess it's", "we are talking about"]
no_topic_response = ["you haven't really said much", "nothing i guess", "the conversation just started"]

# possibble ways of saying you don't know the answer to something
dont_know_answer_responses = ["I have no idea", "I am completely clueless","You know what, I am really not sure", "No idea, ask your mother","I might be a machine, but I don't know EVERYTHING", "Hmmm, let me guess.... the answer is pudding?", "You never told me", "You haven't taught me that yet"]

i_know_answer_responses = [" according to what you told me", " I believe", " if I remember correctly"]

#Known question words
question = ['what', 'whats','who', 'where', 'when', 'how','can','may','will', 'did', 'were', 'was', 'is', 'are', 'does']

# response to give when we don't know how to answer
confused = ["you're kidding right", "what???", "Sorry I didn't catch that", "Oh no she didn't", "Ok, but how does that make you feel?"]

# responce when user is not saying anything
lonely = ["Are you there??", "Is anybody out there?", "Don't you want to talk to me...", "Lonely, I'm so lonely.", "Awkward..."]

#plural funtion from http://www.diveintopython.net/dynamic_functions/stage5.html
def buildRule((pattern, search, replace)):
   return lambda word: re.search(pattern, word) and re.sub(search, replace, word)

def plural(noun, language='en'):
   lines = file('rules.%s' % language).readlines()
   patterns = map(string.split, lines)
   rules = map(buildRule, patterns)
   for rule in rules:
      result = rule(noun)
      if result: return result

# Exit flag
exit_flag = 1

#Removes punctuation from the sentence
def strip_punc(array):
	for i in range(0,len(array)):
		for char in array[i]:
 		   if char in " ,.!?;:":
        	   	array[i] = array[i].replace(char,'')
	return array

def take_out_punc_from_string(raw_sentence):
       raw_sentence = raw_sentence.strip()
       raw_sentence = re.sub(r"[,\.!\?;:']*","",raw_sentence) 
       return raw_sentence

#Given a list of words with known types, return a list with the types in respective order 
def get_types(array):
	type_array=[]
	for words in array:
		for word_type in dic:
			if (words in dic[word_type]):
				type_array.append(word_type)
	return type_array
		   
# determines whether the given word is in the given list
# including plurals if specified
def index_(list_, x,n_v = False): 
   for a in list_:
     if a == x: return 1
     elif n_v and plural(a) == x: return 1
   return -1

#Goes through each word in an array and determines if the type exists or not,
#if a type doesn't exist then it asks for input
def preprocess(array):
	for words in array:
		exists=None
		for word_type in dic:
			#if (words in dic[word_type]): i changed it to account for plurals so we don't have to pluralize everything
                        n_v = False
                        if word_type in ['noun', 'verb']:
                           n_v = True
                        if index_(dic[word_type], words.lower(), n_v) == 1 or index_(dic[word_type], words, n_v) == 1:
				exists=1
		if (exists == None):
                        str_ = 'What type of word is ' + words +'?'
                        conversation.append(str_)
			print str_
                        print ""
			input_type = raw_input()
                        conversation.append(input_type)
			while (input_type not in dic.keys()):
                                str_ = 'I do not recognize that type'
                                conversation.append(str_)
				print(str_)
                                str_ = 'What type of word is ' + words +'?'
                                conversation.append(str_)	
				print str_
                                print ""
				input_type = raw_input()
                                conversation.append(input_type)		
			dic[input_type].append(words)

def is_question(str1):
   return str1[0].lower() in question

# need to implement
def asked_me_about_his_name(sentence):
  if (sentence in user_name_question):
     global topic
     topic = "names"
     if ("user__" in assoc):
        str_ = random.choice(tell_user_their_name) + assoc["user__"]
        print str_
        conversation.append(str_)
     else:
        print "you never told me"
        conversation.append("you never told me")
     return True
  return False

def get_confused_response():
	# add random generator
	str_ = random.choice(confused)
	conversation.append(str_)
	return str_

def get_lonely_response():
	# add random generator
	str_ = random.choice(lonely)
	conversation.append(str_)
	return str_

def get_name_from_introduction(sentence):
   for i in range(0,len(introduce_name)):
       str_arr = sentence.split(introduce_name[i])
       if len(str_arr) > 1:
          for str_ in str_arr:
             if str_ != "":
                return str_
   return ""

def get_response_for_repeated_info():
  return random.choice(repeated_input_reponse)

def told_me_his_name(sentence):
   name = get_name_from_introduction(sentence).strip()
   if name != "":
      global topic
      topic = "your name"
      if ("user__" in assoc) and name == assoc["user__"]:
        str_ = get_response_for_repeated_info()
        conversation.append(str_)  
        print str_
        return True
      else:
        str_ = "So people call you " + name + "?"
        conversation.append(str_)
        print str_
        print ""
        raw_sentence = raw_input()
        conversation.append(raw_sentence)
        sentence = take_out_punc_from_string(raw_sentence)
        if sentence.lower() in confirmations:
           if 'user__' in assoc:
              str_ = "should i forget the current name you told  me " + assoc["user__"] + "?"
              conversation.append(str_)
              print str_
              print ""
              raw_sentence = raw_input()
              conversation.append(raw_sentence)
              sentence = take_out_punc_from_string(raw_sentence)
              if sentence.lower() in confirmations:
                 str_ = "then I will call you " + name
                 conversation.append(str_)
                 assoc['user__'] = name
                 print str_
              else: 
                 str_ = "Ok never mind then "
                 conversation.append(str_)
                 print str_
           else:
              str_ = "then I will call you " + name
              assoc['user__'] = name
              conversation.append(str_)
              print str_
        else:
           str_ = "Ok never mind then"
           conversation.append(str_)
           print str_
        return True
   else:
      return False

def get_greeting():
   name = ""
   if 'user__' in assoc:
      if random.choice([0,1]) == 1:
         name = assoc['user__']
   return random.choice(dic['greetings']) +" "+name

def get_goodbye():
   name = ""
   if 'user__' in assoc:
         name = assoc['user__']
   return random.choice(dic['exits']) +" "+name

# determines whether user wanted to see conversation history
def show_conversation_log(raw_sentence):
   return (raw_sentence.lower() in ["conversation history","conversation log","show conversation log","what is the conversation log","show me the conversation log"])

# prints conversation history
def print_conversation():
   print "Ok, here is what we talked about..."
   print "["
   for i in range(0,len(conversation)):
      print "  " + conversation[i]
   print "]"
   global topic
   topic = "conversation history"
   conversation.append("Ok, here is what we talked about...")

# our first attempt at responding
# checks if input matches any hard coded expectations
def respond1(sentence):
   global topic
   global start_date
   global start_time_sec
   if sentence == "":
		print "Are you trying to break me?!"
		return True
   elif sentence in dic['greetings']:
      greeting_response = get_greeting()
      conversation.append(greeting_response)
      topic = "names"
      print greeting_response
      return True
   elif sentence in dic['exits']:
      good_bye = get_goodbye()
      conversation.append(good_bye)
      print good_bye
      return True
   elif sentence in topic_sentence:
      if topic == "":
        str_ = random.choice(no_topic_response)
      else:
        str_ =random.choice(topic_response) + " "+ topic
      print str_
      conversation.append(str_)
      return True
   elif show_conversation_log(sentence):
      print_conversation()
      return True
   elif told_me_his_name(sentence):
      return True
   elif asked_me_about_his_name(sentence):
      return True
   else:
      boolean = is_question(shlex.split(sentence))
      arr1 = hardcode.hardCode(sentence,start_time_sec, start_date, boolean)
      if arr1[0]:
         print arr1[1]
         conversation.append(arr1[1])
         return True
      else: 
       # arr = proj3mod.runProj3(sentence)
        #if arr[0]:
         #  print arr[1]
          # conversation.append(arr[1])
           #return True
        return False

def verb_in_hash(verb, hash_):
   for i in hash_.keys():
      if en.verb.infinitive(hash_[i]) == en.verb.infinitive(verb):
         return True
   return False

def is_noun_dic(word):
   for i in dic["noun"]:
      if word.lower() == i.lower() or word.lower() == plural(i.lower()):
         return True
   for i in dic["proper noun"]:
      if word.lower() == i.lower():
         return True
   for i in dic["pronoun"]:
      if word.lower() == i.lower():
         return True
   for i in dic["advanced noun"]:
      if word.lower() == i.lower() or word.lower() == plural(i.lower()):
         return True
   return False


def is_verb_dic(word):
   for i in dic['verb']:
      if en.verb.infinitive(i) == en.verb.infinitive(word):
         return True
   return False
def is_adj_dic(word):
    for i in dic['adjective']:
      if i == word:
        return True
    return False

# second attempt at responding using word phrases and associations
def respond2(sent_array,svo,sentence,is_a_question):
    global topic
    is_sentence_parsed = svo != ['','',''] or svo[0] != ''
    starts_with_a_question_word = is_question(sent_array)
    if len(sent_array) == 2:
         if is_a_question or starts_with_a_question_word:
            subject = sent_array[1]
            topic = subject
            if subject not in kb:
              response = random.choice(dont_know_answer_responses)
            else:
              verb = en.verb.infinitive(sent_array[0])
              if verb in kb[subject]:
                 response = random.choice(yes)
              else:
                 response = random.choice(no)
         else:
             if is_noun_dic(sent_array[0]) and is_verb_dic(sent_array[1]):
                subject = sent_array[0]
                topic = subject
                verb = en.verb.infinitive(sent_array[1])
                if subject not in kb:
                   kb[subject] = {}
                if verb not in kb[subject]:
                   kb[subject][verb] = []
                   response = random.choice(ok_response)
                else:
                   response = random.choice(repeated_input_reponse)
             else:
                response= get_confused_response()

    elif len(sent_array) == 3: 
         if is_a_question or starts_with_a_question_word:
            if sent_array[0] in special_questions:
              verb1 = en.verb.infinitive(sent_array[0])
              verb2 = en.verb.infinitive(sent_array[2])
              subject = sent_array[1]
              topic = subject
              if subject not in kb:
                response = random.choice(dont_know_answer_responses)
              elif verb1 in kb[subject]:
                 if len(kb[subject][verb1]) > 0 and verb2 in kb[subject][verb1][0]:
                   response = random.choice(yes)
              elif verb2 in kb[subject]:
                response = random.choice(yes)
              else:
                response = random.choice(no)
            else:
              if sent_array[0] in yes_no_question:
                verb = en.verb.infinitive(sent_array[0])
                subject = sent_array[1]
                topic = subject
                objct = sent_array[2]
                if subject not in kb:
                  response = random.choice(dont_know_answer_responses)
                elif verb in kb[subject]:
                  if objct in kb[subject][verb]:
                    response = random.choice(yes)
                  else:
                    response = random.choice(yes)
                else:
                  response = random.choice(dont_know_answer_responses)
              else:
                verb = en.verb.infinitive(sent_array[1])
                subject = sent_array[2]
                topic = subject
                if subject not in kb:
                  response = random.choice(dont_know_answer_responses)
                elif verb in kb[subject]:
                  verb_array = kb[subject][verb][0]
                  response = ""
                  for i in verb_array:
                    response += i + ", " 
                  response +="is all i know."
                else:
                  response = random.choice(dont_know_answer_responses)
         else:
            if is_noun_dic(sent_array[0]) and is_verb_dic(sent_array[1]):
                subject = sent_array[0]
                topic = subject
                verb = en.verb.infinitive(sent_array[1])
                objct = sent_array[2]
                if objct in dic["adverb"]:
                  if subject not in kb:
                     kb[subject] = {}
                     kb[subject][verb] =[[],[objct]]
                     response = random.choice(ok_response)
                  elif verb not in kb[subject]:
                     kb[subject][verb] = [[],[objct]]
                     response = random.choice(ok_response)
                  elif verb in kb[subject][verb][0]:
                     kb[subject][verb][1].append(objct)
                     response = random.choice(ok_response)
                  else:
                     response = random.choice(repeated_input_reponse)
                else:
                  if subject not in kb:
                     kb[subject] = {}
                     kb[subject][verb] =[[objct],[]]
                     response = random.choice(ok_response)
                  elif verb not in kb[subject]:
                     kb[subject][verb] = [[objct],[]]
                     response = random.choice(ok_response)
                  elif objct not in kb[subject][verb][0]:
                     kb[subject][verb][0].append(objct)
                     response = random.choice(ok_response)
                  else:
                     response = random.choice(repeated_input_reponse)
            elif is_noun_dic(sent_array[1]) and is_verb_dic(sent_array[2]):
                subject = sent_array[1]
                topic = subject
                verb = en.verb.infinitive(sent_array[2])
                objct = sent_array[0]
                if objct in dic["adjective"]:
                  if subject not in kb:
                     kb[subject] = {}
                     kb[subject][verb] =[[],[]]
                     assoc[subject] = [objct] 
                     response = random.choice(ok_response)
                  elif verb not in kb[subject]:
                     kb[subject][verb] = [[],[]]
                     if subject in assoc and objct not in assoc[subject]:
                       assoc[subject].append(objct)
                     response = random.choice(ok_response)
                  elif verb in kb[subject][verb]:
                     if subject in assoc and objct not in assoc[subject]:
                       assoc[subject].append(objct)
                     response = random.choice(ok_response)
                  else:
                     response = random.choice(repeated_input_reponse)
                elif objct in dic["determiner"]:
                  if subject not in kb:
                     kb[subject] = {}
                     kb[subject][verb] =[]
                     response = random.choice(ok_response)
                  elif verb not in kb[subject]:
                     kb[subject][verb] = []
                     response = random.choice(ok_response)
                  else:
                     response = random.choice(repeated_input_reponse)
                else:
                  response = get_confused_response()

            else:
                response= get_confused_response()
    else:
      if is_a_question or starts_with_a_question_word:

        if (is_sentence_parsed):

          subj = svo[1][0]
          topic = subj
          vrb = en.verb.infinitive(svo[1][1])
          oj = svo[1][2]

          if (not subj == ''):
            if(not vrb == ''):
              if(subj in kb):
                if(vrb in kb[subj]):
                  ojs = kb[subj][vrb]
                  senStr = ""
                  eflag = False 
                  for s in ojs[0]:
                    if oj == s:
                      eflag = True
                    senStr = senStr + "%s, " %s
                    if (sent_array[0] in yes_no_question):
                      if(eflag == True):
                        response = random.choice(yes)
                      else:
                        if (s in kb):
                          if (en.verb.infinitive('is') in kb[s]):
                            if (oj in kb[s][en.verb.infinitive('is')][0]):
                              eflag = True
                              response = random.choice(yes)
                    else:
                      response = senStr + "that's what you told me..."
                      eflag = True
                  if(eflag == False):
                      response = random.choice(no)
                else:
                  if (sent_array[0] in yes_no_question):
                    response = random.choice(no)
                  else:
                    response = random.choice(dont_know_answer_responses)
              else:
                response = random.choice(dont_know_answer_responses)
            else:
              response = random.choice(dont_know_answer_responses)
          else:
            response = random.choice(dont_know_answer_responses)
        else:
          response = get_confused_response()

      else:

        if (is_sentence_parsed):

          subj = svo[1][0]
          topic = subj
          vrb = en.verb.infinitive(svo[1][1])
          oj = svo[1][2]
          ajSub = []
          ajObj = []

          for word in svo[0][0]:
            if word in dic['adjective']:
              ajSub.append(word)

          for word in svo[0][2]:
            if word in dic['adjective']:
              ajSub.append(word)

          if (not subj == ''):
            if(not vrb == ''):
              if(not oj == ''):
                if(subj not in kb):
                  kb[subj] = {}
                  kb[subj][vrb] = [[oj],[]]
                  if(subj not in assoc):
                    assoc[subj] = []
                  for w in ajSub: 
                    if (w not in assoc[subj]): 
                      assoc[subj].append(w)
                  for o in ajObj:
                    if (o not in assoc[vrb]):  
                      assoc[vrb].append(o)
                  response = random.choice(ok_response)
                elif(vrb not in kb[subj]):
                  kb[subj][vrb] = [[oj],[]]
                  for w in ajSub: 
                    if (w not in assoc[subj]):
                      assoc[subj].append(w)
                  for o in ajObj:
                    if (o not in assoc[vrb]): 
                      assoc[vrb].append(o)
                  response = random.choice(ok_response)
                elif(oj not in kb[subj][vrb]):
                  kb[subj][vrb][0].append(oj)
                  for w in ajSub: 
                    if (w not in assoc[subj]): 
                      assoc[subj].append(w)
                  for o in ajObj:
                    if (o not in assoc[vrb]):  
                      assoc[vrb].append(o)
                  response = random.choice(ok_response)
                else:
                  response = random.choice(repeated_input_reponse)
              else:
                response = get_confused_response()
            else:
                response = get_confused_response()
          else:
                response = get_confused_response()
        else:
          response = get_confused_response()

    print response
    conversation.append(response)

#Given a sentence and an index, returns the noun phrase, and the index of the next word
def make_NP(sentence, index):     
  noun_phrase = [sentence[index]]
  index2 = index+1
  while index2 < len(sentence): 
    if sentence[index2] in dic['adjective'] or sentence[index2] in dic['adverb']:
      noun_phrase.append(sentence[index2])
    elif sentence[index2] in dic['noun'] or sentence[index2] in dic['pronoun'] or sentence[index2] in dic['proper noun']:
      noun_phrase.append(sentence[index2])
      break
    elif sentence[index2] in dic['advanced noun']:
      dic['noun'].append(sentence[index2])
      noun_phrase.append(sentence[index2])
      break
    else:
      index2 = index2 - 1
      break
    index2 = index2 + 1
  is_noun = noun_phrase[len(noun_phrase) - 1]
  #if (is_noun not in dic['noun'] and is_noun not in dic['pronoun'] and is_noun not in dic['proper noun'] and is_noun not in dic['advanced noun']):       
      #Throw exception here?
      #print 'Grammatical Error, adjectives or determiners with no matching nouns'  
  #print index2
  return [noun_phrase, index2]

#Given a sentence and an index, return a prepositional phrase and the index of the next word
def make_PP(sentence, index):
  statement = make_NP(sentence, index)
  prep_phrase = statement[0]
  index = statement[1]
  return [prep_phrase, index]

#Given a sentence and an index, return a verb phrase and the index of the next word
def make_VP(sentence, index):
  verb_phrase = [sentence[index]]
  index2 = index+1
  while index2 < len(sentence):
    if sentence[index2] in dic['adverb'] and sentence[index2] not in dic['determiner']:
      verb_phrase.append(sentence[index2])
    elif sentence[index2] in dic['verb']:
      verb_phrase.append(sentence[index2])
      break
    elif  sentence[index2] in dic['advanced verb']:
      dic['verb'].append(sentence[index2])
      verb_phrase.append(sentence[index2])
      break
    else:
      index2 = index2 - 1
      break
    index2 = index2 + 1
  #is_verb = verb_phrase[len(verb_phrase) - 1]
  #if (is_verb not in dic['verb']):
  # print 'Grammatical Error, adverbs with no matching verbs'
  
  return [verb_phrase, index2]

#Given a sentence, returns a list with two lists. The first list returns all the words grouped up into phrases
#The second list returns the type of each phrase, as in QW,PP,NP,VP, and CONNECT  
def phrasify(sentence):
  index = 0
  phrase_sentence = []
  phrase_types = []
  while index < len(sentence):
    if sentence[index] in question and index == 0:
      phrase_sentence.append([sentence[index]])
      if sentence[index] in dic['verb']:
        phrase_types.append('QW-V')
      elif sentence[index] in dic['pronoun']:
        phrase_types.append('QW-PN')
      else:
        phrase_types.append('QW')
    elif sentence[index] in dic['preposition']:
      statement = make_PP(sentence, index)
      prep_phrase = statement[0]
      
      phrase_sentence.append(prep_phrase)
      phrase_types.append('PP')
      index = statement[1]
    elif sentence[index] in dic['connective']:
      phrase_sentence.append([sentence[index]])
      phrase_types.append('CONNECT')    
    elif sentence[index] in dic['determiner']:
      statement = make_NP(sentence, index)
      noun_phrase = statement[0]
      index = statement[1]
      phrase_sentence.append(noun_phrase)
      phrase_types.append('NP')
    elif sentence[index] in dic['verb']:
      if index > 0 and phrase_types[len(phrase_types) - 1] == 'VP' and 'ing' not in sentence[index] and (sentence[index] in dic['noun'] or sentence[index] in dic['adjective']):
        phrase_sentence.append([sentence[index]])
        phrase_types.append('NP')
      else:
        phrase_sentence.append([sentence[index]])
        phrase_types.append('VP')
    elif sentence[index] in dic['noun'] or sentence[index] in dic['proper noun'] or sentence[index] in dic['pronoun']:
      phrase_sentence.append([sentence[index]])
      phrase_types.append('NP') 
    elif sentence[index] in dic['adjective']:
      statement = make_NP(sentence, index)
      noun_phrase = statement[0]
      index = statement[1]
      phrase_sentence.append(noun_phrase)
      phrase_types.append('NP') 
    elif sentence[index] in dic['adverb']:
      statement = make_VP(sentence, index)
      verb_phrase = statement[0]
      index = statement[1]
      if verb_phrase[len(verb_phrase)-1] in dic['noun'] or verb_phrase[len(verb_phrase)-1] in dic['adjective'] and verb_phrase[len(verb_phrase)-1] not in dic['verb']:
        phrase_sentence.append(verb_phrase)
        phrase_types.append('NP')
      elif len(phrase_types) > 0 and phrase_types[len(phrase_types)-1] == 'VP':
        phrase_sentence[len(phrase_sentence)-1].extend(verb_phrase)
      else:
        phrase_sentence.append(verb_phrase)
        phrase_types.append('VP')
    elif sentence[index] in dic['advanced noun']:
      dic['noun'].append(sentence[index])
      phrase_sentence.append([sentence[index]])
      phrase_types.append('NP') 
    elif sentence[index] in dic['advanced verb']:
      dic['verb'].append(sentence[index])
      phrase_sentence.append([sentence[index]])
      phrase_types.append('VP')
    else:
      dic['unknown'].append(sentence[index])
      phrase_sentence.append([sentence[index]])
      phrase_types.append('UNKNOWN')
    index = index + 1
  
  #print phrase_sentence
  #print phrase_types
  return [phrase_sentence,phrase_types]
#Checks to see if the word is already a noun or in the simple_nouns dictionary  
def is_noun(word):
  if word in dic['noun']:
    return 1
  simple_nouns = open('simple_nouns.txt','rU')
  i = simple_nouns.readline()[:-1]
  while i:
    if str(i) == word:
      if word not in dic['noun']:
        dic['noun'].append(word)
      return 1
    i = simple_nouns.readline()[:-1]
  return None

#Checks to see if the word is already a verb or in the simple_verbs dictionary
def is_verb(word):
  if word in dic['verb']:
    return 1
  simple_verbs = open('simple_verbs.txt','rU')
  i = simple_verbs.readline()[:-1]
  while i:
    if str(i) == word:
      if word not in dic['verb']:
        dic['verb'].append(word)
      return 1
    i = simple_verbs.readline()[:-1]
  return None 
  
#Given a sentence, tries to find the definition of every single word using a comprehensive dictionaries. Also does a greedy attempt to add verbs that end in 's'
# and verbs that end in -ing to the verb list. 
def find_types(sentence):
  for word in sentence:
    nouns = open('91K_nouns.txt','rU')
    verbs = open('31K_verbs.txt','rU')
    adverbs = open('6K_adverbs.txt','rU')
    adjective = open('28K_adjectives.txt','rU')
  
    is_noun(word) 
    is_verb(word)
    
    i = nouns.readline()[:-1]
    while i:
      if str(i) == word:
        if is_noun(word[:-1]) and word[len(word) - 1] == 's':
          dic['noun'].append(word)  
        elif 'ing' in word and word not in dic['verb']:
          dic['verb'].append(word)
        elif word not in dic['advanced noun']:
          dic['advanced noun'].append(word)
      i = nouns.readline()[:-1]
    i = verbs.readline()[:-1]
    while i:
      if i == word:
        if is_verb(word[:-1]) and word[len(word) - 1] == 's':
          dic['verb'].append(word)
        elif word not in dic['advanced verb']:
          dic['advanced verb'].append(word) 
      i = verbs.readline()[:-1] 
    i = adverbs.readline()[:-1]
    while i:
      if i == word:
        if word not in dic['adverb']:
          dic['adverb'].append(word)
      i = adverbs.readline()[:-1]
    i = adjective.readline()[:-1]
    while i:
      if i == word:
        if word not in dic['adjective']:
          dic['adjective'].append(word)
      i = adjective.readline()[:-1] 
  #print dic

#Strips punctuation
def strip_punc(array):
  for i in range(0,len(array)):
    for char in array[i]:
       if char in " ,.!?;:":
              array[i] = array[i].replace(char,'')
  return array

#Just checks to make sure if there is a VP and a NP 
def grammar(phrase_types):
  if len(phrase_types) == 0:
    return None
  elif ('VP' not in phrase_types and phrase_types[0] is not 'QW-V') or 'NP' not in phrase_types:
    return None
  else:
    return 1

#Returns the first noun it sees in a noun phrase    
def find_subject(nodes,phrase_types):
  if len(nodes) == 0:
    return None
  for x in range(0, len(phrase_types)):
    if phrase_types[x] == 'NP':
      if nodes[x][len(nodes[x])-1] in dic['noun'] or nodes[x][len(nodes[x])-1] in dic['pronoun'] or nodes[x][len(nodes[x])-1] in dic['proper noun']:
        return [nodes[x],nodes[x][len(nodes[x])-1]]
        break

def find_verb_phrase (nodes, phrase_types, index):
  for x in range(index, len(nodes)):
    if phrase_types[x] == 'VP':
      return x
  return None
#Returns the first noun it sees in a verb phrase, special case for linking verb + verb ending in -ing     
def find_verb(nodes, phrase_types):
  if len(nodes) == 0:
    return None
  for x in range(0, len(phrase_types)):
    if phrase_types[x] == 'VP' or (phrase_types[x] == 'QW-V' and x == 0):
      for y in range(0, len(nodes[x])):
        second_verb = find_verb_phrase(nodes, phrase_types, x+1)
        if second_verb:
          for y in range(0, len(nodes[second_verb])):
            if nodes[second_verb][y] in dic['verb']:
              return [nodes[x] + nodes[second_verb],nodes[second_verb][y]]
        if nodes[x][y] in dic['verb'] or nodes[x][y] in dic['advanced verb']:
          return [nodes[x],nodes[x][y]]
      break
#Returns the last noun it sees not in a PP. If no NP, looks in PP.
def find_object(nodes, phrase_types):
  if len(nodes) == 0:
    return None
  x = len(phrase_types) - 1
  while x > 0:
    if phrase_types[x] == 'NP':
      if nodes[x][len(nodes[x])-1] in dic['noun'] or nodes[x][len(nodes[x])-1] in dic['pronoun'] or nodes[x][len(nodes[x])-1] in dic['proper noun']:
        return [nodes[x],nodes[x][len(nodes[x])-1]]
    elif phrase_types[x] == 'VP':
      break
    x = x - 1
  x = len(phrase_types) - 1
  while x > 0:
    if phrase_types[x] == 'PP':
      if nodes[x][len(nodes[x])-1] in dic['noun'] or nodes[x][len(nodes[x])-1] in dic['pronoun'] or nodes[x][len(nodes[x])-1] in dic['proper noun']:
        return [nodes[x],nodes[x][len(nodes[x])-1]]
    elif phrase_types[x] == 'VP':
      break
    x = x - 1
  x = len(phrase_types) - 1
  while x > 0:
    if nodes[x][len(nodes[x])-1] in dic['noun'] or nodes[x][len(nodes[x])-1] in dic['pronoun'] or nodes[x][len(nodes[x])-1] in dic['proper noun'] or nodes[x][len(nodes[x])-1] in dic['adjective']:
        return [nodes[x],nodes[x][len(nodes[x])-1]]
    x = x - 1 
    
#Takes a string as an input, and returns the subject, object, and verve
def get_SVO(sentence):
  try:
    #find_types(sentence)
    phrased = phrasify(sentence)
    #if grammar(phrased[1]):
    subjects = find_subject(phrased[0], phrased[1])
    verbs = find_verb(phrased[0], phrased[1])
    objects = find_object(phrased[0], phrased[1])
    answer_whole = []
    answer_simple = []
    if subjects:
      answer_whole = [subjects[0]]
      answer_simple = [subjects[1]]
    else:
      answer_whole = ['']
      answer_simple = ['']
    if verbs:
      answer_whole = answer_whole + [verbs[0]]
      answer_simple.append(verbs[1])
    else:
      answer_whole = answer_whole + ['']
      answer_simple.append('')
    if objects and not objects[1] == subjects[1] and not objects[1] == verbs[1]:
      answer_whole = answer_whole + [objects[0]]
      answer_simple.append(objects[1])
    else:
      answer_whole = answer_whole + ['']
      answer_simple.append('')

    answer = [answer_whole, answer_simple]
    return answer
  except TypeError:
    return ['','','']

#Event to handle threading
e = threading.Event() 

topics = ["sky diving", "cooking", "soccer", "water polo", "ornithology", "17th century map making"]

def bring_up_topic():
  if ((random.choice([0,1]) == 1) and len(kb) != 0):
    response = "Tell me more about " + random.choice(kb.keys())
    conversation.append(response)
    print response
  else:
    response = "Why don't you tell me about " + random.choice(topics) + "?"
    conversation.append(response)
    print response

def do_something():
  while (1):	#as long as 60s haven't elapsed
    #and the flag is not set
    count = 0
    while(count < 60):
      #do nothing for 20 seconds
      time.sleep(1)

      if(count == 20 or count == 40):
        bring_up_topic()

      if(e.isSet()):
        count = 0
      else:
        count += 1
      #if nothing is typed within 60 seconds, print lonely response
    if (not e.isSet()):
      response = get_lonely_response()
      conversation.append(response)
      print response


# Main function					
def main():
	global exit_flag
        global start_date
        global start_time_sec
        start_date = datetime.datetime.now()
        start_time_sec = time.mktime(time.gmtime())
	thread.start_new_thread(do_something, tuple())
	while(exit_flag):
		raw_sentence = raw_input()
		e.set()
                conversation.append(raw_sentence)
                is_a_question = False
                if len(raw_sentence) > 2:
                  is_a_question = raw_sentence[len(raw_sentence)-1] == "?"
                #Strips each word of its punctuation
                sentence = take_out_punc_from_string(raw_sentence)
		#Splits sentences into a list of stromgs
		sent_array = shlex.split(sentence)
                if not respond1(sentence.lower()):
		   #Checks to make sure that every word has a type
                   # and returns sentence types in list form
		   
                   print "(processing...)"
                   conversation.append("(processing...)")
                   for x in range(0, len(sent_array)-1):
                     if sent_array[x] not in dic['proper noun']:
                        sent_array[x] = sent_array[x].lower()
                   find_types(sent_array)
		   svo = get_SVO(sent_array)
                   #print svo
                   preprocess(sent_array)
                   # if no "hard coded" matches then try fail safe response
                   respond2(sent_array,svo,sentence,is_a_question)
                if sentence in dic['exits']:
					thread.exit()
					exit_flag = None
		print ""
		time.sleep(1)
		e.clear()

main()
