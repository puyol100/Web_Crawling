# 형태소 분석기
import sys
from konlpy.tag import Twitter
from collections import Counter
 
 
def get_tags(text, ntags=50):
	spliter = Twitter()
	nouns = spliter.nouns(text)
	count = Counter(nouns)
	return_list = []
	for n, c in count.most_common(ntags):
		temp = {'tag': n, 'count': c}
		return_list.append(temp)
	return return_list