class MyMovies(object):

    def __init__(self):
        
        self.movies = []


    def getList(self,mode):

        listedMovies = []

        if mode == 1:
            listedMovies = self.movies
        elif mode == 2:
            for movie in self.movies:
                if movie.getStatus():
                    listedMovies.add(movie)
        else:
            for movie in self.movies:
                if movie.getStatus() == False:
                    listedMovies.add(movie)    

        return listedMovies
    
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
   
    def change(self,old,new):
        pos = self.movies.index(old)
        self.movies[pos]=new

    def updateMovie(self,old,new):
        new.setStatus(old.getStatus())
        if old.getTitle().lower() == new.getTitle().lower():
            self.change(old,new)
            return True
        elif self.addMovie(new):
            self.movies.remove(old)
            return True
        else:
            return False
    
    def seenMovie(self,movie):
        movie.changeStatus()
        self.change(movie,movie)

    def getMovie(self,title):
        tmp = Movie(title)
        for movies in self.movies:
            if tmp.equals(movies):
                return movies
        return None

class Movie(object):

    def __init__(self,title):
        self.title = title
        self.status = False

    def equals(self,movie):
        return self.title.lower() == movie.title.lower()
    
    def getTitle(self):
        return self.title

    def setStatus(self,status):
        self.status = status

    def changeStatus(self):
        self.status = not self.status

    def getStatus(self):
        return self.status


