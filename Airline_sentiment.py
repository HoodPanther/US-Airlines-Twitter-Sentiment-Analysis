import sklearn
import matplotlib.pyplot as plt
%matplotlib inline
import pandas as pd
from sklearn.cross_validation import train_test_split
import numpy as np
import seaborn as sns
import re
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud,STOPWORDS


tweet= pd.read_csv("../input/Tweets.csv")
tweet.head()


tweet.shape


#counting the number of tweets each airlines has received
tweet.airline.value_counts()


#Plotting the number of tweets each airlines has received
colors=sns.color_palette("husl", 10)
pd.Series(tweet["airline"]).value_counts().plot(kind = "bar",
color=colors,figsize=(8,6),fontsize=10,rot = 0, title = "Total No. of Tweets for each Airlines")
plt.xlabel('Airlines', fontsize=10)
plt.ylabel('No. of Tweets', fontsize=10)


#counting the number of each type of sentiments
tweet.airline_sentiment.value_counts()


#Plotting the number of each type of sentiments
colors=sns.color_palette("husl", 10)
pd.Series(tweet["airline_sentiment"]).value_counts().plot(kind = "bar",
color=colors,figsize=(8,6),rot=0, title = "Total No. of Tweets for Each Sentiment")
plt.xlabel('Sentiments', fontsize=10)
plt.ylabel('No. of Tweets', fontsize=10)


colors=sns.color_palette("husl", 10)
pd.Series(tweet["airline_sentiment"]).value_counts().plot(kind="pie",colors=colors,
labels=["negative", "neutral", "positive"],explode=[0.05,0.02,0.04],
shadow=True,autopct='%.2f', fontsize=12,figsize=(6, 6),title = "Total Tweets for Each Sentiment")


def plot_sub_sentiment(Airline):
pdf = tweet[tweet['airline']==Airline]
count = pdf['airline_sentiment'].value_counts()
Index = [1,2,3]
color=sns.color_palette("husl", 10)
plt.bar(Index,count,width=0.5,color=color)
plt.xticks(Index,['Negative','Neutral','Positive'])
plt.title('Sentiment Summary of' + " " + Airline)
airline_name = tweet['airline'].unique()
plt.figure(1,figsize=(12,12))
for i in range(6):
plt.subplot(3,2,i+1)
plot_sub_sentiment(airline_name[i])


#counting the total number of negative reasons
tweet.negativereason.value_counts()


#Plotting all the negative reasons
color=sns.color_palette("husl", 10)
pd.Series(tweet["negativereason"]).value_counts().plot(kind = "bar",
color=color,figsize=(8,6),title = "Total Negative Reasons")
plt.xlabel('Negative Reasons', fontsize=10)
plt.ylabel('No. of Tweets', fontsize=10)


tweet.negativereason.value_counts().head(5)


color=sns.color_palette("husl", 10)
pd.Series(tweet["negativereason"]).value_counts().head(5).plot(kind="pie",
labels=["Customer Service Issue", "Late Flight", "Can't Tell","Cancelled Flight","Lost Luggage"],
colors=color,autopct='%.2f',explode=[0.05,0,0.02,0.03,0.04],shadow=True,
fontsize=12,figsize=(6, 6),title="Top 5 Negative Reasons")


air_senti=pd.crosstab(tweet.airline, tweet.airline_sentiment)
air_senti


percent=air_senti.apply(lambda a: a / a.sum() * 100, axis=1)
percent


pd.crosstab(index = tweet["airline"],columns = tweet["airline_sentiment"]).plot(kind='bar',
figsize=(10, 6),alpha=0.5,rot=0,stacked=True,title="Airline Sentiment")


percent.plot(kind='bar',figsize=(10, 6),alpha=0.5,
rot=0,stacked=True,title="Airline Sentiment Percentage")


tweet['tweet_created'] = pd.to_datetime(tweet['tweet_created'])
tweet["date_created"] = tweet["tweet_created"].dt.date


tweet["date_created"]


df = tweet.groupby(['date_created','airline'])
df = df.airline_sentiment.value_counts()
df.unstack()


