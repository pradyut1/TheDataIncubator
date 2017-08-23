import numpy as np
import pandas as pd


def get_word_count_maps(df):
    backGrndWordCounts = {}
    totalBackGrndCount = 0

    badRevWordCounts = {}
    badRevTotalCount = 0

    goodRevWordCounts = {}
    goodRevTotalCount = 0

    for rating, line in zip(df.rating.tolist(), df.fullText.tolist()):
        words = line.split(" ")

        for word in words:
            if word == "":
                continue

            totalBackGrndCount = totalBackGrndCount + 1
            if word in backGrndWordCounts:
                backGrndWordCounts[word] = backGrndWordCounts[word] + 1
            else:
                backGrndWordCounts[word] = 1

            if rating <= 2:
                if word in badRevWordCounts:
                    badRevWordCounts[word] = badRevWordCounts[word] + 1
                else:
                    badRevWordCounts[word] = 1

                badRevTotalCount = badRevTotalCount + 1

            if rating >= 4:
                if word in goodRevWordCounts:
                    goodRevWordCounts[word] = goodRevWordCounts[word] + 1
                else:
                    goodRevWordCounts[word] = 1

                goodRevTotalCount = goodRevTotalCount + 1
                
    with open('word_counts.csv', 'w') as word_count_file:
        for w in backGrndWordCounts:
            bgCount = backGrndWordCounts[w]
            word_count_file.write(w+","+str(backGrndWordCounts[w])+",")

            goodCount = 0
            if w in goodRevWordCounts:
                goodCount = goodRevWordCounts[w]
                word_count_file.write(str(goodRevWordCounts[w])+",")
            else:
                word_count_file.write("0,")

            badCount = 0
            if w in badRevWordCounts:
                badCount = badRevWordCounts[w]
                word_count_file.write(str(badRevWordCounts[w])+",")
            else:
                word_count_file.write("0,")

            delta = np.log((goodCount + bgCount)/(goodRevTotalCount+totalBackGrndCount - goodCount - bgCount)
                          ) - np.log((badCount + bgCount)/(badRevTotalCount+totalBackGrndCount - badCount - bgCount))

            sigma = np.sqrt(1/(goodCount + bgCount) + 1/(badCount + bgCount))

            z = delta/sigma
            word_count_file.write(str(z) + "\n")
            
    df_counts =  pd.read_csv('word_counts.csv', header=None,
                         names=['word', 'globalCount', 'goodCount', 'badCount', 'zScore'])
    
    df_counts = df_counts[df_counts.globalCount >= 10].sort_values(by=['zScore'], ascending=False)
    
    return df_counts

def get_bigram_count_maps(df):
    backGrndWordCounts = {}
    totalBackGrndCount = 0

    badRevWordCounts = {}
    badRevTotalCount = 0

    goodRevWordCounts = {}
    goodRevTotalCount = 0

    for rating, line in zip(df.rating.tolist(), df.fullText.tolist()):
        words = line.split(" ")

        if len(words) <= 1:
            continue
            
        for i in range(0, len(words)-1):
            word1 = words[i]
            word2 = words[i+1]
            
            if word1 == "" or word2 == "":
                continue
                
            word = word1 + "_" + word2

            totalBackGrndCount = totalBackGrndCount + 1
            if word in backGrndWordCounts:
                backGrndWordCounts[word] = backGrndWordCounts[word] + 1
            else:
                backGrndWordCounts[word] = 1

            if rating <= 2:
                if word in badRevWordCounts:
                    badRevWordCounts[word] = badRevWordCounts[word] + 1
                else:
                    badRevWordCounts[word] = 1

                badRevTotalCount = badRevTotalCount + 1

            if rating >= 4:
                if word in goodRevWordCounts:
                    goodRevWordCounts[word] = goodRevWordCounts[word] + 1
                else:
                    goodRevWordCounts[word] = 1

                goodRevTotalCount = goodRevTotalCount + 1
                
    with open('bigram_counts.csv', 'w') as word_count_file:
        for w in backGrndWordCounts:
            bgCount = backGrndWordCounts[w]
            word_count_file.write(w+","+str(backGrndWordCounts[w])+",")

            goodCount = 0
            if w in goodRevWordCounts:
                goodCount = goodRevWordCounts[w]
                word_count_file.write(str(goodRevWordCounts[w])+",")
            else:
                word_count_file.write("0,")

            badCount = 0
            if w in badRevWordCounts:
                badCount = badRevWordCounts[w]
                word_count_file.write(str(badRevWordCounts[w])+",")
            else:
                word_count_file.write("0,")

            delta = np.log((goodCount + bgCount)/(goodRevTotalCount+totalBackGrndCount - goodCount - bgCount)
                          ) - np.log((badCount + bgCount)/(badRevTotalCount+totalBackGrndCount - badCount - bgCount))

            sigma = np.sqrt(1/(goodCount + bgCount) + 1/(badCount + bgCount))

            z = delta/sigma
            word_count_file.write(str(z) + "\n")
            
    df_counts =  pd.read_csv('bigram_counts.csv', header=None,
                         names=['bigram', 'globalCount', 'goodCount', 'badCount', 'zScore'])
    
    df_counts = df_counts[df_counts.globalCount >= 10].sort_values(by=['zScore'], ascending=False)
    
    return df_counts