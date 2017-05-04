#!/usr/bin/env python2
from bottle import *

from nltk.tokenize import TweetTokenizer

try:
	from google.appengine.ext import webapp
	from google.appengine.ext.webapp import util
	isGAE = True
except:
	isGAE = False
	pass

import json, re

from libtraffic import *

@route('favicon.ico')
def favicon():
	return static_file('favicon.ico', root='static/')

@route('/')
@view('home')
def index():
	return { 'apptitle':'SmartTraffic', 'root':request.environ.get('SCRIPT_NAME') }

@route('/test')
def test():
	response.content_type = 'application/json'

	init_data_jalan()
	teks = "06.31 wib arus lalu lintas di jl.ters buah batu sampai aceh terpantau meriah lancar"

	res = tag(jalan(teks))

	return sentence(res)

@route('/tweet')
@post('/tweet')
def tweet():
	response.content_type = 'application/json'

	maxTweet = request.forms.get('maxTweet', 10)
	
	# dishub_bdgkab
	# LalinProyek
	data = getTweet('LalinProyek',maxTweet)

	kirim = []

	no = 1
	for item in data:
		
        # Hapus link yang ada di kalimat
		text = remove_urls(item['text']).lower()
		# replace -
		text = text.replace("-", " - ")
		# Tokenizer
		tknzr = TweetTokenizer()
		tok = tknzr.tokenize(text)

		# Normalisasi lewat kamus
		txtNormal = ""
		n=1
		for kata in tok:
			# print kata
			data = db.KamusNormalisasi.find_one({ 'kata': kata })
			if n != 1:
				txtNormal += " "

			if data:
				txtNormal += data['maksud']
			else :
				txtNormal += kata
			n=n+1

		#remove mention
		txtNormal = remove_mention(txtNormal)

		kirim.append({
			'id'        : item['id'],
			'text'      : text,
			'created_at': item['created_at'],
			'normal'	: jalan(txtNormal),
			'tagger'	: tag(jalan(txtNormal)),
			'sentence'	: sentence(tag(jalan(txtNormal)))
		})

		no=no+1

	kirim = json.dumps(kirim, sort_keys=True, indent=5)  

	return kirim

@post('/handler')
def default_handler():
	maxTweet = request.forms.get('maxTweet', '')
	refreshKamus = request.forms.get('refereshKamus')

	if(int(refreshKamus)==1):
		init_kamus()
		init_data_jalan()
		print "Refresh kamus"
	
	return tweet()

	# response.content_type = 'text/plain'
	# return value

@route('/static/:fname#.+#')
def servestatic(fname):
    return static_file(fname, root='static/')

def main():
    if isGAE:
        util.run_wsgi_app(default_app())
    else:
        init_tag()
        run(host='localhost', port=8081, reloader=True, debug=True)

if __name__ == '__main__':
    main()
