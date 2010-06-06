import unittest

class LottoTarkistaja:
    def __init__(self,voittorivi,voittoluokat):
        self.voittorivi=voittorivi
        self.voittoluokat=voittoluokat
        
    def tarkista(self,rivi):
        numerot=self.laskenumerot(rivi)
        lisanumerot=self.laskelisanumerot(rivi)
        voitot=[]
        for voittoluokka in self.voittoluokat:
            if numerot>=voittoluokka.numerot_count and lisanumerot>=voittoluokka.lisanumerot_count:
                voitot.append(voittoluokka)
        return voitot
        
    def laskenumerot(self,rivi):
        count=0
        for numero in rivi:
            if numero in self.voittorivi.numerot:
                count+=1
        return count
        
    def laskelisanumerot(self,rivi):
        count=0
        for numero in rivi:
            if numero in self.voittorivi.lisanumerot:
                count+=1
        return count

class LottoTarkistajaTest(unittest.TestCase):
    class voittorivi:
        numerot=[1,2,3,4,5,6,7]
        lisanumerot=[8,9,10]
    class voittoluokka:
        def __init__(self,numerot,lisanumerot=0):
            self.numerot_count=numerot
            self.lisanumerot_count=lisanumerot
    voittoluokka7=voittoluokka(7)
    voittoluokka61=voittoluokka(6,1)
    voittoluokka6=voittoluokka(6)
    voittoluokka5=voittoluokka(5)
    voittoluokka4=voittoluokka(4)
    voittoluokat=[voittoluokka7,voittoluokka61,voittoluokka6,voittoluokka5,voittoluokka4]
    def setUp(self):
        self.tarkastaja=LottoTarkistaja(self.voittorivi(),self.voittoluokat)
    def tearDown(self):
        self.tarkastaja=None
    def test_seitsemanoikein(self):
        result=self.tarkastaja.tarkista([1,2,3,4,5,6,7])
        self.assertEqual(len(result),4)
        self.assertTrue(self.voittoluokka4 in result)
        self.assertTrue(self.voittoluokka5 in result)
        self.assertTrue(self.voittoluokka6 in result)
        self.assertTrue(self.voittoluokka7 in result)
    def test_eivoittoa(self):
        result=self.tarkastaja.tarkista([8,9,10,11,12,13,5])
        self.assertEqual(result,[])
    def test_kuusijalisanumerooikein(self):
        result=self.tarkastaja.tarkista([6,5,8,4,3,2,1])
        self.assertEqual(len(result),4)
        self.assertTrue(self.voittoluokka4 in result)
        self.assertTrue(self.voittoluokka5 in result)
        self.assertTrue(self.voittoluokka6 in result)
        self.assertTrue(self.voittoluokka61 in result)
        
if __name__ == '__main__':
    unittest.main()