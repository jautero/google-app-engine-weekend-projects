# -*- coding: latin-1 -*-
from BeautifulSoup import BeautifulSoup
import re
import unittest
class LottoPageParser:
    def __init__(self):
        self.kierros=0
        self.numerot=[]
        self.lisanumerot=[]
        
    def find_kierros(self,text):
        regexp=re.compile("Kierros (\d+)")
        result=regexp.search(text)
        if result:
            return int(result.group(1))
        else:
            return 0
    def feed(self,content):
        soup=BeautifulSoup(content)
        tulokset=soup.find(text="Uusimmat tulokset")
        self.kierros=self.find_kierros(tulokset.parent.nextSibling.nextSibling.string)
        tulokset=soup.find("table",{"class":"numbers"}).find("tbody").find("tr") 
        for item in tulokset.findAll("td"):
            itemclass=item.get("class")
            try:
                itemnumber=int(item.string)
            except:
                itemnumber=0
            if itemclass==None and itemnumber !=0:
                self.numerot.append(itemnumber)
            if itemclass=="secondary" and itemnumber != 0:
                self.lisanumerot.append(itemnumber)

class LottoPageParserTester(unittest.TestCase):
    def setUp(self):
        self.lottoparser=LottoPageParser()
        
    def test_latest(self):
        self.lottoparser.feed(testdata1)
        self.assertEqual(self.lottoparser.kierros,22)
        self.assertEqual(len(self.lottoparser.numerot),7)
        self.assertEqual(len(self.lottoparser.lisanumerot),3)
        self.assertTrue(self.lottoparser.numerot==[3,5,17,19,26,36,38])
        self.assertTrue(self.lottoparser.lisanumerot==[14,25,27])

