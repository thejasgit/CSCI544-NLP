import os
import json

json_data1 = json.load(open('testdata/cinema_test.json', 'r'))
json_data2 = json.load(open('testdata/sports_test.json', 'r'))
json_data3 = json.load(open('testdata/state_test.json', 'r'))
for filename in os.listdir("rsamplein"):
    print filename+"-----"
    #id = filename.split('_')[0]
	id = filename[0]
	d = filename[1]
	if d.isdigit():
		id=id+d
	
    category = filename.split('_')[1].split(".")[0]
    f2=open("rsampleout/out_"+filename,'w')
    content = []
    with open("rsamplein/"+filename) as f:
        strlin = ''
        for line in f:
            #print line
            #print line
            if line.startswith('\n'):
                continue
            elif line.startswith('.\t'):
                 print strlin
                 if strlin=='':
                    continue
                 content.append(strlin.rstrip().rstrip('.'))
                 f2.write(strlin.rstrip()+'.\n')
                 strlin = ''
            else:
                
                temp = []
                words = line.split('\t',1)
                #print words
                strlin+=words[0]

                tag = words[1][0:3].rstrip('.')
                strlin+="/"+tag+" "
                #print words
        if category.strip()=='cinema':
           json_data1[id]['pos'] = content
        elif category.strip()=='sports':
           json_data2[id]['pos'] = content
        else:
           json_data3[id]['pos']= content
c = open('testdata/tag/cinema_test.json', 'w') 
json.dump(json_data1,c)
c.close()
c = open('testdata/tag/sports_test.json', 'w') 
json.dump(json_data2,c)
c.close()
c = open('testdata/tag/state_test.json', 'w')
json.dump(json_data3,c)
c.close()