from BeautifulSoup import BeautifulSoup
class LottoPageParser:
    def __init__(self):
        self.kierros=0
        self.numerot=[]
        self.lisanumerot=[]
        
    def feed(self,content):
        soup=BeautifulSoup(content)
        
