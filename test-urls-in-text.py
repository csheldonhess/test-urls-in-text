# This is in Python 3. Run it in Python 3.

from urllib.request import Request, urlopen
from urllib.error import  URLError
import re

infile = input('Name of the file to check (if it\'s in a different directory, include that information too): ')
print('The output will show up in the console and will also be available in a file called urlreport.txt')

try:
	w = open('urlreport.txt','w')
	
except IOError as err:
	print("I/O error: {0}".format(err))

else:
	try:
		f = open(infile,'r')
		
	except IOError as err:
	    print("I/O error: {0}".format(err))

	else:
		for line in f:
			theexpr = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
			for mgroups in theexpr.findall(line):
				someurl = mgroups[0]
				print(someurl, end=' ')
				w.write(someurl + ' ')
				if (not '://' in someurl):
					someurl = 'http://' + someurl
					print(' -- needs URI scheme name indicated (http://, ftp://, etc.). Using ' + someurl)
					w.write(' -- needs URI scheme name indicated (http://, ftp://, etc.). Using ' + someurl)
				req = Request(someurl)

				try:
				    response = urlopen(req)

				# making the appropriate responses, in the case of errors
				except URLError as e:
				    if hasattr(e, 'reason'):
				        print(someurl, end=" -- ")
				        print (e, end=" ")
				        w.write(someurl + ' ')
				        w.write(e + ' ')
				    elif hasattr(e, 'code'):
				        print(someurl, end=" -- ")
				        print (e, end=" ")
				        w.write(someurl + ' ')
				        w.write(e + ' ')
				    else:
				        #say nothing
				        print(someurl + "has something funky going on.")
				print(" ")
				w.write('\n')
w.close()
f.close() 