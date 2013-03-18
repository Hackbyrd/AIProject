import sys
import shlex
import re
import string

#Already Built Dictionary
dic = {}
dic['proper noun']=['Sue','John','Fido','Don','Perlis'] 
dic['pronoun'] = ['he','she','i','you','we','they','this','that','there','what','who','it','them','me','everyone','everything','something']
dic['determiner'] = ['a','an','the']
dic['noun'] = ['people','children','cat','dog','pet','mat','idea','cats','dogs','pets','mats','ideas']
dic['verb'] = ['is', 'go','are','am','was','were','ate','sleep','like','has','have','do','does', 'mean','means']
dic['advanced noun'] = []
dic['advanced verb'] = []
dic['adverb'] = ['furiously','where']
dic['adjective'] = ['green','colorless','this','that','those']
dic['preposition'] = ['of','on','in','at','to','by','with','among','along','before','around']
dic['connective'] = ['not']
dic['unknown'] = []
question = ['what', 'who', 'where', 'when', 'how','can','may','did','were','was','is','are','does','do']


flag = 1

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
	#	print 'Grammatical Error, adverbs with no matching verbs'
	
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
	simple_nouns = open('simple_nouns.txt','ru')
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
def main():	
	global flag 
	while(flag):
		#Does anyone know if we're given a textfile input or are the TAs entering by hand?
		sentence = raw_input()
		#Splits sentences into a list of stromgs
		sentence = shlex.split(sentence)
		sentence = strip_punc(sentence)
		for x in range(0, len(sentence)-1):
			if sentence[x] not in dic['proper noun']:
				sentence[x] = sentence[x].lower()
		find_types(sentence)
		svo = get_SVO(sentence)
		phrased = phrasify(sentence)
		print phrased[0]
		print phrased[1]
		print svo[0]
		print svo[1]
main()
