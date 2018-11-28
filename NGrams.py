import re
import codecs

def preProcess(line):
        # strip line, break into words
        # extracting the text sentence from each line
        line = "".join(line.split())
        line = line.lower()   # to lower case
        line = re.sub(r"\d+", "", line) # remove digits
        line = re.sub(r'[^\w\s]','',line)  #remove punctutations
        line=re.sub(' +',' ',line)
        #print line
        return list(line)

def countNgram(tokens,order):
    pairs=dict()
    if len(tokens)<order:
        #print pairs
        return pairs

    for i in range( len(tokens) - (order+1) ):
        pair=tuple(tokens[i:i + order])
        if pair not in pairs:
            pairs[pair]=0
        pairs[pair]+=1
    return pairs

def ngramPrint(ngramDict):
    sum = 0
    for key,val in sorted(ngramDict.iteritems()):
        sum+=val
        print ''.join(key)+":"+str(val)
    print "Assorted Count : ", sum

def combinedCounts(countList):
    merged=dict()
    for pairs in countList:
        for key, val in pairs.iteritems():
            if key not in merged:
                merged[key] = 0
            merged[key] += val
    return merged

def smoothen(assortedDict, ngram):
    for i in range(ord('a'), ord('z')+1):
        smoothenDict(assortedDict,  tuple(chr(i).decode('utf-8')), ngram)

absentLexemList = list()
def smoothenDict(assortedDict, lexem, iterIndex):
  if(iterIndex == 0):
    if(lexem not in assortedDict.keys()):
        assortedDict[lexem] = 0
        absentLexemList.append(lexem)
    return
  else:
      for i in range(ord('a'),ord('z')+1):
        searchStr = (lexem + tuple(chr(i).decode('utf-8')))
        smoothenDict(assortedDict, searchStr, iterIndex - 1)

def finalizeCount(assortedDict):
     for key in assortedDict.keys():
         if key in absentLexemList:
             assortedDict[key] += 1

if __name__ == "__main__":
    unigramEn=list()
    bigramEn=list()
    trigramEn = list()
    unigramPairsEn = dict()
    bigramPairsEn = dict()
    triGramPairsEn = dict()
    for line in codecs.open('D:/Code/python/Ngram/TrainingCorpusENandFR/enCorpus.txt','r','utf-8'):
        tokens=preProcess(line)
        unigramEn.append(countNgram(tokens,1))
        bigramEn.append(countNgram(tokens,2))
        trigramEn.append(countNgram(tokens,3))
    unigramPairsEn=combinedCounts(unigramEn)
    bigramPairsEn=combinedCounts(bigramEn)
    triGramPairsEn = combinedCounts(trigramEn)
    #smoothen
    smoothen(unigramPairsEn, 0)
    smoothen(bigramPairsEn, 1)
    smoothen(triGramPairsEn, 2)
    finalizeCount(unigramPairsEn)
    finalizeCount(bigramPairsEn)
    finalizeCount(triGramPairsEn)
    ngramPrint(unigramPairsEn)
    ngramPrint(bigramPairsEn)
    ngramPrint(triGramPairsEn)
