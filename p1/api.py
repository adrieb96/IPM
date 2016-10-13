import requests
import json

key = "ec388678283f75639302a76fd4944cb4"

class TMDB(object):
    
    def __init__(self,lang):

        self.db = "https://api.themoviedb.org/3/movie/"
        self.search = "https://api.themoviedb.org/3/search/movie/"
        self.lang = lang

    def try_connection(self):
        try:
            self.get_response(self.db+"?api_key="+key)
            return True
        except:
            return False

    def get_response(self,url):
        response = requests.get(url)
        return json.loads(response.text)


    def get_movie_id(self,title):

        url = "%s?api_key=%s&language=%s&query=%s" %(self.search,key,self.lang,title)
        response = self.get_response(url)

        films = response['results']
        for item in films:
            return item['id']
        return None

    def get_title(self,movie_id):

        url = "%s%d?api_key=%s&language=%s" %(self.db,movie_id,key,self.lang)
        txt = self.get_response(url)
        return txt['title']
    

    def get_recommendations(self,movie_list):
    
        def get_recommendation(movie_id,n):
    
            url = "%s%d/recommendations?api_key=%s&language=%s" %(self.db,movie_id,key,self.lang)
            txt = self.get_response(url)
            films =  txt['results']
        
            for item in films:
                 if n<1:
                     return item['title']
                 n-=1
            return None
        #----------------------------------------

        def get_iterations(i):
            if i<4:
                return (3,False)
            if i<6:
                return (2,False)
            else:
                return (1,i>10)
        #--------------------------------------    

        recommendations = []
        
        (i,repeat) = get_iterations(len(movie_list))

        for item in movie_list:
            j = 0
            while j<i:
                movie = get_recommendation(item,j)
                if movie is None:
                    break
                elif movie in recommendations:
                    if repeat:
                        break
                else:
                    recommendations.append(movie)
                    j+=1

        return recommendations      
