#!/usr/bin/python

# Contains a model consisting of a frequency distribution of each of the different characters.
# Assumes each character is drawn uniformly at random from this distribution.

from source_coder import character_list
import re
from random import randint
from bs4 import BeautifulSoup
import requests
from math import log

class OneFrequencyModel:
	def __init__(self):
		try:
			f = open("OneProbabilityData.txt","r")
			probabilities = list(map(float,f))
			self.probs = {}
			for i in range(len(probabilities)):
				self.probs[character_list[i]] = probabilities[i]
		except: # crawl wikipedia for statistics
			occurrence_number = {}
			for i in character_list:
				occurrence_number[i] = 5
			response = requests.get("https://en.wikipedia.org")
			soup = BeautifulSoup(response.text, "lxml")
			links = [link for link in soup.body.p.find_all('a') if link['href'][0] != '#'] # we dont want links which are references
			text = re.sub(r'\[\d*\]','',soup.body.p.getText()) # remove references from the text
			for c in text:
				if c in occurrence_number: # extraneous characters might occur
					occurrence_number[c] += 1
			for i in range(500):
				next_link = links[randint(0,len(links))]
				try:
					response = requests.get("https://en.wikipedia.org" + next_link['href'])
					soup = BeautifulSoup(response.text, "lxml")
					paragraphs = soup.body.find_all('p')
					for p in paragraphs:
						links += [link for link in p.find_all('a') if link['href'][0] != '#']
						text = re.sub(r'\[\d*\]','',p.getText()) # remove references from the text
						for c in text:
							if c in occurrence_number: # extraneous characters might occur
								occurrence_number[c] += 1
				except:
					links.remove(next_link)
			self.probs = {}
			total_characters = 0
			try:
				stats_file = open("OneProbabilityData.txt","w")
			except:
				print("File for storing the language statistics couldn't be opened.")
				sys.exit(0)
			for c in character_list[:-1]:
				total_characters += occurrence_number[c]
			for c in character_list[:-1]:
				self.probs[c] = (float(occurrence_number[c])/total_characters)*(.999999) # need to leave room for EOF character.
				stats_file.write("{:.12f}".format(self.probs[c]))
				stats_file.write("\n")
			c = character_list[-1]
			self.probs[c] = .0000001
			stats_file.write("{:.12f}".format(self.probs[c]))
			stats_file.write("\n")
				
	def probabilities(self):
		return self.probs

	def next_char(self,a):
		return

	def entropy(self):
		entropy = 0
		for c in character_list:
			if self.probs[c] > 0:
				entropy -= self.probs[c]*log(self.probs[c],2)
		return entropy
