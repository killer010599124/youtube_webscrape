import requests
import json
import csv  

col = row = 0
job_total = [[0 for x in range(row)] for x in range(col)]
users_data = [[0 for x in range(row)] for x in range(col)]
def get_reviews(skill_detail, user_name, user_id, profile_limit=10):
    profile_url = 'https://www.freelancer.com/api/projects/0.1/reviews/'
    params = {"limit": profile_limit, "role": "freelancer", "to_users[]": user_id, "project_details": "true", "contest_details": "true", "project_job_details": "true", "contest_job_details": "true", "review_types[]": "contest", "review_types[]": "project", "webapp": "1", "compact": "true", "new_errors": "true", "new_pools": "true"}

    project_id = 0
    skill = []
    job = []

    html_requests = requests.get(profile_url,params)
        
    total_json_data = html_requests.text

    json_data = json.loads(total_json_data)
    # print(json_data['result']['projects'])
    # job title and reviews
    for review_item in json_data['result']['reviews']:
        project_id = review_item['project_id']
        project_id = str(project_id)
        for skill_item in json_data['result']['projects'][project_id]['jobs']:
            skill.append(skill_item['seo_url'])
        job.append(skill_detail)
        job.append(user_name)
        job.append(skill)
        job.append(review_item['review_context']['context_name'])
        job.append(review_item['description'])

        job_total.append(job)
        job = []
        skill = []
        
user_name = ''
user_id = 0
person_data = []
profile_limit = 50
skill_detail = ''
job = []
users_url = 'https://www.freelancer.com/api/users/0.1/users/directory/'
users_params = {'limit':70,'offset':400,'query':'','avatar':'true','country_details':'true','display_info':'true','job_ranks':'true','jobs':'true','location_details':'true','online_offline_details':'true','preferred_details':'true','profile_description':'true','pool_details':'true','qualification_details':'true','reputation':'true','status':'true','webapp':'1','compact':'true','new_errors':'true','new_pools':'true'}


html_requests = requests.get(users_url,users_params)
total_json_data = html_requests.text
json_data = json.loads(total_json_data)

for user_item in json_data['result']['users']:
    user_name = user_item['username']
    user_id = user_item['id']
    skill_detail = user_item['tagline']
#    all_review = user_item['reputation']['reviews']
    person_data.append(user_id)
    person_data.append(user_name)
    person_data.append(skill_detail)
#    person_data.append(all_review)
    users_data.append(person_data)
    person_data = []
i=0
for user_data in users_data:
    i= i+1
    
    print(user_data[1], i)
    get_reviews(user_data[2],user_data[1], user_data[0])

with open('product2.csv', 'w', encoding='UTF8', newline='') as f:

        writer = csv.writer(f)

        writer.writerows(job_total)

f.close()

print('----------end---------')
