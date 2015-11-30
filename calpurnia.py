#!/usr/bin/python3

import argparse
import scraper
import os.path
import sqlite3

def get_course_string(course):
	GREEN = '\033[92m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'


	course_string = BOLD + GREEN  + UNDERLINE+ course['section'] + '*' + course['code'] + " " + course['title'] + " [" + course['credit'] + "]\n"  +  END
	course_string = course_string + course['desc'] + "\n"
	
	if (course['off']):
		course_string = course_string + BOLD + "Offerings: "+ END + course['off'] + "\n"
	
	if (course['prereqs']):
		course_string = course_string + BOLD + "Prerequisites: "+ END + course['prereqs'] + "\n"
	
	if (course['restr']):
		course_string = course_string + BOLD + "Restrictions: "+ END + course['restr'] + "\n"

	return course_string

def make_db(verbose):
	if not os.path.exists('./_db/courses.db'):
		scraper.write_courses_to_db(verbose)


def build_query(course_list):
	query = 'SELECT * FROM courses WHERE'

	for course in course_list:
		code = course[-4:]
		sec = course[:-4]
		print (sec + ' code - ' + code)

		query += ' (section="'+sec.upper()+'" AND code="'+code+'") OR'

	query = query[:-2].strip()
	#print (query)
	return query 


def get_courses_from_db(course_list):
	conn = sqlite3.connect('./_db/courses.db')

	with conn:
		conn.row_factory = sqlite3.Row

		cur = conn.cursor()
		
		query = build_query(course_list)
		cur.execute(query)

		rows = cur.fetchall()

		for row in rows:
			print (get_course_string(row))
	

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('courses', nargs='+')

	args = parser.parse_args()

	'''
	for course in args.courses:
		try:
			
		except (KeyError):
			print ('Error: CIS*'+str(num) + ' is not an offered course.\n')
	'''

	get_courses_from_db(args.courses)


if __name__=='__main__':
	main()