"""Test for METAR Library
Author: Matthieu BOUCHET
"""
from metar.metar import *
import unittest


class testsMetar(unittest.TestCase):
    """Class of unitary tests for METAR Library
    """

    def test_getMetar(self):
        metar = Metar('LFLY','LFLY 292200Z AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.getMetar(),'LFLY 292200Z AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG')

    def test_getDateTime(self):
        metar = Metar('LFLY','LFLY 292200Z AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.getDateTime(),("29","22","00"))

    def test_analyzeChangements(self):
        metar = Metar('LFLY','LFLY 192100Z AUTO 17012KT CAVOK 06/M02 Q1017 BECMG 19020G35KT')
        self.assertEquals(metar.analyzeChangements(),{
            'TEMPO':None,
            'BECMG':'19020G35KT',
            'GRADU':None,
            'RAPID':None,
            'INTER':None,
            'TEND':None
        })

        metar = Metar('LFLY','LFLY 192100Z AUTO 17012KT CAVOK 06/M02 Q1017 TEMPO 19020G35KT')
        self.assertEquals(metar.analyzeChangements(),{
            'TEMPO':'19020G35KT',
            'BECMG':None,
            'GRADU':None,
            'RAPID':None,
            'INTER':None,
            'TEND':None
        })

        metar = Metar('LFLY','LFLY 192100Z AUTO 17012KT CAVOK 06/M02 Q1017 NOSIG')
        self.assertEquals(metar.analyzeChangements(),None)
        
    def test_analyzeDateTime(self):
        metar = Metar('LFLY','LFLY 292200Z AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.analyzeDateTime(),("29","22","00"))
        metar = Metar('LFLY','LFLY AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.analyzeDateTime(),None)
    
    def test_analyzeAuto(self):
        metar = Metar('LFLY','LFLY 292200Z AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.analyzeAuto(),True)
        metar = Metar('LFLY','LFLY 292200Z VRB03KT CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.analyzeAuto(),False)

    def test_analyzeWind(self):
        metar = Metar('LFLY','LFLY 292200Z AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.analyzeWind(),{
            'direction':'VRB',
            'speed':3,
            'gust':None,
            'variation':None
        })
        
        metar = Metar('LFLY','LFLY 292200Z AUTO 22005KT CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.analyzeWind(),{
            'direction':220,
            'speed':5,
            'gust':None,
            'variation':None
        })
        
        metar = Metar('LFLY','LFLY 292200Z AUTO 22010G25KT 040V210 CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.analyzeWind(),{
            'direction':220,
            'speed':10,
            'gust':25,
            'variation':(40,210)
        })
        
        metar = Metar('LFLY','LFLY 292200Z AUTO /////KT CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.analyzeWind(),None)

    def test_analyzeVizibility(self):
        metar = (Metar('LFLY','LFLY 292200Z AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG'),
        Metar('LFLY','LFLY 292200Z AUTO VRB03KT 5200 06/M00 Q1000 NOSIG'),
        Metar('LFLY','LFLY 292200Z AUTO VRB03KT 350V040 5200NE 06/M00 Q1000 NOSIG'),
        Metar('LFLY','LFLY 292200Z AUTO VRB03KT 06/M00 Q1000 NOSIG'),
        Metar('LFLY','LFLY 292200Z AUTO VRB03KT 9950 06/M00 Q1000 NOSIG'))

        results = [(9999),(5200),(5200),None,(9950)]

        for k in range(len(metar)):
            self.assertEquals(metar[k].analyzeVisibility(),results[k])

    def test_analyzeRVR(self):
        metar = (Metar('LFPG','LFPG 292200Z AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG'),
        Metar('LFPG','LFPG 292200Z AUTO VRB03KT CAVOK R26R/0450 06/M00 Q1000 NOSIG'),
        Metar('LFPG','LFPG 292200Z AUTO VRB03KT CAVOK R26L/5000 06/M00 Q1000 NOSIG'),
        Metar('LFPG','LFPG 292200Z AUTO VRB03KT CAVOK R27L/M4100 06/M00 Q1000 NOSIG'))

        results = (None,({'runway':'26R','visibility':450},),({'runway':'26L','visibility':5000},),({'runway':'27L','visibility':4100},))

        for k in range(len(metar)):
            print(metar[k].analyzeRVR())
            self.assertEquals(metar[k].analyzeRVR(),results[k])

    def test_analyzeWeather(self):
        metar = (Metar('LFLY','LFLY 231830Z AUTO 19012KT CAVOK 06/02 Q0997'),
        Metar('LFLY','LFLY 231830Z AUTO 19012KT +RETS 06/02 Q0997'),
        Metar('LFPG','LFPG 292200Z AUTO VRB03KT -VCRA R26R/0450 06/M00 Q1000 NOSIG'),
        Metar('LFPG','LFPG 292200Z AUTO VRB03KT +VCSN R26L/5000 06/M00 Q1000 NOSIG'),
        Metar('LFPG','LFPG 292200Z AUTO VRB03KT XXGR +RETS R27L/N4100 06/M00 Q1000 NOSIG'))

        results = (None,({'intensity':True,'prefix':'Recent','weather':'Thunderstorm'},),
        ({'intensity':False,'prefix':'in Vicinity','weather':'Rain'},),
        ({'intensity':True,'prefix':'in Vicinity','weather':'Snow'},),
        ({'intensity':None,'prefix':'Violent','weather':'Hail'},{'intensity':True,'prefix':'Recent','weather':'Thunderstorm'},)
        )

        
        for k in range(len(metar)):
            print(metar[k].analyzeWeather())
            
            self.assertEquals(metar[k].analyzeWeather(),results[k])

unittest.main()