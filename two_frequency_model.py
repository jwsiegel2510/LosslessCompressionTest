#!/usr/bin/python

# Contains a model consisting of a frequency distribution of each of bigrams.
# Assumes each character is drawn uniformly at random from the marginal distribution 
# given the previous character.

from source_coder import character_list
import re
from random import randint
from bs4 import BeautifulSoup
import requests
from math import log

class TwoFrequencyModel:
	def __init__(self):
		self.current_char = chr(127)
		try:
			f = open("TwoProbabilityData.txt","r")
			probabilities = list(map(float,f))
			self.probs = {}
			for i in character_list:
				self.probs[i] = {}
			for i in range(len(probabilities)):
				self.probs[character_list[i // len(character_list)]][character_list[i%len(character_list)]] = probabilities[i]
					
		except: # crawl wikipedia for statistics
			occurrence_number = {}
			for i in character_list:
				occurrence_number[i] = {}
			for i in character_list:
				for j in character_list:
					occurrence_number[i][j] = 1
			response = requests.get("https://en.wikipedia.org")
			soup = BeautifulSoup(response.text, "lxml")
			links = [link for link in soup.body.p.find_all('a') if link['href'][0] != '#'] # we dont want links which are references
			text = re.sub(r'\[\d*\]','',soup.body.p.getText()) # remove references from the text
			prev_char = chr(127)
			for c in text:
				if c in occurrence_number: # extraneous characters might occur
					occurrence_number[prev_char][c] += 1
					prev_char = c
			occurrence_number[prev_char][chr(127)] += 1
			for i in range(500):
				next_link = links[randint(0,len(links))]
				try:
					response = requests.get("https://en.wikipedia.org" + next_link['href'])
					soup = BeautifulSoup(response.text, "lxml")
					paragraphs = soup.body.find_all('p')
					for p in paragraphs:
						links += [link for link in p.find_all('a') if link['href'][0] != '#']
						text = re.sub(r'\[\d*\]','',p.getText()) # remove references from the text
						prev_char = chr(127)
						for c in text:
							if c in occurrence_number: # extraneous characters might occur
								occurrence_number[prev_char][c] += 1
								prev_char = c
						occurrence_number[prev_char][chr(127)] += 1
				except:
					links.remove(next_link)
			self.probs = {}
			for i in character_list:
				self.probs[i] = {}
			try:
				stats_file = open("TwoProbabilityData.txt","w")
			except:
				print("File for storing the language statistics couldn't be opened.")
				sys.exit(0)
			for c in character_list:
				total_characters = len(character_list)
				for d in character_list:
					total_characters += occurrence_number[c][d]
				for d in character_list:
					self.probs[c][d] = (float(occurrence_number[c][d])/total_characters)
					stats_file.write("{:.12f}".format(self.probs[c][d]))
					stats_file.write("\n")
				
	def probabilities(self):
		return self.probs[self.current_char]

	def next_char(self,a):
		self.current_char = a
		return
