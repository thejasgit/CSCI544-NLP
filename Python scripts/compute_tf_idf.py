from __future__ import division, unicode_literals

import re
from textblob import TextBlob as tb
import json
import math
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pickle

detailsdata = []
jsonft = []
class TfIdf:

    def __init__(self, corpusPath, outDir ):
        self.cps = corpusPath
        self.corpus = ""#json.load(open(corpusPath[0], 'r'))
        self.outFileDir = outDir

        if not os.path.exists(self.outFileDir):
            os.makedirs(self.outFileDir)
        self.reg = re.compile('\. |\.\xa0')
        self.wordDfDict = {}
        self.trainBloblist = []
        self.testBloblist = []
        self.trainBloblistLength = 0
        self.testBloblistLength = 0
        self.postags = {}
        #gss
        with open('gss.pickle','r') as f:
            self.gss = pickle.load(f)
        with open('allDicts.pickle','r') as f:
            l = pickle.load(f)
            self.categoryWordDict = []
            self.categoryWordDict.append(l[0])
            self.categoryWordDict.append(l[1])
            self.categoryWordDict.append(l[2])
            self.categoryDictLength = l[3]
            self.cindex = l[4]


    def setup(self):
        for cp in self.cps:
            self.corpus = json.load(open(cp, 'r'))
            self.buildCorpus()
        self.calculateDf()

    def tf(self,blob):
        out = {}
        for word in blob.words:
            if word not in out:
                out[word] = 0
            out[word] += 1
        for key,value in out.iteritems():
            out[key] = value/len(blob.words)
        return out

    def computeIdf(self, df):
        return math.log(self.trainBloblistLength + 1 / (1 + df))

    def buildCorpus(self):
        for i in range(0,len(self.corpus)):
            content = '. '.join(self.corpus[i]['content'])
            content.replace('..','.')
            self.trainBloblist.append(tb(content))
        self.trainBloblistLength = len(self.trainBloblist)

    def buildTestData(self):
        self.testBloblist = {}
        for key, value in self.dev.iteritems():
            content = '. '.join(self.dev[key]['content'])
            content.replace('..','.')
            self.testBloblist[key] = (tb(content))
        self.testBloblistLength = len(self.testBloblist)

    def calculateDf(self):
        for i, blob in enumerate(self.trainBloblist):
            #print i
            for word in set(blob.words):
                if word not in self.wordDfDict:
                    self.wordDfDict[word] = 0
                self.wordDfDict[word] += 1

    def grabTags(self,key):
        self.postags = {}
        print str(key)
        arr = self.dev[key]['pos']  
        #print str(arr)      
        for x in range(0,len(arr)):
            line = arr[x]            
            wrds = line.split(' ')  
            #print str(line)
            #print str(wrds)
            for word in wrds:
                #print str(word)                
                wd = word.split('/')[0].strip().rstrip('.')
                tag = word.split('/')[1].strip().rstrip('.')
                self.postags[wd] = tag.strip()

    def extractSummary(self, devPath, outFileName):
        self.dev = json.load(open(devPath, 'r'))
        print len(self.dev)
        self.buildTestData()
        out = {}
        c = {0:0,1:0,2:0}
        for i, blob in self.testBloblist.iteritems():
            cn = self.getCategoryNumber(blob)
            c[cn] += 1
            self.grabTags(i)
            #print str(self.postags)
            sentenceList = self.reg.split(unicode(blob))
            sentenceRankDict = {}
            sentenceRankDict2 = {}
            tfw = self.tf(blob)
            for j in range(0,len(sentenceList)):
                sentence = tb(sentenceList[j])
                sentenceRank = 0
                sentenceRank2 = 0 
                for word in sentence.words:
                    if word in self.wordDfDict:
                        tf = tfw[word]
                        df = self.wordDfDict[word]
                        tfIdf = tf * self.computeIdf(df+1)
                        gss = 0
                        if word in self.gss:
                            gss = tf*self.gss[word][cn]
                        sentenceRank += (tfIdf + gss)
                    if word in self.postags and word in self.wordDfDict and (self.postags[word] not in ['PRP','PSP','RP','SYM']):
                        tf = tfw[word]
                        #print str(word)
                        #print str(self.postags[word]) 
                        df = self.wordDfDict[word]
                        tfIdf = tf * self.computeIdf(df+1)
                        gss = 0
                        if word in self.gss:
                            gss = tf*self.gss[word][cn]
                        sentenceRank2 += (tfIdf + gss)

                if sentenceRank != 0:
                    sentenceRankDict[sentence] = [sentenceRank, j]

                if sentenceRank2 != 0:
                    sentenceRankDict2[sentence] = [sentenceRank2, j]

            topSentences = sorted(sentenceRankDict.items(), key=lambda x: x[1][0], reverse=True)

            topSentencespos = sorted(sentenceRankDict2.items(), key=lambda x: x[1][0], reverse=True)
            #deciding
            topSentencesToFile = ""
            topSentencesToFilepos = ""
            #select 20% of article, with min = 4 , max = 6 sentences
            numberOfSentence = int(math.floor(0.2*len(sentenceList)))
            if  numberOfSentence > 6:
                numberOfSentence = 6
            elif numberOfSentence < 4:
                numberOfSentence = 4

            topSentences = sorted(topSentences[:numberOfSentence], key=lambda x: x[1][1])
            topSentencespos = sorted(topSentencespos[:numberOfSentence], key=lambda x: x[1][1])

            for sentence, sentenceNumber in topSentences:
                topSentencesToFile += format(sentence)+". \n"

            for sentence, sentenceNumber in topSentencespos:
                topSentencesToFilepos += format(sentence)+". \n"

            out[i] = {"text" : topSentencesToFile}
            articleNumber = i
            sentencesToFile = ""
            for sentence in sentenceList:
                sentencesToFile += format(sentence)+". \n"
            t = outFileName.split(".")[0]
            self.writeToFile(str(articleNumber)+'_'+t, sentencesToFile, topSentencesToFile,topSentencesToFilepos)
            jsonft.append({ "id": articleNumber+t, "data" : sentencesToFile, "summary": topSentencesToFile, "summarypos": topSentencesToFilepos   })
        print (c)
        detailsdata.append(c)
        outfileName = "system_"+outFileName
        with open(outfileName, 'w') as outfile:
            json.dump(out, outfile)

    def getCategoryNumber(self, blob):
        #naive bayes to determine category
        out = [1.0, 1.0, 1.0]
        #cinema     #state        #sports
        for i in range(0, len(self.cindex)):
            #out[i] *= self.categoryDictLength[i]/ (sum(self.categoryDictLength)- self.categoryDictLength[i]) # prior
            for word in blob.words:
                if word in self.categoryWordDict[i]:
                    out[i] = out[i]*math.log( self.categoryWordDict[i][word]/self.categoryWordDict[i]["total_words_category"])
        return out.index(max(out))


    def writeToFile(self, articleNumber, sentencesToFile, topSentencesToFile ,topSentencesToFilepos):
        outfileName = os.path.join(self.outFileDir, articleNumber + ".txt")
        outfileNamesum = os.path.join(self.outFileDir+'/summary', articleNumber + ".txt")
        outfileNamepos = os.path.join(self.outFileDir+'/possummary', articleNumber + ".txt")
        outFile = open(outfileName, 'w')
        outFilesum = open(outfileNamesum, 'w')
        outFilepos = open(outfileNamepos, 'w')
        outFile.write(sentencesToFile)
        outFile.write('\n')
        outFile.write("--------------------- Summary -----------------------------")
        outFile.write('\n')
        outFile.write(topSentencesToFile)
        outFile.write("--------------------- POS Summary -----------------------------")
        outFile.write('\n')
        outFile.write(topSentencesToFilepos)
        outFile.close()
        outFilesum.write(topSentencesToFile)
        outFilepos.write(topSentencesToFilepos)
        outFilepos.close()
        outFilesum.close()





