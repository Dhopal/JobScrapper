import requests, os, bs4, json, codecs, sys, time, datetime, calendar, errno, logging
import ast

list_of_jobs = []
tree_of_jobs = {}

def make_valid_string(s):
	return ((s.lstrip()).rstrip()).replace("\n"," ")

def find_vc_and_ac(date, job_id):
	d = str(date)
	while len(d) < 13:
		d = d + str('0')
	payload = {
	'adId': job_id,
	'postedDate': str(d)
	}
	r = requests.get(
		url='http://alerts.timesjobs.com/naf/node/jobInsight/getAppViewCount',
		data=payload,
		headers={'X-Requested-With': 'XMLHttpRequest'}
		)
	# print("date = " + str(date))
	# print("job_id = " + str(job_id))
	# print(r.text)
	return r.text

def scrap_job_details(URL):
	#print("Downloading job for url            : " + URL)
	url = URL
	res = requests.get(url)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, "html.parser")

    #first get the job id
	job_id = soup.find('div', attrs = {'class':'clearfix wrap jd-main-job-1'})['id']

	job_box = {
	    'job_id' : '',
	    'url' : '',
		'job_title' : '',
		'company_name' : '',
		'experience' : '',
		'salary' : '',
		'location' : '',
		'key_skills' : [],
		'job_function' : [],
		'job_industry' : [],
		'specialization' : '',
		'role' : '',
		'qualification' : [],
		'job_description' : [],
		'about_hiring_company' : '',
		'job_posted_by_company' : '',
		'desired_candidate_profile' : '',
		'posted_on' : '',
		'star' : '',
		'review_count' : '',
		'views_cnt' : '',
		'applied_cnt' : ''
	}
	job_box['job_id'] = job_id

	#posted_on
	posted_on = soup.select('#' + job_id + ' > section > section > div > div.jd-action-bottom.clearfix > div.posting-dtl > span.pstd-on')
	if len(posted_on) > 0:
		job_box['posted_on'] = make_valid_string(posted_on[0].text[11:])

	#view_count and applied_cnt
	date = datetime.datetime.strptime(job_box['posted_on'].replace(" ","").replace(",","").upper(), "%d%b%Y")
	postedDate = calendar.timegm(date.utctimetuple())
	data = ast.literal_eval(find_vc_and_ac(postedDate, job_id[5:]))
	print(job_id)
	print(data)
	print(postedDate)
	if len(data) > 0:
		job_box['views_cnt'] = str(data['data']['vc'])
		job_box['applied_cnt'] = str(data['data']['ac'])
	print(job_box['views_cnt'])
	print(job_box['applied_cnt'])
	#review_cnt
	review_cnt = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > div > div > a')
	if len(review_cnt) > 0:
		job_box['review_cnt'] = make_valid_string(review_cnt[0].text)
	#star
	star = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > div > div > span > span.star-fill')
	#print(str(star[0]['style'])[6:-1])
	if len(star) > 0:
		job_box['star'] = str(star[0]['style'])[6:-1]

	job_box['url'] = url

	#Job title
	job_name = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > h1 > span')
	if len(job_name) > 0:
		job_box['job_title'] = job_name[0].text

    #Hiring Company Name
	company_name = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > div > h2 > a > span')
	if len(company_name) > 0:
		job_box['company_name'] = make_valid_string(company_name[0].text)
	else:
		company_name = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > div')
		if len(company_name) > 0:
			job_box['company_name'] = make_valid_string(company_name[0].text)

	#Experience
	experience = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > ul > li:nth-of-type(1) > span:nth-of-type(2)')
	if len(experience) > 0:
		job_box['experience'] = make_valid_string(experience[0].text)


	#Salary
	salary = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > ul > li:nth-of-type(2) > span:nth-of-type(2)')
	if len(salary) > 0:
		job_box['salary'] = make_valid_string(salary[0].text)

	#Location
	location = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > ul > li:nth-of-type(3)')
	if len(location) > 0:
		job_box['location'] = make_valid_string(location[0].text)


	#key skills
	key_skills = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > section > span')
	if len(key_skills) > 0:
		skills_list = key_skills[0].text.split()
		job_box['key_skills'] = skills_list


	#job function
	job_function = soup.select('#applyFlowHideDetails_1 > li:nth-of-type(1) > span')
	if len(job_function) > 0:
		job_box['job_function'] = job_function[0].text


	#job industry
	job_industry = soup.select('#applyFlowHideDetails_1 > li:nth-of-type(2) > span')
	if len(job_industry) > 0:
		job_box['job_industry'] = job_industry[0].text


	#specialization
	specialization = soup.select('#applyFlowHideDetails_1 > li:nth-of-type(3) > span')
	if len(specialization) > 0:
		job_box['specialization'] = specialization[0].text


	#role
	role = soup.select('#applyFlowHideDetails_1 > li:nth-of-type(4) > span')
	if len(role) > 0:
		job_box['role'] = make_valid_string(role[0].text)


	#qualification
	qualification = soup.select('#applyFlowHideDetails_1 > li:nth-of-type(5) > span')
	qualification_list = []
	for ul in qualification:
	    for li in ul.findAll('li'):
	    	qualification_list.append(make_valid_string(li.text))
	job_box['qualification'] = qualification_list


	#job description [it needs to handle all paragraphs]
	job_description = soup.select('#applyFlowHideDetails_2')
	if len(job_description) > 0:
		job_box['job_description'] = make_valid_string(job_description[0].text)


	# about hiring company
	about_hiring_company = soup.select('#applyFlowHideDetails_4')
	if len(about_hiring_company) > 0:
		job_box['about_hiring_company'] = make_valid_string(about_hiring_company[0].text)

	#Job posted by company
	job_posted_by_company = soup.select('#applyFlowHideDetails_5')
	if len(job_posted_by_company) > 0:
		job_box['job_posted_by_company'] = make_valid_string(job_posted_by_company[0].text)

	#desired candidate profile
	desired_candidate_profile = soup.select('#applyFlowHideDetails_3')
	if len(desired_candidate_profile) > 0:
		job_box['desired_candidate_profile'] = make_valid_string(desired_candidate_profile[0].text)
	return job_box

if __name__ == "__main__":
	start = 0
	l = []
	with open('urls_for_jobs.txt') as f:
		lines = f.read().splitlines()
		for i in range(start,len(lines)):
			print('Downloading Job : ' + str(i) +  lines[i])
			with open('Jobs_json/'+str(str(i) + '.txt'), 'wb') as f:
				json.dump(scrap_job_details(lines[i]), codecs.getwriter('utf-8')(f), ensure_ascii=False)
			