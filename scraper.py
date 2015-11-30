from bs4 import BeautifulSoup
import urllib3

def get_courses_from_url(cal_url):
	http = urllib3.PoolManager()
	r = http.request('GET', cal_url)
	content = r.data
	soup = BeautifulSoup(content)

	courses = soup.find_all('div', attrs={"class":"course"})
	return courses

def get_course(course):
	# Get the title line with course code, title, semester list, and credits
	title_line = course.find('tr', class_="title").find('th').find('a').getText()
	
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

	# Make the course title
	title = title_line[9:-12].strip()
	
	# Make course code
	code = int(title_line[4:8])

	# Make course credit
	credit = title_line[-5:-1]

	# Return a dictionary of course data
	return {'code': code,
			'title': title,
			'sems': [],
			'credit':credit,
			'description':description,
			'offerings': offerings,
			'restrictions': restrictions,
			'prereqs': prereqs }

		
def make_courses_dict(courses):
	courses_dict = {}
	for course in courses:
		# Get the dictionary of data for each course
		course_dict = get_course(course)

		#MAdd to the dictionary of courses with course code as key
		courses_dict[course_dict['code']] = course_dict

	return courses_dict

def get_courses(url):
	courses = get_courses_from_url(url)
	courses_dict = make_courses_dict(courses)

	return courses_dict


