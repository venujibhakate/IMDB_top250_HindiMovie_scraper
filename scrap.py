from bs4 import BeautifulSoup
import requests
import pprint
import json
# import os
import pathlib
import random
import time

url = "https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
def scrap_top_list():
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    movies_list = []
    main_div = soup.find('div',class_='lister')
    tbody = main_div.find('tbody',class_='lister-list')
    trs = tbody.findAll('tr')
    
    i = 0
    for tr in trs:
        position = i = i + 1
        
        name = tr.find('td',class_='titleColumn').a.get_text()
        year = tr.find ('td',class_='titleColumn').span.get_text()
        rating = tr.find ('td',class_='ratingColumn').get_text()
        link = tr.find('td',class_='titleColumn').a['href']
        
        new = {}
        
        movie_link = "https://www.imdb.com"+link
        new['psition']= position
        new['movie_name']= str(name)
        new['year']= int(year[1:5])
        new['rating'] = float(rating)
        new['link'] = movie_link
    
        movies_list.append(new)
    return movies_list
top_movies = scrap_top_list()
# pprint.pprint(top_movies)
# yaha par maine first function ko call kar rakha hai.


# Task2*********************************************************************
def group_by_year():
    for i in top_movies:
        dic = {}
        year = i['year']
        if (not i.get(year)):
            dic[year] = []
            dic[year].append(i)
        # pprint.pprint (dic)
        return dic
listof_years = group_by_year()
# pprint.pprint(listof_years)

# Task3***********************************************************************
def group_by_decade():
    moviedec = {}
    empty = []
    for j in top_movies:
        mod = j['year']%10
        decade = j['year']-mod
        if decade not in moviedec:
            moviedec[decade] = []
        moviedec[decade].append(j)

    return(moviedec)
listof_decade = group_by_decade()
# pprint.pprint(listof_decade)
# yaha par maine second task call karwaya hai. 
 

# Task12*********************************************************************
def scrape_movie_casts(url):
    listof_cast = []
    json_dic1 = url
    # print json_dic1
    url_id1 = json_dic1.split("/")
    url_id1 = url_id1[-2]
    # print url_id1    
    file_name_2 = "cast_data/"+ url_id1 +".json"
    filepath1 = pathlib.Path(file_name_2)
    if filepath1.exists():
        # print "nahi"
        with open(file_name_2,'r') as json_data:
            data2 = json_data.read()
            data3 = json.loads(data2)
        return data3
    else:  
                
        res2 = requests.get(json_dic1)
        soup2 = BeautifulSoup(res2.text,"html.parser")
        table_data = soup2.find("table",class_ = "cast_list")
        actors = table_data.find_all("td",class_ = "")
        
        for i in actors:
            actor_dic = {}
            imdb_id = i.find("a").get("href")[6:15]
            name = i.get_text().strip()
            actor_dic["imdb_id"] = str(imdb_id)
            actor_dic["name"] = str(name)
            listof_cast.append(actor_dic)
        with open(file_name_2,"w") as data2:
            data2.write(json.dumps(listof_cast))
        # return listof_cast   
    




# Task4**********************************************************************
# Task8***********************************************************************
# Task9*************************************************************************
# Task13***************************************************************************
def scrape_movie_details(url):
    url_id = url.split('/')
    url_id = url_id[-2]
    movie_name = ''
    file_name = "moviefile/"+url_id+".json"
    filepath = pathlib.Path(file_name)
    if filepath.exists():
        with open(file_name,'r') as json_data:
            data = json_data.read()
            data2 = json.loads(data)
        return data2        
    else:
        second_new = {}
        page = requests.get(url)
        soup = soup = BeautifulSoup(page.text,"html.parser")
        title_div = soup.find('div',class_='title_wrapper').h1.get_text()
        movie_name = title_div.split()
        # print movie_name
        movie_name.pop()
        movie_name = ' '.join(movie_name)

        # sub_div = soup.find('div',class_="subtext")
        
        gener = soup.find('div',class_='subtext').a.get_text()
        # print gener
        # a_tag = gener.findAll("a")
        # all_gener_list = []
        # for g in a_tag:
        #     all_gener_list.append(a_tag[g].get_text())
        # print all_gener_list
        
        movie_Directors = soup.find('div',class_="credit_summary_item")
        director_list = movie_Directors.findAll("a")
        director_name = []
        for i in director_list:
            director_name.append(i.get_text())
            # print director_name
        
        poster_img = soup.find('div',class_='poster').a['href']
        bio = soup.find('div',class_='summary_text').get_text()
        extra_details = soup.find('div',attrs={"class":'article',"id":'titleDetails'})
        list_divs = extra_details.find_all('div')
        for div in list_divs:
            tag_h4 = div.find_all('h4')
            for text in tag_h4:
                if 'Country:' in text :
                    movie_country = div.find('a').get_text()
                elif 'Language:'in text:
                    movie_language  = div.find_all('a')
                    movie_language_list = [language.get_text() for language in movie_language] 
                elif 'Runtime:'in text:
                    movie_runtime  = div.find('time').get_text()
                    second_new['runtime']= movie_runtime
        second_new['name']= movie_name
        second_new['gener']= [gener]
        second_new['director']=  director_name
        second_new['poster_img'] = poster_img
        second_new['bio'] = bio
        second_new['Country']= movie_country
        second_new['Language']= movie_language_list
        movie_casts = scrape_movie_casts(url)
        second_new['cast']= movie_casts
        with open(file_name,"w") as data:
            data.write(json.dumps(second_new))
        # return second_new
