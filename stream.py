import settings
import sys
import MeCab
import tweepy
from collections import Counter
import re
from numpy.random import *

"""
引数をクエリとして，ツイッターの現在のタイムラインからクエリを含むツイートを100こ検索
そのツイートを形態素解析して，含まれる単語の上位5個からランダムに返す
"""


# 環境変数から認証情報を取得する。
CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET = settings.CONSUMER_SECRET
ACCESS_TOKEN = settings.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET

# 認証情報を設定する。
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#検索ワードはコマンドラインから
search_word = sys.argv

#APIインスタンスを作成
api = tweepy.API(auth)
#ツイートをresultに格納
result = api.search(search_word[1] ,count=100)

# print(create_node("今日はいい天気ですね"))
nouns_list = []
word_class = ["名詞","形容詞","動詞"]

#動作部分
for i in result:
    text = i.text
    tagger = MeCab.Tagger("-Ochasen")
    tagger.parse('') #謎の行動
    node = tagger.parseToNode(text)

    while node:
        #名詞のみをリストに追加
        if node.feature.split(",")[0] == word_class[1]:
            nouns_list.append(node.surface)
        node = node.next

correct_list = []

#出てきた単語数をそれぞれ表示
counter = Counter(nouns_list)
for word, cnt in counter.most_common(50):
    if re.findall(r'([a-zA-Z1-9@+/+:+_+-+.+ー+(+)+#+]+)', word) == []:
        correct_list.append(word)
        #print(word,cnt)

n = randint(5)

print("応答：",correct_list[n],"ですね")
#print(correct_list)
