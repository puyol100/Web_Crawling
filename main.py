import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
from datetime import datetime
import get_text
import ordering
import viewer
TARGET_URL_BEFORE_SEARCH= ''
TARGE_URL_BEFORE_KEWORD = ''
TARGE_URL_REST = ''
url_array = []

def get_info(URL,output_file,user_input_site, url_num, sort_type):
   count = 0
   global url_array
   if user_input_site == '동아일보':
      if sort_type == '최신순':
         sort_pos = URL.index('sorting')
         sort_URL = URL[:sort_pos+8] + '1' + URL[sort_pos+9:]
      else:
         sort_URL = URL

      page_num = url_num // 15
      for i in range(page_num+1):
         current_page_num = 1 + i*15;
         position = sort_URL.index('=')
         URL_with_page_num = sort_URL[:position+1] + str(current_page_num) + sort_URL[position+1:]
         source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
         soup = BeautifulSoup(source_code_from_URL,'lxml',from_encoding = 'utf-8')
         
         for title in soup.findAll('p',{'class':'tit'}):
            if count == url_num:
               return 
            count = count + 1
            make_count_str = str(count)+'. '
            title_link = title.select('a')
            article_URL = title_link[0]['href']
            article_title = title_link[0].text
            output_file.write(make_count_str)
            output_file.write(article_title)
            output_file.write('\n')
            output_file.write(article_URL)
            output_file.write('\n')
            url_array.append(article_URL)

   elif user_input_site == '중앙일보':
      if sort_type == '정확도순':
         sort_pos = URL.index('SortType')
         sort_URL = URL[:sort_pos+9] + 'Accuracy' + URL[sort_pos+12:]
      else:
         sort_URL = URL

      page_num = url_num // 10
      for i in range(page_num+1):
         current_page_num = 1 + i*10;
         position = sort_URL.index('=')
         URL_with_page_num = sort_URL[:position+1] + str(current_page_num) + sort_URL[position+1:]
         source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
         soup = BeautifulSoup(source_code_from_URL,'lxml',from_encoding = 'utf-8')

         for title in soup.find_all('h2','headline mg'):
            if count == url_num:
               return
            count = count + 1
            make_count_str = str(count)+'. '
            title_link = title.select('a')
            article_URL = title_link[0]['href']
            article_title = title_link[0].text
            output_file.write(make_count_str)
            output_file.write(article_title)
            output_file.write('\n')
            output_file.write(article_URL)
            output_file.write('\n')
            url_array.append(article_URL)

   elif user_input_site == '한겨레':
      page_num = url_num // 10

      now = datetime.now()
      date_pos = URL.index('dateto')
      date = str(now.year) + '.' + str(now.month) + '.' + str(now.day)
      date_URL = URL[:date_pos+7] + date + URL[date_pos+7+len(date):]

      if sort_type == '정확도순':
         sort_pos = date_URL.index('sort')
         sort_URL = date_URL[:sort_pos+5] + 's' + date_URL[sort_pos+6:]
      else:
         sort_URL = date_URL

      for i in range(page_num+1):
         current_page_num = i*10;
         URL_with_page_num = sort_URL + str(current_page_num)
         source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
         soup = BeautifulSoup(source_code_from_URL,'lxml',from_encoding = 'utf-8')

         for title in soup.find_all('dt'):#'dd',"photo"):
            title_link = title.select('a')
            if title_link == []:
               continue;
            if count == url_num:
               return 
            count = count + 1
            make_count_str = str(count)+'. '
            article_URL = title_link[0]['href']
            article_title = title_link[0].text
            output_file.write(make_count_str)
            output_file.write(article_title)
            output_file.write('\n')
            output_file.write(article_URL)
            output_file.write('\n')
            url_array.append(article_URL)

def main():
   print("본 프로그램은 검색어 관련 기사 신문사 URL을 최신순으로 뽑아주는 프로그램입니다.")
   print("신문사는 중앙일보, 한겨레, 동아일보 가 있습니다")
   print("신문사와 검색어를 입력해 주세요")
   while True:
      user_input_site = input("원하는 신문사를 입력하세요: ")
      user_keyword_input = input("검색어를 입력해 주세요: ")
      url_num = int(input('받아올 url 수: '))
      sort_type = (input('최신순? 정확도순?: '))
      if user_input_site == '동아일보':
         output_file_name = 'DongA.txt'
         #http://www.donga.com/news/search?check_news=1&more=1&sorting=1&range=3&search_date=&query=%EC%82%AC%EB%93%9C
         TARGET_URL_BEFORE_SEARCH = "http://news.donga.com/search?p="
         TARGE_URL_BEFORE_KEWORD ='&query='
         TARGE_URL_REST = "&check_news=1&more=1&sorting=3&search_dae=1&v1=&v2=&range=1"
         break
      elif user_input_site == '중앙일보':
         output_file_name = 'JoongAng.txt'
         #https://news.joins.com/Search/TotalNews?page=1&Keyword=%EC%82%AC%EB%93%9C&SortType=New&SourceGroupType=Joongang&SearchCategoryType=TotalNews
         TARGET_URL_BEFORE_SEARCH = "https://news.joins.com/Search/TotalNews?page="
         TARGE_URL_BEFORE_KEWORD = '&Keyword='
         TARGE_URL_REST = "&SortType=New&SourceGroupType=Joongang&SearchCategoryType=TotalNews"
         break
      elif user_input_site == '한겨레':
         output_file_name = 'Hangyeore.txt'
         #http://search.hani.co.kr/Search?command=query&keyword=%EC%82%AC%EB%93%9C&media=news&submedia=&sort=d&period=all&datefrom=2000.01.01&dateto=2019.11.03&pageseq=0
         TARGET_URL_BEFORE_SEARCH = "http://search.hani.co.kr/Search"
         TARGE_URL_BEFORE_KEWORD = '?command=query&keyword='
         TARGE_URL_REST = "&media=news&submedia=&sort=d&period=all&datefrom=2000.01.01&dateto=2019.11.03&pageseq="
         break
      else:
         print("서비스하지 않는 신문사 입니다.")
         print("재입력 부탁드립니다")
		 
   target_URL = TARGET_URL_BEFORE_SEARCH + TARGE_URL_BEFORE_KEWORD \
               + quote(user_keyword_input) + TARGE_URL_REST
   output_file = open(output_file_name,'w')

   get_info(target_URL,output_file,user_input_site, url_num, sort_type)
   output_file.close()
   print('신문사에 대한 ',url_num,'개의 ',sort_type,' 기사를 출력했습니다.')
   tt = input('해당 기사에서 많이 사용된 단어를 보여드릴까요?(입력 Y or N) ')
   if tt == 'Y':
    a = int(input("원하시는 url의 번호를 입력해주세요 (1~):"))
    result_text=get_text.get_text(url_array[a-1],user_input_site)
    tags = ordering.get_tags(result_text)
    viewer.show_data(tags)

   print('종료합니다')
  
main()