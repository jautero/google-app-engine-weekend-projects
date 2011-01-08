#!/usr/bin/python
import festival,os,time

festivalfile=os.environ['HOME']+"/RA2003.xml"

def movie_cmp(self,other):
    return cmp(self.free_screenings,other.free_screenings)

def sort_by_date(scra,scrb):
    return cmp(scra.convert_time(),scrb.convert_time())

def sort_by_theatre(scra,scrb):
    return cmp(scra.theatre,scrb.theatre)

def create_candidates(festari):
    candidates=[]
    for movie in festari.movies:
        if movie.selected:
            candidates.append(movie)
        movie.free_screenings=0
        for screening in movie.screenings:
            if screening.soldout:
                screening.free=0
            else:
                movie.free_screenings+=1
                screening.free=1
    return candidates

festari=festival.read_festival(open(festivalfile,"r"))
aikataulu=festival.Timetable()
aikataulu.addFestival(festari)
aikataulu.calculate_overlaps()
candidates=create_candidates(festari)
selected_screenings=[]
best_candidate=[]

def find_candidates():
    global best_candidate
    candidates.sort(movie_cmp)
    if len(candidates)==0:
        return 1
    for index in range(0,len(candidates)):
        candidate=candidates.pop(index)
        if candidate.free_screenings==0:
            # Backtrack
            candidates.insert(index,candidate) 
            return 0
        for screening in candidate.screenings:
            if screening.free:
                updated=[]
                for scr in screening.overlaping:
                    if scr.free:
                        scr.free=0
                        scr.movie.free_screenings-=1
                        updated.append(scr)
                selected_screenings.append(screening)
                if len(selected_screenings)>len(best_candidate):
                    best_candidate=selected_screenings[:]
                if find_candidates():
                    return 1
                else:
                    selected_screenings.remove(screening)
                    for src in updated:
                        scr.free=1
                        scr.movie.free_screenings+=1
        candidates.insert(index,candidate)
    return 0

def printscreening(screening):
    print "\t%s: %s %s" % (screening.movie.name.encode("ISO-8859-1"),
                         time.strftime("%a %d.%m. %H:%M",
                                       time.localtime(screening.convert_time())),
                         screening.theatre.encode("ISO-8859-1"))

if find_candidates():
    print "Movie list:"
    selected_screenings.sort(sort_by_date)
    print "    by date:"
    map(printscreening,selected_screenings)
    print "    by theatre"
    selected_screenings.sort(sort_by_theatre)
    old_theatre=selected_screenings[0].theatre
    for screening in selected_screenings:
        if (screening.theatre!=old_theatre):
            print
            old_theatre=screening.theatre
        printscreening(screening)

else:
    print "Matching list couldn't be found."
    print "Best match:"
    for screening in selected_screenings:
        print "%s: %s %s" % (screening.movie.name.encode("ISO-8859-1"),
                             time.strftime("%a %d.%m. %H:%M",time.localtime(screening.convert_time())),
                             screening.theatre.encode("ISO-8859-1"))
    