if __name__ == '__main__':
    testdata1="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fi" lang="fi">
    <head>


              <title>Veikkaus - Lotto - Etusivu</title>


          <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
      <link rel="icon" href="/info/media/shared/favicon.ico" type="image/ico" />
      <link rel="stylesheet" type="text/css" href="/css/common.css?v=14" />
            <link rel="stylesheet" type="text/css" href="/css/games.css?v=14" />
          <script type="text/javascript" src="/js/texts_www_fi.js?v=14"></script>

      <script type="text/javascript" src="/js/utils_www.js?v=14"></script>
      <script type="text/javascript" src="/js/xml_www.js?v=14"></script>
      <script type="text/javascript" src="/js/gamefolder_www.js?v=14"></script>
      <script type="text/javascript">
        doBrowserCheck();
      </script>
      <link rel="stylesheet" type="text/css" href="/css/lotto.css?v=14" />
      <link rel="stylesheet" type="text/css" media="print" href="/css/print.css?v=14" />
      <script type="text/javascript" src="/js/utils_goc_www.js?v=14"></script>

      <script type="text/javascript" src="/js/lotto_www.js?v=14"></script>
      <script type="text/javascript">





    var rowPrice = 80 / 100.0;
    var awdExtraRowPrice = 20 / 100.0;
    var jokerPrice = 200 / 100.0;
    var awdEnabled = "true".toLowerCase() == "true" ? true : false; // to get real primitives

    /* Tells if this page is the normal / system / reduced system lotto */
    var baseURL = "/pelit";
    var game = "lotto";
    var sys = "frontpage";

    var MAXVALUE, NUMBEROFROWS, MAXSELECTIONS, systemSize, systemRowCounts, reducedSystemRowCounts;

    // Changes global "config" parameters for game mode
    function selectGameMode(mode) {
        if(game == "lotto") {
    	    if(mode == "system") {
    	        NUMBEROFROWS = 1;
    	        MAXSELECTIONS = 8;
    	        systemSize = 98;
    	    }
    	    else if(mode == "reduced") {
    	        NUMBEROFROWS = 1;
    	        MAXSELECTIONS = 12;
    	        systemSize = 99;
    	    }
    	    else {
    	        NUMBEROFROWS = 12;
    	        MAXSELECTIONS = 7;
        		BLOCK_SIZE = 1;
        		MIN_BLOCKS = 12;
        		MAX_BLOCKS = 20;
    	        systemSize = 7;
    	    }

        // Maps system row length to number of actual rows generated
    		    systemRowCounts = {
    			        8 : 8,
    			        9 : 36,
    			        10 : 120,
    			        11 : 330
    		    };

        reducedSystemRowCounts = {
    		        12 : 60,
    		        13 : 112,
    		        14 : 196,
    		        15 : 237,
    		        16 : 439,
    		        18 : 600
    		    };

    		    MAXVALUE = 39;
    	    }

        if (game == "viking") {
    	    if(mode == "system") {
    	        NUMBEROFROWS = 1;
    	        MAXSELECTIONS = 7;
    	        systemSize = 98;
    	    }
    	    else if(mode == "reduced") {
    	        NUMBEROFROWS = 1;
    	        MAXSELECTIONS = 12;
    	        systemSize = 99;
    	    }
    	    else {
    	        NUMBEROFROWS = 10;
        		BLOCK_SIZE = 1;
        		MIN_BLOCKS = 12;
        		MAX_BLOCKS = 20;
    	        MAXSELECTIONS = 6;
    	        systemSize = 6;
    	    }

    	    systemRowCounts = {
    			        7 : 7,
            			8 : 28,
    			        9 : 84,
    			        10 : 210,
    			        11 : 462
    	    };

    	    reducedSystemRowCounts = {
    	        12 : 41,
    	        13 : 66,
    	        14 : 80,
    	        15 : 120,
    	        16 : 160,
    	        17 : 188,
    	        18 : 236,
    	        19 : 330,
    	        20 : 400,
    	        24 : 784
        	};

        	MAXVALUE = 48;   
        	}

        sys = mode;
    }

    // Initial game mode, defined at top of lotto_form_*.vm etc.
    selectGameMode(sys);
      </script>
    </head>

    <body onload="initFrontpage();" id="lotto" onunload="unload()">
      <div id="container">

    <!-- header.vm START -->
        <div id="header">


      <div id="top-nav">

        <ul>
          <li class="first">
            <a href="/" id="logo" title="Veikkaus"><img src="/info/media/shared/logo.jpg" alt="Veikkaus" /></a>
          </li>
                      <li class="games current" onclick="toggleGameList(this, event);">
                <a href="#" title="Pelit" onclick="return false;">Pelit</a>
            <div class="container">
              <p>Pelien sivuilta löydät pelikupongit, viimeisimmät tulokset, peliohjeet ja tilastot.</p>

              <ul>
                <li class="lotto"><a href="/pelit?op=frontpage&amp;game=lotto&amp;l=f" title="Lotto">Lotto</a></li>
                <li class="keno"><a href="/pelit?op=frontpage&amp;game=keno&amp;l=f" title="Keno">Keno</a></li>
                <li class="viking"><a href="/pelit?op=frontpage&amp;game=viking&amp;l=f" title="Viking Lotto">Viking Lotto</a></li>
            	                                    <li class="jokeri"><a href="/pelit?op=frontpage&amp;game=jokeri&amp;l=f" title="Jokeripelit">Jokeripelit</a></li>
            		    		            <li class="bingo"><a href="/pelit?op=frontpage&amp;game=bingo&amp;l=f" title="Veikkausbingo">Veikkausbingo</a></li>

                                        <li>&nbsp;</li>

                <li>&nbsp;</li>
                  </ul>

                  <ul class="viiva">
          <!-- Help snippet snippet/help/fi/other/games_einstant_links.html start -->
                  <li class="einstant"><a href="/pelit?game=einstant&amp;op=frontpage&amp;l=f" title="Nettiarvat" class="current">Nettiarvat:</a></li>
                  <li class="einstant"><a href="/info/nettiarvat/saunaan/index.html" title="Saunaan-arpa">- Saunaan-arpa</a></li>

                  <li class="einstant"><a href="/info/nettiarvat/palapeli/index.html" title="Palapeli-arpa">- Palapeli-arpa</a></li>
                  <li class="einstant"><a href="/info/nettiarvat/kesa/index.html" title="Kes&auml;-arpa">- Kes&auml;-arpa</a></li>
                  <li class="einstant"><a href="/info/nettiarvat/jalokivi/index.html" title="Jalokiviarpa">- Jalokiviarpa</a></li>
                  <li class="einstant"><a href="/info/nettiarvat/onnenbiisit/index.html" title="Onnenbiisit-arpa">- Onnenbiisit</a></li>
                  <li class="einstant"><a href="/info/nettiarvat/onnensanat/index.html" title="Onnensanat-arpa">- Onnensanat</a></li>  
                  <li class="einstant"><a href="/info/nettiarvat/assa/index.html" title="&Auml;ss&auml;-arpa">- &Auml;ss&auml; </a></li>

                  <li class="einstant"><a href="/info/nettiarvat/casino/index.html" title="Casino-arpa">- Casino</a></li>
    			  <li class="einstant"><a href="/info/nettiarvat/luonto/index.html" title="Luontoarpa">- Luonto</a></li>
                  <li class="einstant"><a href="/info/nettiarvat/horoskooppi/index.html" title="Horoskooppiarpa">- Horoskooppi</a></li>
    			  <!-- Help snippet snippet/help/fi/other/games_einstant_links.html end -->
              </ul>
                  <ul class="viiva">
                <li class="fixedodds"><a href="/pelit?op=frontpage&amp;game=fixedodds&amp;l=f" title="Pitkäveto">Pitkäveto</a></li>

                    <li class="score"><a href="/pelit?op=frontpage&amp;game=score&amp;l=f" title="Tulosveto">Tulosveto</a></li>
                    <li class="multiscore"><a href="/pelit?op=frontpage&amp;game=multiscore&amp;l=f" title="Moniveto">Moniveto</a></li>
                    <li class="winner"><a href="/pelit?op=frontpage&amp;game=winner&amp;l=f" title="Voittajavedot">Voittajavedot</a></li>
                        <li class="live"><a href="/live?op=frontpage&amp;l=f" title="Live-veto">Live-veto</a></li>
                    <li class="sport"><a href="/pelit?op=frontpage&amp;game=sport&amp;l=f" title="Vakiot">Vakiot</a></li>
                    <li class="ravi"><a href="/pelit?op=frontpage&amp;game=ravi&amp;l=f" title="V-pelit">V-pelit</a></li>

                                          </ul>

             	 <ul class="viiva">
        <!-- Help snippet snippet/help/fi/other/games_non_gaming_links.html start -->
        <li><a href="/info/pelit/index.html" title="Pelit-etusivu">Pelit-etusivu</a></li>
        <li><a href="/pelit?op=jackpot&amp;l=f" title="Potit">Potit</a></li>
    	<li><a href="/info/arvat/index.html" title="Arvat">Arvat</a></li>
        <li><a href="/info/pelitilastot/index.html" title="Pelitilastot">Pelitilastot</a></li>

        <li><a href="#" title="Tulokset" onclick="window.open('/info/apua/tuloshaku/index.html','Tulostenhakukone','toolbar=no,directories=no,status=no,scrollbars=yes,resizable=yes,menubar=no,location=no,copyhistory=no,width=600,height=600')">Tulokset</a></li>
        <li><a href="/info/abc/palvelut/rastipekka.html">Rastipekka</a></li>
        <li><a href="/info/abc/index.html" title="Pelaamisen ABC">Pelaamisen ABC</a></li>
        <li><a href="/info/pelipaussi/index.html" title="Pelipaussi">Pelipaussi</a></li><!-- Help snippet snippet/help/fi/other/games_non_gaming_links.html end -->
          	    </ul>
              <div class="clearer"></div>

              <ul class="footer">
                <li class="close"><a href="#" title="Sulje" onclick="return false;">Sulje</a></li>
              </ul>
              <div class="clearer"></div>
            </div>
          </li>    
          <!--end of game link-->



          <li class="dreams " onclick="toggleGameList(this, event);">

            <a href="#" title="Haave" onclick="return false;" >Haave</a>
            <div class="container">
             	 <ul>
          <!-- Help snippet snippet/help/fi/other/dreams_links.html start -->
    				<li class="dreams"><a href="/info/haaveita/index.html" title="Haave-etusivu" class="current">Haave-etusivu</a></li>
    				<li class="dreams"><a href="/info/haaveita/voittajat/index.html" title="Voittajat">Voittajat</a></li>
    				<li class="dreams"><a href="/info/haaveita/kun_voitat/index.html" title="Kun voitat">Kun voitat</a></li>

    				<li class="dreams"><a href="/info/haaveita/loyda_pelisi/index.html" title="L&ouml;yd&auml; pelisi">L&ouml;yd&auml; pelisi</a></li>
    				<li class="dreams"><a href="/info/kenossa/index.html" title="Kenossa">Kenossa</a></li>
                    <li class="dreams"><a href="https://www2.veikkaus.fi/jokerivitsi/">Jokerivitsi</a></li>
                    <!-- Help snippet snippet/help/fi/other/dreams_links.html end -->
             	 </ul>
              <div class="clearer"></div>

              <ul class="footer">
                <li class="close"><a href="#" title="Sulje" onclick="return false;">Sulje</a></li>
              </ul>
              <div class="clearer"></div>
            </div>
          </li>

          <li class="sports " onclick="toggleGameList(this, event);">
            <a href="#" title="Urheilu" onclick="return false;" >Urheilu</a>

            <div class="container">
             	 <ul>
          <!-- Help snippet snippet/help/fi/other/sports_links.html start -->
                          <li class="sports"><a href="/info/urheilua/index.html" title="Urheilu-etusivu" class="current">Urheilu-etusivu</a></li>
                          <li class="sports"><a href="/info/urheilua/vakio/index.html" title="Vakioviikko">Vakioviikko</a></li>
                          <li class="sports"><a href="/info/urheilua/sports_week.html" title="Kalenteri">Kalenteri</a></li>
                          <li class="sports"><a href="/info/urheilua/paivanvedot/index.html" title="P&auml;iv&auml;n vedot">P&auml;iv&auml;n vedot</a></li>

                          <li class="sports"><a href="/info/urheilua/urheilutilastot/index.html" title="Tilastot">Tilastot</a></li>
    					  <li class="sports"><a href="/info/urheilua/jalkipelit/index.html" title="J&auml;lkipelit">J&auml;lkipelit</a></li>
                 <li class="sports"><a href="https://www3.veikkaus.fi/vetosm/index.html" title="Vedonly&ouml;nnin SM-kisa"><strong>Veto SM</strong></a></li>
                 <li class="sports"><a href="https://www3.veikkaus.fi/v75sm/index.html" title="V75 SM"><strong>V75 SM</strong></a></li>
                 <li class="sports"><a href="https://www3.veikkaus.fi/vakiosm/index.html" title="Vakio SM"><strong>Vakio SM</strong></a></li>
    					  <!-- Help snippet snippet/help/fi/other/sports_links.html end -->

             	 </ul>
              <div class="clearer"></div>
              <ul class="footer">
                <li class="close"><a href="#" title="Sulje" onclick="return false;">Sulje</a></li>
              </ul>
              <div class="clearer"></div>
            </div>
          </li>


          <li class="entertainment " onclick="toggleGameList(this, event);">
            <a href="#" title="Viihde" onclick="return false;" >Viihde</a>
            <div class="container">
             	 <ul>
          <!-- Help snippet snippet/help/fi/other/entertainment_links.html start -->
                          <li class="entertainment"><a href="/info/viihde/index.html" title="Viihde-etusivu" class="current">Viihde-etusivu</a></li>
                          <li class="entertainment"><a href="/info/viihde/arvonnat/index.html" title="Arvonnat">Arvonnat</a></li>

    <li class="entertainment"><a href="/info/viihde/kampanjat/index.html" title="Kampanjat">Kampanjat</a></li><!-- Help snippet snippet/help/fi/other/entertainment_links.html end -->
             	 </ul>
              <div class="clearer"></div>
              <ul class="footer">
                <li class="close"><a href="#" title="Sulje" onclick="return false;">Sulje</a></li>
              </ul>
              <div class="clearer"></div>
            </div>

          </li>

          <li class="company " onclick="toggleGameList(this, event);">
            <a href="#" title="Yritys" onclick="return false;" >Yritys</a>
            <div class="container">
             	 <ul>
          <!-- Help snippet snippet/help/fi/other/company_links.html start -->
                          <li class="company"><a href="/info/yritys/index.html" title="Yritys-etusivu" class="current">Yritys-etusivu</a></li>
                          <li class="company"><a href="/info/yritys/yritysinfo/index.html" title="Yritysinfo">Yritysinfo</a></li>

                          <li class="company"><a href="/info/yritys/vastuullisuus/index.html" title="Vastuullisuus">Vastuullisuus</a></li>
                          <li class="company"><a href="/info/yritys/tyopaikat/index.html" title="Ty&ouml;paikat">Ty&ouml;paikat</a></li>
                          <li class="company"><a href="/info/yritys/medialle/index.html" title="Medialle">Medialle</a></li>
    					  <li class="company"><a href="/info/yritys/avainluvut/raportit.html" title="Raportit">Raportit</a></li><!-- Help snippet snippet/help/fi/other/company_links.html end -->
             	 </ul>
              <div class="clearer"></div>

              <ul class="footer">
                <li class="close"><a href="#" title="Sulje" onclick="return false;">Sulje</a></li>
              </ul>
              <div class="clearer"></div>
            </div>
          </li>

          <li class="myveikkaus " onclick="toggleGameList(this, event);">
            <a href="#" title="Oma Veikkaus" onclick="return false;" >Oma Veikkaus</a>

            <div class="container">
             	 <ul>
          <!-- Help snippet snippet/help/fi/other/myveikkaus_links.html start -->
    					  <li class="myveikkaus"><a href="/pelit?op=myveikkaus_frontpage&amp;section=account&amp;l=f" title="Oma Veikkaus -etusivu" class="current">Oma Veikkaus -etusivu</a></li>
                          <li class="myveikkaus"><a href="/pelit?op=playeraccount_frontpage&amp;section=account&amp;l=f" title="Pelitili">Pelitili</a></li>
                          <li class="myveikkaus">&nbsp;<a href="/pelit?section=account&op=playeraccount_transfer_funds_frontpage&l=f" title="Rahansiirto">- Rahansiirto</a></li>
                          <li class="myveikkaus"><a href="/pelit?section=account&amp;op=customer_frontpage&amp;l=f" title="Asiakkuus">Asiakkuus</a></li>

                          <li class="myveikkaus"><a href="/pelit?section=account&amp;op=services_frontpage&amp;l=f" title="Palvelut">Palvelut</a></li>
    					  <li class="myveikkaus"><a href="/info/veikkauskorttiedut/index.html" title="Veikkaus-korttiedut" class="current">Veikkaus-korttiedut</a></li>
      					  <li class="myveikkaus"><a href="/info/veikkauskorttiedut/veikkauskortti/index.html" title="Veikkaus-kortti">Veikkaus-kortti</a></li>
       					  <li class="myveikkaus"><a href="/info/veikkauskorttiedut/asiakaslehti/index.html" title="Asiakaslehti">Asiakaslehti</a></li>
    <!-- Help snippet snippet/help/fi/other/myveikkaus_links.html end -->
             	 </ul>
              <div class="clearer"></div>

              <ul class="footer">
                <li class="close"><a href="#" title="Sulje" onclick="return false;">Sulje</a></li>
              </ul>
              <div class="clearer"></div>
            </div>
          </li>

            </ul>
      </div>

      <div id="login-box"></div>
                      <script type="text/javascript">
        <!--
        var is_iframe = isLoginIframe();
        if (is_iframe) {
          document.write('<iframe src="/pelit?op=login_info&amp;l=f" name="loginFrame" id="login"><' + '/iframe>');
        }  
        -->
      </script>
        </div>
      <noscript>
        <div class="error" style="margin-left: 10px; margin-right: 10px;"> 
        <p><strong>Selaimesi ei tue JavaScriptiä tai JavaScript ei ole päällä. <a href="/pelit?op=nojavascript&amp;l=f">Lue lisää</a>.<br>Voit käyttää myös <a href="/mobile"> mobiilikäyttöliittymää </a>.</strong></p>
      </div>
    </noscript>
    <!-- header.vm END -->

    <!-- navigation_full.vm START -->
          <div id="sub-nav">
      <ul>

                <li class="first current"><a href="/pelit?game=lotto&amp;op=frontpage&amp;l=f" title="Lotto">Lotto</a></li>

                    <li class=""><a href="/tuloshaku?game=lotto&amp;op=results_frontpage&amp;l=f" title="Tulokset">Tulokset</a></li>
                <li>  <a href="/info/lotto/pelitietoa.html" title="Pelitietoa">Pelitietoa</a></li>
          <li>  <a href="/info/lotto/ohje.html" title="Ohje">Ohje</a></li>
        <li>  <a href="/info/lotto/saannot.html" title="Säännöt">Säännöt</a></li>

          </ul>
      <div class="clearer"></div>
    </div>
    <!-- navigation_full.vm END -->


    <div class="headings">
      <h1>Lotto</h1>
      <h2>Kierros 23</h2>
    </div>
        <div id="content-container" class="bg">

          <div id="content">
                                <h3 class="ad"><a href="/pelit?game=lotto&amp;op=form" title="Täysosumille jaossa 7 100 000 e">Täysosumille jaossa <em>7 100 000 e</em></a></h3>
        <img src="/info/media/shared/lotto/bg-lotto-frontpage.gif" class="ad" alt="" />

            <div id="play">
              <h2><a href="/pelit?game=lotto&amp;op=form&amp;l=f" title="Pelikuponki">Pelikuponki</a></h2>
              <!-- draw = 1065 -->
              <p>Pelaaminen päättyy la 12.6. klo 20.30</p>

                                                        <div>
          <p>Täysosumille jaossa <strong>7 100 000 e.</strong><br/>
                            &nbsp;
    </p>
        </div>

              <p>
                <strong>Pelitavat:</strong>
                <a href="/pelit?game=lotto&amp;op=form&amp;l=f" title="Tavallinen">Tavallinen</a> | 
                <a href="/pelit?game=lotto&amp;op=systemform&amp;l=f" title="Järjestelmä">Järjestelmä</a> | 
                <a href="/pelit?game=lotto&amp;op=reducedform&amp;l=f" title="Harava">Harava</a> |
                <a href="/pelit?game=lotto&amp;op=dreamform&amp;l=f" title="Unelmalotto">Unelmalotto</a>                        	| <a href="/pelit?game=lotto&amp;op=favouriterowsform&amp;l=f" title="Suosikkirivit">Suosikkirivit</a>                      </p>

            </div>

            <div class="help-links">
    <!-- Help snippet snippet/help/fi/lotto/lotto_links.html start -->

    <p>Lottoarvonnan voit kuunnella my&ouml;s Yle Radio Suomesta joka lauantai klo 20.45.</p>
    <p><img src="/info/media/mainokset/ajankohtaiset/kuponkisivun_mainos/lottoradio.jpg" alt="Radio" width="120" height="60" />
    </p>
    <!--<h3><strong><img src="/info/media/mainokset/ajankohtaiset/kuponkisivun_mainos/lottoradio.jpg" width="120" height="60" /><br />
    Lottoa my&ouml;s radiosta</strong></h3>
    <p>Lauantain lottoarvonnat  kuuluvat 27. kes&auml;kuuta alkaen my&ouml;s <strong>Ylen Radio Suomessa. Kello 20.45 </strong>alkavia,  suorana l&auml;hetett&auml;vi&auml; arvontoja voi kuunnella Ylen aalloilla elokuun loppuun  saakka kaikkialla Suomessa.</p>
    --><!-- Help snippet snippet/help/fi/lotto/lotto_links.html end -->
            </div>

            <div class="content-block previous-round">

              <h2>Uusimmat tulokset</h2>
                      <h2>Kierros 22</h2>
                    <!-- lotto_result_single.vm START -->


    <div class="heading">
      <h3>Arvonta 1 - </h3>
      <p>Arvontapäivämäärä la 5.6.2010</p>

    </div>

    <table class="numbers">
      <thead>
        <tr>
          <th colspan="7">Oikea rivi</th>
          <th class="separate"></th>
          <th colspan="3">Lisänumerot</th>
        </tr>

      </thead>
      <tbody>
        <tr>
          <td>3</td>
          <td>5</td>
          <td>17</td>
          <td>19</td>

          <td>26</td>
          <td>36</td>
          <td>38</td>
          <td class="separate"></td>
            <td class="secondary">14</td>
            <td class="secondary">25</td>

            <td class="secondary">27</td>
          </tr>
      </tbody>
    </table>


      <h3>Voitonjako</h3>
    <table class="shares">
      <tbody>
          <tr>

          <th>7 oikein</th>
          <td>- kpl</td>
          <td>-&nbsp;&euro;</td>
        </tr>
          <tr>
          <th>6+1 oikein</th>
          <td>21 kpl</td>

          <td>11&nbsp;363,90&nbsp;&euro;</td>
        </tr>
          <tr>
          <th>6 oikein</th>
          <td>177 kpl</td>
          <td>1&nbsp;430,80&nbsp;&euro;</td>

        </tr>
          <tr>
          <th>5 oikein</th>
          <td>8920 kpl</td>
          <td>43,10&nbsp;&euro;</td>
        </tr>
          <tr>

          <th>4 oikein</th>
          <td>137185 kpl</td>
          <td>11,70&nbsp;&euro;</td>
        </tr>
          <tr><th>&nbsp;</th></tr>
        <tr><th>LottoPlus &minus; lisävoittoluokat</th></tr>

          <tr>
          <th>4+3 oikein</th>
          <td>11 kpl</td>
          <td>5&nbsp;415,70&nbsp;&euro;</td>
        </tr>
          <tr>
          <th>4+2 oikein</th>

          <td>1250 kpl</td>
          <td>40,70&nbsp;&euro;</td>
        </tr>
          <tr>
          <th>4+1 oikein</th>
          <td>17343 kpl</td>
          <td>5,10&nbsp;&euro;</td>

        </tr>
          <tr>
          <th>3+3 oikein</th>
          <td>390 kpl</td>
          <td>146,50&nbsp;&euro;</td>
        </tr>
          <tr>

          <th>3+2 oikein</th>
          <td>16779 kpl</td>
          <td>5,30&nbsp;&euro;</td>
        </tr>
          <tr>
          <th>3+1 oikein</th>
          <td>154615 kpl</td>

          <td>1,00&nbsp;&euro;</td>
        </tr>
          <tr><th>&nbsp;</th></tr>
      </tbody>
    </table>

    <!-- lotto_result_single.vm END -->
      		<table class="links">
              <tr>
                <td class="search-link"><a href="/tuloshaku?game=lotto&amp;op=results_frontpage" title="Tuloshaku">Tuloshaku</a></td>

                <td class="print-link"><a href="javascript:print();" title="Tulosta">Tulosta</a></td>
              </tr>
    		</table>
            </div>
    	<div class="content-block">
    <!-- Help snippet snippet/help/fi/lotto/lotto_frontpage.html start -->
    <h2>Lotto lyhyesti</h2>
    <ul>
      <li>valitaan 7 numeroa 39:st&auml; </li>

      <li>arvotaan 7 numeroa ja 3 lis&auml;numeroa 39:st&auml;</li>
      <li>rivihinta 0,80 euroa, lis&auml;voittoluokat 0,20 euroa </li>
      <li>hajarivej&auml; 1-20 kpl kupongilla  </li>
      <li>j&auml;rjestelm&auml;ss&auml; 8-11 rastia </li>

      <li>haravassa 12-18 rastia  </li>
      <li>maksamalla 0,20 euron lis&auml;maksun rivi osallistuu  my&ouml;s lis&auml;voittoluokkiin</li>
      <li>peliaika p&auml;&auml;ttyy yleens&auml; lauantaina kello 20.30</li>
      <li>arvonta-aika yleens&auml; lauantaina kello 20.45</li>

      <li>2, 3, 5, 10 viikon kestopelit tai ikipeli</li>
      <li>p&auml;&auml;voitto 7 oikein -tuloksella</li>
      <li>voitto jo 4 oikein -tuloksella </li>
      <li>lis&auml;voittoluokissa voitto jos riviss&auml; 3 tai 4 oikein ja lis&auml;ksi 1, 2  tai 3 lis&auml;numeroa oikein</li>

      <li><a href="https://www.veikkaus.fi/info/kampanjat/lottoplus_ja_vikingplus/lottoplus_ja_vikingplus.html#ikipeliohje">N&auml;in lis&auml;&auml;t LottoPlus-lis&auml;voittoluokat ikipeliin</a></li>
      <li><a href="/info/lotto/haravaopas_plussat.html">Haravaopas kertoo Plussien voittoluokat</a><br />
      </li>
    </ul>
    <p>&nbsp;</p>
    <!-- Help snippet snippet/help/fi/lotto/lotto_frontpage.html end -->
    	</div>
     </div>

          <hr class="hide" />

          <div id="extras">
    <!-- gamefolder_empty.vm START -->
    <!-- salestimes.vm START -->
    <script type="text/javascript">
      gamingSystemOpen = false;
      openTargetsExist = true;
    </script>

            <script type="text/javascript">
          gamingSystemOpen = true;
        </script>
                            <!-- salestimes.vm END -->

    <div id="folder" class="harmaa">
          <div class="heading-left">
    	      <div class="heading-right">
          <h3>Pelikansio</h3>
        </div>
      </div>
      <div id="folder-content" class="empty-rows">

        <!-- salestimes.vm START -->

    <script type="text/javascript">
      gamingSystemOpen = false;
      openTargetsExist = true;
    </script>

            <script type="text/javascript">
          gamingSystemOpen = true;
        </script>
                            <!-- salestimes.vm END -->

        <div class="empty-content">
          Pelikansiossa ei ole pelejä.    </div>
      </div>
    </div>

    <!-- gamefolder_empty.vm END -->
    <!-- lotto_quickpick.vm START -->
    <form action="/pelit?game=lotto&amp;op=checkGame&amp;stats_wager_type=quickpick" method="post" name="lotto-quickgame" onsubmit="return isQuickPickValid(this);" >
      <div class="game-box">
        <input type="hidden" name="system_size" value="7" />
        <input type="hidden" name="Pelaapikapeli" value="Pelaa" />

        <div class="heading-left"><div class="heading-right">
          <h3>Pelaa Loton pikapeli</h3>
        </div>

      </div>   <div class="box">
        <div class="game">
          <p>
            <label>
              <strong>Rivimäärä</strong>
              <select id="quick_rows" name="quick_rows" onchange="updateQuickPickGamePrice(this.form, 'quick-price');">
                <option value="1">1 rivi</option>

     <option value="2">2 riviä</option>

     <option value="3">3 riviä</option>

     <option value="4">4 riviä</option>

     <option value="5">5 riviä</option>

     <option value="6">6 riviä</option>

     <option value="7">7 riviä</option>


     <option value="8">8 riviä</option>

     <option value="9">9 riviä</option>

     <option value="10">10 riviä</option>

     <option value="11">11 riviä</option>

     <option value="12" selected="selected">12 riviä</option>

     <option value="13">13 riviä</option>


     <option value="14">14 riviä</option>

     <option value="15">15 riviä</option>

     <option value="16">16 riviä</option>

     <option value="17">17 riviä</option>

     <option value="18">18 riviä</option>

     <option value="19">19 riviä</option>


     <option value="20">20 riviä</option>

              </select>
            </label>
            <label>
              <strong>Kesto</strong>
              <select id="duration" name="D" onchange="updateQuickPickGamePrice(this.form, 'quick-price');">
                <option value="1" selected="selected">1 viikko</option>

                <option value="2">2 viikkoa</option>
                <option value="3">3 viikkoa</option>
                <option value="5">5 viikkoa</option>
                <option value="10">10 viikkoa</option>
                <option value="0">Ikipeli</option>
              </select>

            </label>
          </p>
    	  <p class="checkbox">
              <strong>LottoPlus &minus; lisävoittoluokat: </strong>
              <label for="awdCheckBox">
                <input type="checkbox" id="awdCheckBox" name="awdSelected" value="true" onclick="updateQuickPickGamePrice(this.form, 'quick-price');" />
                + 0,20&nbsp;&euro;/rivi          </label>

          </p> 
          	<!-- jokeri_gamesaddon.vm START -->

    	<p class="checkbox" id="jokeri_gamesaddon">




       	<strong id="jokeri_game_name">Jokeripelit: </strong>
    	<span>
    		<label for=lottojokeri_sidegame>
    	    	<input type="checkbox" id="lottojokeri_sidegame" name="lottojokeri_sidegame" value="0" 
    	    		onclick="this.checked ? value = 1 : value = 0;updateJokerSelectList();updateQuickPickGamePrice(this.form, 'quick-price')"  />
    	    	Lauantai-Jokeri<br/>

    	    </label>
    	</span>
    	<strong id="jokeri_game_name">Jokeririvejä </strong>
    	<select id="jokeri_rows" name="jokeri_rows" onclick="updateQuickPickGamePrice(this.form, 'quick-price')" disabled>
    											<option value="1" selected="selected">
    							1 rivi						</option>
    											<option value="2" >
    							2 riviä						</option>

    											<option value="3" >
    							3 riviä						</option>
    											<option value="4" >
    							4 riviä						</option>
    											<option value="5" >
    							5 riviä						</option>
    											<option value="6" >

    							6 riviä						</option>
    											<option value="7" >
    							7 riviä						</option>
    											<option value="8" >
    							8 riviä						</option>
    											<option value="9" >
    							9 riviä						</option>

    											<option value="10" >
    							10 riviä						</option>
    			</select>

    <input type="hidden" name="jokeriNumbers" value="" />
    </p>
    <!-- jokeri_gamesaddon.vm END -->
        </div>     <div class="price">
          <h4>Hinta .... <span id="quick-price">0,00&nbsp;&euro;</span></h4>

        </div>
        <div class="submit">
          <input type="submit" id="qp-submit" name="pikapeli" value="Pelaa" />
        </div>
      </div> </div>
    </form>
    <!-- lotto_quickpick.vm END -->
    <!-- Help snippet snippet/help/fi/lotto/lotto_frontpage_side.html start -->
    <!-- Help snippet snippet/help/fi/lotto/lotto_frontpage_side.html end -->
          </div>

          <div class="clearer"></div>
        </div>

    <!-- footer.vm START -->
          <div id="footer">
      <div class="copyright">
        <p>Asiakasneuvonta päivittäin klo 8:00-22:00 <strong>0800 17284</strong></p>
        <p><a href="/info/copyright.html" title="&copy; Copyright Veikkaus Oy">&copy; Copyright Veikkaus Oy</a></p>

      </div>

      <div class="nav">
        <ul>
                <li class="first"><a href="/info/abc" title="Pelaamisen ABC">Pelaamisen ABC</a></li>
          <li><a href="info/sivukartta.html" title="Sivukartta">Sivukartta</a></li>
          <li>  <a href="/info/palaute/" title="Palaute">Palaute</a></li>

                  <li class="last"><a href="info/pelipaussi/" title="Pelipaussi">Pelipaussi</a></li>
              </ul>
      </div>
      <div class="clearer"></div>
    </div>
      <!-- APP time: 8.6.2010 klo 23.25 -->
            <script type="text/javascript">
        language = "f";
        userId = "";
          statisticPrice = "";
          statisticsPageId = "lotto_frontpage";
        statisticsPageExtraId = "";
      </script>
      <!-- Help snippet snippet/help/fi/other/statistics.html start -->

       <script type="text/javascript" src="/info/statistic/swatag.js"></script>
    <!-- Help snippet snippet/help/fi/other/statistics.html end -->
    <!-- footer.vm END -->

        <div class="clearer"></div>
      </div>
    </body>
    </html>
    """
    unittest.main()