# coding: UTF-8
# pip install ipykernel
# pip install mecab-python-windows
import MeCab as mec
import sys
import re
import math

def analyze(contents, number_of_line, debug):
    m = mec.Tagger("-Ochasen")
    texts = re.split('[。\n！？!?]', contents.replace('>',''))
    words_map = {}
    num_of_sentence = len(texts)
    _texts = []
    for txt in texts:
        res = m.parse(txt)
        _texts.append(res)
        lines = res.split('\n')
        items = (re.split('[\t,]', line) for line in lines)
        for item in items:
            try:
                top = item[2][0]
                if(top in words_map):
                    exist = False
                    for i in range(len(words_map[top])):
                        if(item[2] == words_map[top][i][0]):
                            words_map[top][i] = (item[2],words_map[top][i][1]+1)
                            exist = True
                            break
                    if(not exist):
                        words_map[top].append((item[2],1))
                else:
                    words_map[top] = [ (item[2],1) ] #(word,its number)
            except:
                pass

    for i in words_map:
        for j in range(len(words_map[i])):
            v = math.log(num_of_sentence / words_map[i][j][1])
            words_map[i][j] = (words_map[i][j][0],v)

    result = []
    for i in range(len(_texts)):
        sum_word = 0
        lines = _texts[i].split('\n')
        items = (re.split('[\t,]', line) for line in lines)
        for item in items:
            try:
                top = item[2][0]
                for j in words_map[top]:
                    if(j[0] == item[2]):
                        sum_word += j[1]
                        break
            except:
                pass
        if(not texts[i] == ''):
            result.append( (texts[i],sum_word) )
    if(debug):
        print("result")
        for i in result:
            print(i)
    ranks = [(-1,-1) for i in range(number_of_line)]
    for i in range(len(result)):
        for j in range(len(ranks)):
            if(ranks[j][1] < result[i][1]):
                exist = False
                for k in ranks:
                    if(not k[0] == -1):
                        if(result[i][0] == result[k[0]][0]):
                            exist = True
                            break
                if(exist):
                    break

                if( (not ranks[j][0] == -1) and (j+1) < number_of_line):
                    tmp = (ranks[j][0],ranks[j][1])
                    for k in range(j,number_of_line-2):
                        if(not ranks[k+1][0] == -1):
                            swap = (ranks[k+1][0],ranks[k+1][1])
                            ranks[k+1] = tmp
                            tmp = swap
                        else:
                            ranks[k+1] = tmp
                            break
                
                ranks[j] = (i,result[i][1])
                break

    res = {}
    for i in ranks:
        res[i[0]] = result[i[0]][0]
    res = sorted(res.items(), key=lambda x: x[0])
    _res = []
    for i in res:
        _res.append(i[1])
    return _res


#debug = False
#contents = None
#try:
#    with open(sys.argv[1], encoding="utf-8") as f:
#        contents = f.read()
#    if(sys.argv[3] == '-d'):
#        debug = True
#except:
#    pass
#res = analyze(contents, int(sys.argv[2]),debug)
#for i in res:
#    print(i)
