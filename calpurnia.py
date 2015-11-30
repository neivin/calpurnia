import argparse
import scraper
import os.path

def get_course_string(course):
	GREEN = '\033[92m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'


	course_string = BOLD + GREEN  + UNDERLINE+ "CIS*" + str(course['code']) + " " + course['title'] + " [" + course['credit'] + "]\n"  +  END
	course_string = course_string + course['description'] + "\n"
	
	if (course['offerings']):
		course_string = course_string + BOLD + "Offerings: "+ END + course['offerings'] + "\n"
	
	if (course['prereqs']):
		course_string = course_string + BOLD + "Prerequisites: "+ END + course['prereqs'] + "\n"
	
	if (course['restrictions']):
		course_string = course_string + BOLD + "Restrictions: "+ END + course['restrictions'] + "\n"

	return course_string


def get_courses_from

def main():

	CALENDAR_URL = 'https://www.uoguelph.ca/registrar/calendars/undergraduate/2015-2016/c12/c12cis.shtml'
	
	courses = scraper.get_courses(CALENDAR_URL)

	parser = argparse.ArgumentParser()
	parser.add_argument('courses', nargs='+', type=int)

	args = parser.parse_args()

	for num in args.courses:
		try:
			selected_course = courses[num]
			print (get_course_string(selected_course))
		except (KeyError):
			print ('Error: CIS*'+str(num) + ' is not an offered course.\n')

	scraper.get_depts_list('')

if __name__=='__main__':
	main()