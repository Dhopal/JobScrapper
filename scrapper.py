import requests, os, bs4, json, codecs

def make_valid_string(s):
	return ((s.lstrip()).rstrip()).replace("\n"," ")


def scrap_job_details(URL):
	#print("Downloading job for url            : " + URL)
	url = URL
	#print('Downloading webpage...')
	res = requests.get(url)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, "html.parser")
    
    #first get the job id
	job_id = soup.find('div', attrs = {'class':'clearfix wrap jd-main-job-1'})['id']

	job_box = {
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
	#view_cnt
	views_cnt = soup.select('#ji_view_id_' + job_id[5:]) #'#jdsj-60174370'
	if len(views_cnt) > 0:
		job_box['views_cnt'] = make_valid_string(views_cnt[0].text)

	#applied_cnt
	applied_cnt = soup.select('#ji_apply_id_' + job_id[5:])
	if len(applied_cnt):
		job_box['applied_cnt'] = make_valid_string(applied_cnt[0].text)

	#review_cnt
	review_cnt = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > div > div > a')
	if len(review_cnt) > 0:
		job_box['review_cnt'] = make_valid_string(review_cnt[0].text)
	#star
	star = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > div > div > span > span.star-fill')
	#print(str(star[0]['style'])[6:-1])
	if len(star) > 0:
		job_box['star'] = str(star[0]['style'])[6:-1]

	#posted_on
	posted_on = soup.select('#' + job_id + ' > section > section > div > div.jd-action-bottom.clearfix > div.posting-dtl > span.pstd-on')
	if len(posted_on) > 0:
		job_box['posted_on'] = make_valid_string(posted_on[0].text)

	job_box['url'] = url

	#Job title
	job_name = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > h1 > span')
	if len(job_name) > 0:
		job_box['job_title'] = job_name[0].text

#jdsj-61378174 > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > div > h2	
    #Hiring Company Name
	company_name = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > div > h2 > a > span')
	if len(company_name) > 0:
		job_box['company_name'] = make_valid_string(company_name[0].text)
	else:
		company_name = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > div')
		if len(company_name) > 0:
			job_box['company_name'] = make_valid_string(company_name[0].text)

	#TODO
	#Rating star and Reviews
	reviews = soup.select('#' + job_id + ' > section > section > div > div.jd-header.clearfix > div.top-job-detail.clearfix > div > div > div > div > a')
	#print(reviews)

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
	#print(json.dumps(job_box))
	#print(job_box)

def scrap_site_map_page():
	all_times_jobs = {}
	url = 'http://www.timesjobs.com/jobs-sitemap/';
	total_page_cnt = 1
	job_cnt = 0
	for page_cnt in range(1, total_page_cnt + 1):
		all_times_jobs[str('jobs-sitemap/' + str(page_cnt))] = []

		new_url = url + str(page_cnt)
		print('Downloading webpage...' + str(new_url))
		res = requests.get(new_url)
		res.raise_for_status()
		soup = bs4.BeautifulSoup(res.text, "html.parser")
		total_sub_page_cnt = 60 #make it 60

		level2 = {}
		for i in range(1, total_sub_page_cnt + 1):
			sub_page_url = new_url + "/" + str(i)
			#print(sub_page_url)
			jobs_res = requests.get(sub_page_url)
			jobs_res.raise_for_status()
			jobs_soup = bs4.BeautifulSoup(jobs_res.text, "html.parser")
			#cnt = 0
			level2[str('jobs-sitemap/' + str(page_cnt) + '/' + str(i))] = []
			for a in jobs_soup.find_all('a',href=True):
				x = a['href']
				if x.startswith('http://www.timesjobs.com/job-detail/'):
					#print(x)
					job_cnt += 1
					print("job_cnt = " + str(job_cnt))
					level2[str('jobs-sitemap/' + str(page_cnt) + '/' + str(i))].append(scrap_job_details(x))

		
		all_times_jobs[str('jobs-sitemap/' + str(page_cnt))].append(level2)
	return all_times_jobs
	#print(json.dumps(all_times_jobs))
    
if __name__ == "__main__":
	data = scrap_site_map_page()
	with open('data.txt', 'wb') as f:
		json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)