# listof_movie_details = scrape_movie_details()
# pprint.pprint(listof_movie_details)



# # Task5*********************************************************************** 
def  getall_movie_list_details(moviesall_list):
    random_sleep = random.randint(1,3)
    print (random_sleep)
    clock = time.sleep(random_sleep)
    # print (clock)
    
    
    all_movie_list = []
    for i in moviesall_list [:250]:
        dic = i["link"]
        scrape_movie_details10 = scrape_movie_details(dic)
        all_movie_list.append(scrape_movie_details10)
    return all_movie_list
all_movie_details = getall_movie_list_details(top_movies)
pprint.pprint(all_movie_details)

# Task6************************************************************************
def analyse_movies_language(movie_details):
    movie_details_list = {}
    for language in movie_details:
        if language not in movie_details_list:
            movie_details_list[language] = 1
        else:
            movie_details_list[language] += 1
    return movie_details_list  

language_list = []
for i in all_movie_details:
    mod = i['Language']
    language_list.extend(mod)
# print empty
# print analyse_movies_language(language_list)

# # Task7************************************************************************
def analyse_movies_directors(movie_details):
    director_details_list = {}
    for Director in movie_details:
        if Director not in director_details_list:            
            director_details_list[Director] = 1
        else:
            director_details_list[Director] += 1
    return director_details_list
director_list = []
for j in all_movie_details:
    movie_director_list = j["director"]
    director_list.extend(movie_director_list)
# # print director_list
#pprint.pprint (analyse_movies_directors(director_list))

# Task10**************************************************************
def analyse_language_and_directors(moviesall_list):
    dic_director = {}
    for movie in moviesall_list:
        for director in movie["director"]:
            dic_director[director] = {}
        # print dic_director
    for i in  moviesall_list:
        for director in i["director"]:
            for language in i["Language"]:
                # print(language)
                if director in dic_director:
                    dic_director[director][language] = 0
    for i in moviesall_list:
        for director in i["director"]:
            for language in i["Language"]:
                if director in dic_director:
                    dic_director[director][language] += 1
            
    return dic_director
director_and_language = analyse_language_and_directors(all_movie_details )
# pprint.pprint(director_and_language)

#Task11****************************************************************** 
def analyse_movies_gener(moviesall_list):
    dicof_gener = {}
    for g in moviesall_list :
        if g  not in dicof_gener:
            dicof_gener[g] = 1
        else:
            dicof_gener[g] += 1
    return dicof_gener

gener_list = []
# count = 0
for i in all_movie_details:
    Find_gener = i['gener']
    # if  "Drama" in Find_gener:
    #     count +=1
    gener_list.extend(Find_gener)
# print count
# pprint.pprint(analyse_movies_gener(gener_list))


# Task14*******************************************************************************

# def analyse_co_actors(moviesall_list):
#     coactors_dic = {}
#     coactors_list = []
#     for i in range(10):
#         for j in moviesall_list:
#             print j
# analyse_co_actors(all_movie_details)

# Task15************************************************************************************
def analyse_actors(moviesall_list):
    total_movie_actors_list = {}
    for i in moviesall_list:
        key = i["cast"]
        # print key
        for i in key:
            # print i
            actors_imdb_id = i["imdb_id"]
            # print actors_imdb_id
            actors_imdb_name = i["name"]
            # print actors_imdb_name
            # total_movie_actors_list =(actors_imdb_id,actors_imdb_name)
            # print total_movie_actors_list
            if actors_imdb_id in total_movie_actors_list:
                dic["num_movie"] += 1
            else:
                total_movie_actors_list[actors_imdb_id] = {}
                dic = total_movie_actors_list[actors_imdb_id]
                dic["name"]= actors_imdb_name
                dic["num_movie"] = 1
    return total_movie_actors_list
pprint.pprint(analyse_actors(all_movie_details))


