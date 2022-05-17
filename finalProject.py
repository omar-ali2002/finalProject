import re
import random as rd
import math


def filteringDataset(filename):
    file=open(r"C:\Users\omara\Desktop\Health-News-Tweets DATASET\Health-Tweets\{}".format(filename)+".txt",'r', encoding="utf8") # encoding="utf8" -->without this we get <UnicodeDecodeError> 
    tweets=list(file)
    #list_of_tweets=[]
    
    for i in range(len(tweets)):
        
        
        #Removing Tweets ID and Timestamps 
        tweets[i]=tweets[i][50:]
        
        
        #Removing URLs 
        #(http\w?.+)
        #(\w{4}\:\/\/\w{3}\.\w{2}.+)
        tweets[i]=re.sub(r'(http\w?.+)','', tweets[i])
        
        
        #Remove any word with symbol (@) 
        tweets[i]=re.sub(r'(@\w[A-z0-9]+)', '' ,tweets[i])
        
        
        #Removing Punctuations
        tweets[i]=re.sub(r'[^\w\s]','', tweets[i]) # [^\w\s] search individual for anything not \s (space) and not \w (alphanumeric)
        #tweets[i]=tweets[i].translate(str.maketrans('','',string.punctuation)) # (string.punctuation) containsAllSymbols --> [ !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ ]
        
        
        #convert all words to lowerCase
        tweets[i]=tweets[i].lower()
        
        #break when space exists and insert in new list
        #list_of_tweets.append(tweets[i].split())
        tweets[i]=tweets[i].split()
    
    #print(tweets[0])
    file.close()
    return tweets
  
def calculateDistance(tweet1, tweet2):
    intersection = set(tweet1).intersection(tweet2)
    union = set(tweet1).union(tweet2)
    return 1 - (len(intersection) / len(union))

def assign_cluster(tweets, centroids):
    clusters = dict()

    for t in range(len(tweets)):
        min_dis = math.inf
        cluster_idx = -1;
        for c in range(len(centroids)):
            dis = calculateDistance(centroids[c], tweets[t])
            if centroids[c] == tweets[t]:
                cluster_idx = c
                min_dis = 0

            if dis < min_dis:
                cluster_idx = c
                min_dis = dis

        if min_dis == 1:
            cluster_idx = rd.randint(0, len(centroids) - 1)

        clusters.setdefault(cluster_idx, []).append([tweets[t]])    
        last_tweet_idx = len(clusters.setdefault(cluster_idx, [])) - 1
        clusters.setdefault(cluster_idx, [])[last_tweet_idx].append(min_dis)
        
    return clusters

def update_centroids(clusters):

    centroids = []
    for c in range(len(clusters)):
        min_dis_sum = math.inf
        bestidx = -1
    
        
        for x in range(len(clusters[c])):
            tot = 0
            for y in range(len(clusters[c])):
                if x != y:
                    dis = calculateDistance(clusters[c][x][0], clusters[c][y][0])
                    tot += dis

            if tot < min_dis_sum:
                min_dis_sum = tot
                bestidx = x
                
        centroids.append(clusters[c][bestidx][0])
    
    return centroids

def compute_SSE(clusters):

    sse = 0
    for c in range(len(clusters)):
        for t in range(len(clusters[c])):
            sse = sse + (clusters[c][t][1] * clusters[c][t][1])

    return sse

def k_means(tweets, k=4, maxit=50):
    centroids = []
    size = 0
    used = dict()
    
    while (True):
        if size>=k:
            break
        else:
            idx = rd.randint(0, len(tweets) - 1)
            if idx not in used:
                size += 1
                used[idx] = True
                centroids.append(tweets[idx])
    
    
    prev = []
    for i in range(maxit):
        clusters = assign_cluster(tweets, centroids)
        prev = centroids
        centroids = update_centroids(clusters)
        
        go = False
        if len(prev) != len(centroids):
            go = True
        
        for c in range(len(centroids)):
            if " ".join(centroids[c]) != " ".join(prev[c]):
                go = True
        
        if go==False:
            break

    sse = compute_SSE(clusters)
    return clusters, sse


tweets = filteringDataset("bbchealth")
k = 3
for e in range(5):
    clusters, error = k_means(tweets, k)
    
    for c in range(len(clusters)):
       print(str(c+1) + ": ", str(len(clusters[c])) + " tweets")
       # # to print tweets in a cluster
       # for t in range(len(clusters[c])):
       #     print("t" + str(t) + ", " + (" ".join(clusters[c][t][0])))

    print("--> SSE : " + str(error))
    print('\n')
    k = k + 1

