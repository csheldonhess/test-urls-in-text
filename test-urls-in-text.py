# This is in Python 3. Run it in Python 3.

from urllib.request import Request, urlopen
from urllib.error import  URLError
import re

print("Listing URLs:")

f = open('elearn.txt','r')
for line in f:
	theexpr = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
	for mgroups in theexpr.findall(line):
		someurl = mgroups[0]
		print(someurl, end=" ")
		if (not '://' in someurl):
			someurl = 'http://' + someurl
			print(" -- needs URI scheme name indicated (http://, ftp://, etc.). Using " + someurl)
		req = Request(someurl)

		try:
		    response = urlopen(req)

		# making the appropriate responses, in the case of errors
		except URLError as e:
		    if hasattr(e, 'reason'):
		        print(someurl, end=" -- ")
		        print (e, end=" ")
		    elif hasattr(e, 'code'):
		        print(someurl, end=" -- ")
		        print (e, end=" ")
		    else:
		        #say nothing
		        print(someurl + "is weird.")
		print(" ")


f.close() 