import os
for filename in os.listdir("samplein"):
    print filename+"-----"
    f2=open("sampleout/"+filename,'w')
    with open("samplein/"+filename) as f:
        for line in f:
            #print line
            if line.startswith('----'):
                break
            words = line.rstrip(".").split()
            #print words
        
            for word in words:
                print word
                f2.write(word.strip()+'\n')
            f2.write('.\n')
            f2.write('\n\n')