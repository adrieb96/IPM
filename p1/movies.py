class MyMovies(object):

    def __init__(self):
        
        self.movies = []


    def getList(self):
        return self.movies
    
    def printList(self):
        for movie in self.movies:
            print movie.getTitle()

    def checkMovie(self,movie):
        for movies in self.movies:
            if movie.equals(movies):
                return False
        return True    

    def addMovie(self,movie):
        if self.checkMovie(movie):
            pos = 0
            end = len(self.movies)
            while pos < end and movie.getTitle().lower() > self.movies[pos].getTitle().lower():
                pos += 1
            self.movies.insert(pos,movie)
            return True
        else:
            return False
    
    def deleteMovie(self,movie):
        self.movies.remove(movie)
   
    def updateMovie(self,old,new):
        if old.getTitle().lower() == new.getTitle().lower():
            pos = self.movies.index(old)
            self.movies.remove(old)
            self.movies.insert(pos,new)
        else:
            self.movies.remove(old)
            self.addMovie(new)

    def getMovie(self,title):
        tmp = Movie(title)
        for movies in self.movies:
            if tmp.equals(movies):
                return movies

class Movie(object):

    def __init__(self,title):
        self.title = title

    def equals(self,movie):
        return self.title.lower() == movie.title.lower()
    
    def getTitle(self):
        return self.title

