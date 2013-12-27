# This is in Python 3. Run it in Python 3.

from urllib.request import Request, urlopen
from urllib.error import  URLError
import http.server
import re

# Interact with the user
infile = input('Name and path of the file to check: ')
print('\nThe output will show up in the console and will also be available in a file called urlreport.txt\n\n')
print('Here we go! \n\n')

# Tricking the server into treating us like a real web browser
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
theagent = { 'User-Agent' : user_agent }

# This should always succeed; it creates the output file and makes it writable
try:
	w = open('urlreport.txt','w')
except IOError as err:
	print("I/O error: {0}".format(err))

else:
	# Here's where we see if the user entered a good filename

	# ****** When everything else works, remind me to put this in a while() loop
	# ... because I like my users and want to give them a chance to get it right
	# ******

	try:
		f = open(infile,'r')
		
	except IOError as err:
	    print("I/O error: {0}".format(err))

	# If everything's in order with all the filenames, let's proceed
	else:
		# Going line-by-line through the file...
		for line in f:
			# ... use this sweet regex I found to grab all the URLs from the text
			theexpr = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
			# This thing gives you stupid tuples with information only in the first slot
			# I don't know why.
			for mgroups in theexpr.findall(line):
				# But we'll grab the first spot in the tuple, which is the URL
				someurl = mgroups[0]
				# Interact with the user and output file some more
				print('Checking ' + someurl, end=' -- ')
				w.write('Checked ' + someurl + ': ')
				# I was feeling a little prim when I added this output; why include http sometimes but not others?
				# Still, adding the [understood] http: is easy and prevents needless errors.
				if (not '://' in someurl):
					someurl = 'http://' + someurl
					print('Needs URI scheme name indicated (http://, ftp://, etc.). \nTrying ' + someurl + ' instead:', end=' ')
					w.write('Needs URI scheme name indicated (http://, ftp://, etc.). \nTried ' + someurl + ': ')
				
				# Send the request, with no data and that user agent lie
				req = Request(someurl, data=None, headers=theagent)

				# I have questions about this structure; maybe I shouldn't be "except"ing the errors.
				# Perhaps they should be printed just like the successes in the try: statement.
				try:
				    response = urlopen(req)
				    print(http.server.BaseHTTPRequestHandler.responses[response.code][0])
				    if response.geturl() != someurl:
				    	print('The URL redirected. Update ' + someurl + ' to ' + response.geturl())
				    	w.write('The URL redirected. Update ' + someurl + ' to ' + response.geturl() + '\n')

				# Making the appropriate responses, in the case of errors
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
				        # This should never happen. But if it does, it's something interesting!
				        print(someurl + "has something funky going on.")
				print(" ") # double-spacing
				w.write('\n') # single-spacing
# Cleaning up.				
w.close()
f.close() 