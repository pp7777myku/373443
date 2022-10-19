import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

movie_name = []  #name of movie
movie_url = []  #link
movie_star = []  #score
movie_star_people = []  #numbers of viewer
movie_director = []  # director
movie_actor = []  # main actor
movie_year = []  # year
movie_country = []  # contry
movie_type = []  # type

def get_info(url, headers):
	res = requests.get(url, headers=headers)
	soup = BeautifulSoup(res.text, 'html.parser')
	for movie in soup.select('.item'):
		name = movie.select('.hd a')[0].text.replace('\n', '')  # name of movie
		movie_name.append(name)
		url = movie.select('.hd a')[0]['href']  #link
		movie_url.append(url)
		star = movie.select('.rating_num')[0].text  #score
		movie_star.append(star)
		star_people = movie.select('.star span')[3].text  #numbers of viewer
		star_people = star_people.strip().replace('人评价', '')
		movie_star_people.append(star_people)
		movie_infos = movie.select('.bd p')[0].text.strip() 
		director = movie_infos.split('\n')[0].split('   ')[0]
		movie_director.append(director)
		try:  
			actor = movie_infos.split('\n')[0].split('   ')[1]
			movie_actor.append(actor)
		except:  
			movie_actor.append(None)
		if name == '大闹天宫 / 大闹天宫 上下集  /  The Monkey King': 
			year0 = movie_infos.split('\n')[1].split('/')[0].strip()
			year1 = movie_infos.split('\n')[1].split('/')[1].strip()
			year2 = movie_infos.split('\n')[1].split('/')[2].strip()
			year = year0 + '/' + year1 + '/' + year2
			movie_year.append(year)
			country = movie_infos.split('\n')[1].split('/')[3].strip()
			movie_country.append(country)
			type = movie_infos.split('\n')[1].split('/')[4].strip()
			movie_type.append(type)
		else: 
			year = movie_infos.split('\n')[1].split('/')[0].strip()
			movie_year.append(year)
			country = movie_infos.split('\n')[1].split('/')[1].strip()
			movie_country.append(country)
			type = movie_infos.split('\n')[1].split('/')[2].strip()
			movie_type.append(type)


def output(csv_name):

	df = pd.DataFrame()  # 初始化一个DataFrame对象
	df['Название фильма'] = movie_name
	df['Ссылка'] = movie_url
	df['Рейтинг'] = movie_star
	df['Количество человек'] = movie_star_people
	df['Директор'] = movie_director
	df['В главных ролях'] = movie_actor
	df['Год'] = movie_year
	df['Страна'] = movie_country
	df['Тип'] = movie_type
	df.to_csv(csv_name, encoding='utf_8_sig')  # save to csv


if __name__ == "__main__":
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
	# start crawling
	for i in range(10):  # total 10 pages, 25 movies per page
		page_url = 'https://movie.douban.com/top250?start={}'.format(str(i * 25))
		print('Crawling page {}.'.format(str(i + 1)))
		get_info(page_url, headers)
		sleep(2) 
	output(csv_name="Result.csv")
	print('END')
