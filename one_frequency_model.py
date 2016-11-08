#!/usr/bin/python

# Contains a model consisting of a frequency distribution of each of the different characters.
# Assumes each character is drawn uniformly at random from this distribution.

from source_coder import character_list
import re
from random import randint
from bs4 import BeautifulSoup
import requests

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
			for i in range(100):
				next_link = links[randint(0,len(links))]
				response = requests.get("https://en.wikipedia.org" + next_link['href'])
				soup = BeautifulSoup(response.text, "lxml")
				paragraphs = soup.body.find_all('p')
				for p in paragraphs:
					links += [link for link in p.find_all('a') if link['href'][0] != '#']
					text = re.sub(r'\[\d*\]','',p.getText()) # remove references from the text
					for c in text:
						if c in occurrence_number: # extraneous characters might occur
							occurrence_number[c] += 1
			self.probs = {}
			total_characters = 0
			try:
				stats_file = open("OneProbabilityData.txt","w")
			except:
				print("File for storing the language statistics couldn't be opened.")
				sys.exit(0)
			for c in character_list:
				total_characters += occurrence_number[c]
			for c in character_list:
				self.probs[c] = float(occurrence_number[c])/total_characters
				stats_file.write("{:.12f}".format(self.probs[c]))
				stats_file.write("\n")
				
	def probabilities(self):
		return self.probs

	def next_char(self,a):
		return
