from lxml.html import parse
import sqlite3
import time
def getpage(c,conn):
  baseurl = 'http://www.wordhacker.com/en/article/Barron_gre_list_%s.htm'
	alphabets = [ 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z' ]
	for alphabet in alphabets:
		url = baseurl %(alphabet)
		word(url,c,conn)
def scrape(url):
	page = parse(url).getroot()
	sect = page.cssselect('table')[3]
	thetable = sect.cssselect('table')[2]
	rows = thetable.cssselect('tr')
	return rows
def word(url,c,conn):
	for r in scrape(url):
		x = r.cssselect('td')[0]
		if x.text_content().strip()[0] == 'B':
			continue
		#There were some words which had some characters out of Unicode, and couldn't be parsed...so we skip them
		if x.text_content().strip() == 'bitter':
			continue
		if x.text_content().strip() == 'dominate':
			continue
		if x.text_content().strip() == 'plume':
			continue		
		if x.text_content().strip() == 'scotch':
			continue		
		meanings = r.cssselect('td')[1]
		meaning = meanings.text_content().strip()
		word = x.text_content().strip()
		data = (word, meaning)
		c.execute('insert into vocab values (? ,?)' , data)
		conn.commit()
		print word,'is added to your database.'		
if __name__ == '__main__':
	#You should have already initialised an sqlite database, with appropriate schema.
	conn = sqlite3.connect('./database.db')
	c = conn.cursor()
	getpage(c,conn)
