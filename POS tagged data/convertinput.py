import json
temp = {}
json_data1 = json.load(open('crawl_cinema.json', 'r'))
for i in range(0,len(json_data1)):
    temp[i] = json_data1[i]

f = open('cinema_test.json','w')
json.dump(temp,f)

temp = {}
json_data1 = json.load(open('crawl_sports.json', 'r'))
for i in range(0,len(json_data1)):
    temp[i] = json_data1[i]

f = open('sports_test.json','w')
json.dump(temp,f)

temp = {}
json_data1 = json.load(open('crawl_statenews.json', 'r'))
for i in range(0,len(json_data1)):
    temp[i] = json_data1[i]

f = open('state_test.json','w')
json.dump(temp,f)