corpusPath = ["Crawler/corpuscrawler/udayavani_cinema_news.json", "Crawler/corpuscrawler/udayavani_sports_news.json", "Crawler/corpuscrawler/udayavani_state_news.json"]
#corpusPath = ["cinema_test.json", "state_test.json","sports_test.json"]
progress = open('progress.txt', 'w')
progress.write('0')
progress.close()
t = TfIdf(corpusPath, 'results' )
t.setup()
#t.extractSummary("Crawler/corpuscrawler/crawl_cinema.json", "cinema.json")
#t.extractSummary("Crawler/corpuscrawler/crawl_state.json", "state.json")
#t.extractSummary("Crawler/corpuscrawler/crawl_sports.json", "sports.json")
details = open('tfidfdetails.txt', 'w')


t.extractSummary("Crawler/corpuscrawler/cinema_test.json", "cinema.json")
progress = open('progress.txt', 'w')
progress.write('30')
progress.close()
t.extractSummary("Crawler/corpuscrawler/state_test.json", "state.json")
progress = open('progress.txt', 'w')
progress.write('60')
progress.close()
t.extractSummary("Crawler/corpuscrawler/sports_test.json", "sports.json")
json.dump(detailsdata,details)
details.close()
summaryjsn = open('summaryjson.txt', 'w')
json.dump(jsonft,summaryjsn)
summaryjsn.close()
progress = open('progress.txt', 'w')
progress.write('100')
progress.close()