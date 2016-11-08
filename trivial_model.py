#!/usr/bin/python

# Contains a trivial model of the english language. The model contains no information and thus
# assumes that each letter in the source is drawn uniformly at random from the liast of 
# possible characters.

from source_coder import character_list

class TrivialModel:
	def probabilities(self):
		probs = {}
		probability = .999999/(len(character_list)-1) # all characters except the EOF character have the same probability.
		for i in character_list[:-1]:
			probs[i] = probability
		probs[-1] = .0000001
		return probs

	def next_char(self,a):
		return
