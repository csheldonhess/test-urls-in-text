# This is in Python 3. Run it in Python 3.

from urllib.request import Request, urlopen
from urllib.error import  URLError
import http.server
import re

# ... use this sweet regex I found to grab all the URLs from the text
theexpr = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

# Interact with the user
infile = input('\nFile or URL to check: ')
print('\nThe output will show up in the console and will also be available in a file called urlreport.txt\n\n')
print('Here we go! \n\n')

# Tricking the server into treating us like a real web browser
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
theagent = { 'User-Agent' : user_agent }

# This should always succeed; it creates the output file and makes it writable
try:
	w = open('urlreport.txt','w')
except IOError as err:
	print("Bad output file. I/O error: {0}".format(err))

else:
	# Here's where we see if the output file opened acceptably

	
	if theexpr.match(infile) != None:
		# it is a URL
		someurls = [infile]
	else:
		try:
			f = open(infile,'r')
			someurls = []
			# Going line-by-line through the file...
			for line in f:
				# Below, findall() gives you lists with information only in the first slot
				# Unless there are two or more URLs per line...
				# Possible future upgrade: deal with the improbable circumstance of multiple URLs on a line
				for mgroups in theexpr.findall(line):
					# We'll grab the first spot in the list, which is a URL
					someurls.append(mgroups[0])
			f.close() 
		
		except IOError as err:
		    print("Bad file specified by user. Exiting. I/O error: {0}".format(err))

					
		
	for someurl in someurls:
		# Interact with the user and output file some more
		print('Checking ' + someurl, end=' -- ')
		w.write('Checked ' + someurl + ': ')
		# I was feeling a little prim when I added this output; why include http sometimes but not others?
		# Still, adding the [understood] http:// is easy and prevents needless errors.
		if (not '://' in someurl):
			someurl = 'http://' + someurl
			print('Needs URI scheme name indicated (http://, ftp://, etc.). \nTrying ' + someurl + ' instead:', end=' ')
			w.write('Needs URI scheme name indicated (http://, ftp://, etc.). \nTried ' + someurl + ': ')		
		# Send the request, with no data and that user agent lie
		req = Request(someurl, data=None, headers=theagent)
		# this should work in Python 3.3.3 but doesn't:
		#req = Request(someurl, data=None, headers=theagent, cafile=None, capath=None, cadefault=False)

		# I have questions about this structure; maybe I shouldn't be "except"ing the errors.
		# Perhaps they should be printed just like the successes in the try: statement.
		try:
		    response = urlopen(req)
		    # That long thing below tells you what code was returned 
		    # [0] tells it to give you the short version; [1] would be more verbose...
		    # ... and not a lot more helpful
		    thecode = http.server.BaseHTTPRequestHandler.responses[response.code][0]
		    print(thecode)
		    w.write(thecode + '\n')
		    # Check for redirects
		    if response.geturl() != someurl:
		    	print('The URL redirected. Consider updating ' + someurl + ' to ' + response.geturl())
		    	w.write('The URL redirected. Consider updating ' + someurl + ' to ' + response.geturl() + '\n')

		# Making the appropriate responses, in the case of errors
		# Pretty much copied verbatim from the Python docs, only output changed :)
		except URLError as e:
		    if hasattr(e, 'reason'):
		        print('We failed to reach a server.')
		        print('Reason: ', e.reason)
		        w.write('We failed to reach a server.')
		        w.write('Reason: ' + str(e.reason))
		    elif hasattr(e, 'code'):
		        print('The server couldn\'t fulfill the request.')
		        print('Error code: ', e.code)
		        w.write('The server couldn\'t fulfill the request.')
		        w.write('Error code: ' + str(e.code))
		    else:
		        # This should never happen. But if it does, it's something interesting!
		        print(someurl + "has something funky going on.")
		print(" ") # adds a double-space between entries
		w.write('\n\n') # adds a double-space between entries
	


# Cleaning up.				
w.close()

