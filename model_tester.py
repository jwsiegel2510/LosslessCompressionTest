#!/usr/bin/python

# Tests a model by compressing the Hitch Hiker's Guide to the Galaxy,
# calculating the compression ratio and checking to be sure that the decompressed
# text is identical to the original.

from source_coder import compress
from source_coder import decompress
from one_frequency_model import OneFrequencyModel # change this line to test a different model.

model = OneFrequencyModel() # change this line to test a different model.

message = ''
with open('HitchHikersGuide.txt','r') as myfile:
	message = myfile.read()

compressed_message = compress(message, model)
print("The compression ratio (over ascii character encoding) is:", 2141320.0/(len(compressed_message)))
recovered_message = decompress(compressed_message, model)
if (recovered_message == message):
	print("Recovery: SUCCESS")
else:
	print("Recovery: FAILURE")