#visualization using wordcloud for the negative tweets
df=tweet[tweet['airline_sentiment']=='negative']
words = ' '.join(df['text'])
cleaned_word = " ".join([word for word in words.split()
if 'http' not in word
and not word.startswith('@')
and word != 'RT'])
wordcloud = WordCloud(stopwords=STOPWORDS,
background_color='black',
width=3000,
height=2500
).generate(cleaned_word)
plt.figure(1,figsize=(12, 12))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()


#visualization using wordcloud for the positive tweets
df=tweet[tweet['airline_sentiment']=='positive']
words = ' '.join(df['text'])
cleaned_word = " ".join([word for word in words.split()
if 'http' not in word
and not word.startswith('@')
and word != 'RT'])
wordcloud = WordCloud(stopwords=STOPWORDS,
background_color='black',
width=3000,
height=2500
).generate(cleaned_word)
plt.figure(1,figsize=(12, 12))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()


#visualization using wordcloud for the neutral tweets
df=tweet[tweet['airline_sentiment']=='neutral']
words = ' '.join(df['text'])
cleaned_word = " ".join([word for word in words.split()
if 'http' not in word
and not word.startswith('@')
and word != 'RT'])
wordcloud = WordCloud(stopwords=STOPWORDS,
background_color='black',
width=3000,
height=2500
).generate(cleaned_word)
plt.figure(1,figsize=(12, 12))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()


def tweet_to_words(raw_tweet):
letters_only = re.sub("[^a-zA-Z]", " ",raw_tweet)
words = letters_only.lower().split()
stops = set(stopwords.words("english"))
meaningful_words = [w for w in words if not w in stops]
return( " ".join( meaningful_words ))
def clean_tweet_length(raw_tweet):
letters_only = re.sub("[^a-zA-Z]", " ",raw_tweet)
words = letters_only.lower().split()
stops = set(stopwords.words("english"))
meaningful_words = [w for w in words if not w in stops]
return(len(meaningful_words))
tweet['sentiment']=tweet['airline_sentiment'].apply(lambda x: 0 if x=='negative' else 1)
tweet.sentiment.head()


#Splitting the data into train and test
tweet['clean_tweet']=tweet['text'].apply(lambda x: tweet_to_words(x))
tweet['Tweet_length']=tweet['text'].apply(lambda x: clean_tweet_length(x))
train,test = train_test_split(tweet,test_size=0.2,random_state=42)
train_clean_tweet=[]
for tweets in train['clean_tweet']:
train_clean_tweet.append(tweets)
test_clean_tweet=[]
for tweets in test['clean_tweet']:
test_clean_tweet.append(tweets)
from sklearn.feature_extraction.text import CountVectorizer
v = CountVectorizer(analyzer = "word")
train_features= v.fit_transform(train_clean_tweet)
test_features=v.transform(test_clean_tweet)
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import accuracy_score
Classifiers = [
LogisticRegression(C=0.000000001,solver='liblinear',max_iter=200),
KNeighborsClassifier(3),
SVC(kernel="rbf", C=0.025, probability=True),
DecisionTreeClassifier(),
RandomForestClassifier(n_estimators=200),
AdaBoostClassifier(),
GaussianNB()]
dense_features=train_features.toarray()
dense_test= test_features.toarray()
Accuracy=[]
Model=[]
for classifier in Classifiers:
try:
fit = classifier.fit(train_features,train['sentiment'])
pred = fit.predict(test_features)
except Exception:
fit = classifier.fit(dense_features,train['sentiment'])
pred = fit.predict(dense_test)
accuracy = accuracy_score(pred,test['sentiment'])
Accuracy.append(accuracy)
Model.append(classifier.__class__.__name__)
print('Accuracy of '+classifier.__class__.__name__+' is '+str(accuracy))


Index = [1,2,3,4,5,6,7]
plt.bar(Index,Accuracy)
plt.xticks(Index, Model, rotation=45)
plt.ylabel('Accuracy')
plt.xlabel('Model')
plt.title('Accuracies of Models')



