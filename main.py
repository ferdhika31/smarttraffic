#!/usr/bin/env python2
from bottle import *

from pprint import pprint

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

import time

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

@route('/visualisasi')
@view('visualisasi')
def visualisasi():
	return { 'apptitle':'SmartTraffic', 'root':request.environ.get('SCRIPT_NAME') }

@route('/klasifikasi')
@view('klasify')
def klasifikasi():
	return { 'apptitle':'SmartTraffic', 'root':request.environ.get('SCRIPT_NAME') }

@route('/cekKla')
@post('cekKla')
def cekKla():
	txt = request.forms.get('teks', '07.27 waktu indonesia barat situasi lalu lintas jl jakarta sampai purwakarta terpantau ramai')

	return klasify(txt)

@route('/crawling')
@post('/crawling')
def crawling():
	response.content_type = 'application/json'

	# dishub_bdgkab
	# LalinProyek
	data = getTweet('tmc_restabesbdg',5)

	kirim = json.dumps(data, sort_keys=True, indent=5) 

	return kirim

@route('/tweet')
@post('/tweet')
def tweet():
	response.content_type = 'application/json'

	maxTweet = request.forms.get('maxTweet', 5)

	# dishub_bdgkab
	# LalinProyek
	data = getTweet('tmc_restabesbdg', maxTweet)

	# Inisialisasi atau kalo ada kamus yng baru
	init_kamus()
	init_data_jalan() 

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
		# data jalan
		txtNormal = jalan(txtNormal)

		# Postag
		postag = tag(txtNormal)

		# Classify
		classify = klasify(txtNormal.replace('.',' '))

		# Sentence
		sntc = json.loads(sentence(postag))

		if sntc.has_key("sampai"):
			txtSentence = {
				'idTweet'   : item['id'],
				'dari'		: sntc['dari'].replace('.',' '),
				'sampai'	: sntc['sampai'].replace('.',' '),
				'waktu'		: time.strftime('%d-%m-%Y', time.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),
				'pukul'		: sntc['jam'],
				'kondisi'	: classify
			}

			kirim.append(txtSentence)
			# Simpan text sentence ke db
			if not db.TweetSentence.find_one({ 'idTweet': item['id'] }):
				db.TweetSentence.insert_one(txtSentence)
		elif sntc.has_key("dari"): #kalo ada data
			txtSentence = {
				'idTweet'   : item['id'],
				'dari'		: sntc['dari'].replace('.',' '),
				'waktu'		: time.strftime('%d-%m-%Y', time.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),
				'pukul'		: sntc['jam'],
				'kondisi'	: classify
			}

			kirim.append(txtSentence)
			# Simpan text sentence ke db
			if not db.TweetSentence.find_one({ 'idTweet': item['id'] }):
				db.TweetSentence.insert_one(txtSentence)


	kirim = json.dumps(kirim, sort_keys=True, indent=5) 

	return kirim

@route('/contoh')
def contoh():
	response.content_type = 'application/json'
	
	# dishub_bdgkab
	# LalinProyek
	data = getTweet('tmc_restabesbdg',5)

	# init_kamus()
	# init_data_jalan()

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
		# data jalan
		txtNormal = jalan(txtNormal)

		kirim.append({
			'id'        : item['id'],
			'text'      : text,
			'hari'		: time.strftime('%a', time.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),
			'created_at': time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),
			'normal'	: txtNormal,
			'tagger'	: tag(txtNormal),
			'sentence'	: sentence(tag(jalan(txtNormal)), jalan(txtNormal))
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
