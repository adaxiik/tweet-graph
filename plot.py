#!/usr/bin/env python3
from dateutil import parser
import json,datetime,time
import matplotlib.pyplot as plt
from numpy import sort



with open('tweet.js', 'r') as f:
    file = f.read()
tweets_raw = json.loads(file)

tweets = []

for tweet in tweets_raw:
    tweets.append(tweet['tweet']) 


def showTweetsPerDay():
    day_tweet_count = {}

    for tweet in tweets:
        day = tweet['created_at'].split(' ')[0]
        if day not in day_tweet_count:
            day_tweet_count[day] = 1
        else:
            day_tweet_count[day] += 1
    labels = 'Mon - {0}'.format(day_tweet_count['Mon']), 'Tue - {0}'.format(day_tweet_count['Tue']), 'Wed - {0}'.format(day_tweet_count['Wed']), 'Thu - {0}'.format(day_tweet_count['Thu']), 'Fri - {0}'.format(day_tweet_count['Fri']), 'Sat - {0}'.format(day_tweet_count['Sat']), 'Sun - {0}'.format(day_tweet_count['Sun'])
    sizes = [day_tweet_count['Mon'], day_tweet_count['Tue'], day_tweet_count['Wed'], day_tweet_count['Thu'], day_tweet_count['Fri'], day_tweet_count['Sat'], day_tweet_count['Sun']]
    explode = (0, 0, 0, 0, 0, 0, 0) 

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title('Tweets Per Day')
    plt.show()

def showTweetsPerHour():
    hour_tweet_count = {}
    for tweet in tweets:
        hour = tweet['created_at'].split(' ')[3].split(':')[0]
        if hour not in hour_tweet_count:
            hour_tweet_count[hour] = 1
        else:
            hour_tweet_count[hour] += 1
    plt.bar(range(len(hour_tweet_count)), hour_tweet_count.values(), align='center')
    plt.xticks(range(len(hour_tweet_count)), sorted(hour_tweet_count.keys()))
    plt.xlabel('Hour')
    plt.ylabel('Tweet Count')
    plt.title('Tweets Per Hour')
    plt.show()
        
def showTweetsPerMonth():
    month_tweet_count = {}
    for tweet in tweets:
        month = tweet['created_at'].split(' ')[1]
        if month not in month_tweet_count:
            month_tweet_count[month] = 1
        else:
            month_tweet_count[month] += 1
    plt.bar(range(len(month_tweet_count)), month_tweet_count.values(), align='center')
    plt.xticks(range(len(month_tweet_count)), month_tweet_count.keys())
    plt.xlabel('Month')
    plt.ylabel('Tweet Count')
    plt.title('Tweets Per Month')
    plt.show()

def showTopTenWords(min_length=3):
    words = []
    for tweet in tweets:
        words += tweet['full_text'].split()

    word_count = {}
    for word in words:
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    
    top_ten = []
    for word in sorted_word_count:
        if len(word[0]) > min_length:
            top_ten.append(word)
        if len(top_ten) == 10:
            break

    top_ten = top_ten[:10]
    plt.bar(range(len(top_ten)), [x[1] for x in top_ten], align='center')
    plt.xticks(range(len(top_ten)), [x[0] for x in top_ten])
    plt.xlabel('Word')
    plt.ylabel('Count')
    plt.title('Top Ten Words')
    plt.show()

def averageTweetsPerDay():
    tweet_count = {}
    for tweet in tweets:
        tweet_time = createdAtSTRtoUnix(tweet['created_at'])
        if tweet_time not in tweet_count:
            tweet_count[tweet_time] = 1
        else:
            tweet_count[tweet_time] += 1

    sorted_tweet_count = sorted(tweet_count.items(), key=lambda x: x[0])
    tweet_count_str = {}
    for tweet in sorted_tweet_count:
        tweet_time_str = unixToSTR(tweet[0])
        if tweet_time_str not in tweet_count_str:
            tweet_count_str[tweet_time_str] = tweet[1]
        else:
            tweet_count_str[tweet_time_str] += tweet[1]


    plt.bar(range(len(tweet_count_str)), tweet_count_str.values(), align='center')
    plt.xticks(range(len(tweet_count_str)), tweet_count_str.keys(), rotation=90,size='x-small')

    plt.xlabel('Time')
    plt.ylabel('Tweet Count')

    plt.show()

def tweetCountPlot(titleForEveryXcount=50):
    tweet_count = []
    for tweet in tweets:
        tweet_count.append(createdAtSTRtoUnix(tweet['created_at']))
    
    tweet_count.sort()
    
    plt.plot(tweet_count, [x for x in range(len(tweet_count))])

    not_every = tweet_count[::titleForEveryXcount]
    plt.xticks(not_every, [unixToSTR(x) for x in not_every], rotation=90)

    plt.xlabel('Time')
    plt.ylabel('Tweet Count')
    plt.title('Tweet Count over Time')
    plt.show()

def createdAtSTRtoUnix(created_at_str):
    parser.parse(created_at_str)
    return int(parser.parse(created_at_str).timestamp())

def unixToSTR(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime('%d.%m.%Y')

def main():
    showTweetsPerDay()
    showTweetsPerHour()
    showTweetsPerMonth()
    showTopTenWords(3)
    averageTweetsPerDay()
    tweetCountPlot(50)

if __name__ == '__main__':
    main()
    