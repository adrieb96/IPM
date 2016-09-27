class MyMovies(object):

    def __init__(self):
        
        self.movies = []


    def getList(self):
        return self.movies

    def addMovie(self,movie):
        self.movies.append(movie)

    def deleteMovie(self,movie):
        self.movies.remove(movie)
   
    def updateMovie(self,old,new):
        self.deleteMovie(old)
        self.addMovie(new)

class Movie(object):

    def __init__(self,title,time,year):
        self.title = title
        self.time = time
        self.year = year
    
    def getData(self):
        return (self.title,self.time,self.year)

pelicula = Movie("LotR",200,2000)
peliculas =  MyMovies()
peliculas.addMovie(pelicula)
for movie in peliculas.getList():
    print movie.getData()
