import requests
import json

key = "ec388678283f75639302a76fd4944cb4"

#Connects to the db and returns the answer
def get_response(url):
    response = requests.get(url,timeout=7)
    return json.loads(response.text)

class TMDB(object):
    
    def __init__(self,lang):

        self.db = "https://api.themoviedb.org/3/movie/"
        self.search = "https://api.themoviedb.org/3/search/movie/"
        self.lang = lang

    #Tries to connect to the DB
    def try_connection(self):
        try:
            get_response(self.db+"?api_key="+key)
            return True
        except:
            return False

        
    #Returns a list with all the movies with a similar title
    def get_similar_title(self,title):

        url = "%s?api_key=%s&language=%s&query=%s" %(self.search,key,self.lang,title)
        response = get_response(url)
        
        films = response['results']
        titles = []
        for item in films:
            if item['vote_average'] > 4:
                titles.append((item['title'],item['release_date'][0:4],item['vote_average']))
        return titles   


    #Returns the id of the given movie
    def get_movie_id(self,title):

        url = "%s?api_key=%s&language=%s&query=%s" %(self.search,key,self.lang,title)
        response = get_response(url)
        
        films = response['results']
        for item in films:
            return item['id']
        return None


    #Returns the title of the movie which has the given id
    def get_title(self,movie_id):

        url = "%s%d?api_key=%s&language=%s" %(self.db,movie_id,key,self.lang)
        response = get_response(url)
        return response['title']
    

    """
    #Returns a list of recommendations based on the given movie list
    def get_recommendations(self,movie_list):
    """ 

    def get_recommendation(self, movie_id,n):
    
        url = "%s%d/recommendations?api_key=%s&language=%s" %(self.db,movie_id,key,self.lang)
        response = get_response(url)

        films =  response['results']
    
        recs = []

        for item in films:
            if n<1:
                break
            recs.append(item['title'])
            n -= 1
        return recs
        """ #----------------------------------------

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
            recs = get_recommendation(item,i)

            if len(recs)<1:
                continue
            for movie in recs:
                if movie in recommendations:
                    if repeat:
                        break
                else:
                    recommendations.append(movie)

        return recommendations      
        """

