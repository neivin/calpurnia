#!/usr/bin/python3
from bs4 import BeautifulSoup
import urllib3
import sqlite3

INDEXURL = 'https://www.uoguelph.ca/registrar/calendars/undergraduate/2015-2016/c12/index.shtml'

def get_depts_list(index_url):
	#index_url = 'https://www.uoguelph.ca/registrar/calendars/undergraduate/2015-2016/c12/index.shtml'
	
	http = urllib3.PoolManager()
	r = http.request('GET', index_url)
	content = r.data
	soup = BeautifulSoup(content)

	depts_soup = soup.find('div', class_='subnav').find_all('a')
	depts = []

	for dept in depts_soup:
		depts.append(dept['href'][5:-6])

	# Remove index.shtml item from list
	return depts[1:]


def get_courses_from_url(cal_url):
	http = urllib3.PoolManager()
	r = http.request('GET', cal_url)
	content = r.data
	soup = BeautifulSoup(content)

	courses = soup.find_all('div', attrs={"class":"course"})
	return courses

def get_course(course):
	# Get the title line with course code, title, semester list, and credits
	title_line = course.find('tr', class_="title").find('th').find('a').getText().strip()
	
	# Get the course description
	desc_line = course.find('tr', class_="description").find('td').getText().strip();
	
	# Fix stupid formatting from Guelph website (turn multiple spaces into one)
	description = ' '.join(desc_line.split())

	# Get the offerings line if the course has it
	offerings_line = course.find('tr', class_="offerings")
	# Set Default prereqs
	offerings = ''
	if offerings_line is not None:
		offerings = offerings_line.find('td').text.strip()

	# Get the prereqs line if the course has it
	prereqs_line = course.find('tr', class_="prereqs")
	# Set Default prereqs
	prereqs = ''
	if prereqs_line is not None:
		prereqs = prereqs_line.find('td').text.strip()

	# Get restrictions line
	restrictions_line = course.find('tr', class_="restrictions")
	# Set Default prereqs
	restrictions = ''
	if restrictions_line is not None:
		restrictions = restrictions_line.find('td').text.strip()

	# Get departments
	deps_line = course.find('tr', class_="departments").find('td').text.strip()

	first_space_index = title_line.index(' ')

	# Make the course title
	title = title_line[first_space_index:-12].strip()
	
	# Make course code
	star_index = title_line.index('*')

	section = title_line[:star_index]
	code = title_line[(star_index+1):first_space_index]

	# Make course credit
	credit = title_line[-5:-1]

	# Return a dictionary of course data
	return {'section': section,
			'code': code,
			'title': title,
			'sems': [],
			'credit':credit,
			'description':description,
			'offerings': offerings,
			'restrictions': restrictions,
			'prereqs': prereqs,
			'dept': deps_line }

		
def make_courses_list(courses):
	courses_list = []
	for course in courses:
		# Get the dictionary of data for each course
		course_dict = get_course(course)

		# Add to the list of courses
		courses_list.append(course_dict)

	return courses_list

def get_courses(url):
	courses = get_courses_from_url(url)
	courses_list = make_courses_list(courses)

	return courses_list

def write_courses_to_db(verbose):
	if verbose:
		print ('Building database of courses...')

	conn = sqlite3.connect('./_db/courses.db')
	cur = conn.cursor()
	
	depts_list = get_depts_list(INDEXURL)

	# Create the db table
	cur.execute("DROP TABLE IF EXISTS courses")
	cur.execute("CREATE TABLE courses (section TEXT, code TEXT, title TEXT, credit TEXT, desc TEXT, off TEXT, restr TEXT, prereqs TEXT, dept TEXT, PRIMARY KEY (section, code))")
	
	for dept in depts_list:
		# Make the url for each department
		dept_url = 'https://www.uoguelph.ca/registrar/calendars/undergraduate/2015-2016/c12/c12'+ dept + '.shtml'
		
		# Make a dicitionary for the department courses
		dept_courses_list = get_courses(dept_url)

		if verbose:
			print("Adding "+dept.upper()+ " courses...")
		# Add all the courses into the db
		for course in dept_courses_list:
			cur.execute("INSERT INTO courses VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (course['section'], course['code'], course['title'], course['credit'], course['description'], course['offerings'], course['restrictions'], course['prereqs'], course['dept'] ))
		
		conn.commit()

	conn.close()

