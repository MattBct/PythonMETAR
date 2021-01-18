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
        metar = Metar('LFLY','LFLY 292200Z AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG'),
        Metar('LFLY','LFLY 292200Z AUTO VRB03KT 350V040 CAVOK 06/M00 Q1000 NOSIG'),
        Metar('LFLY','LFLY 292200Z AUTO VRB03KT 5200 06/M00 Q1000 NOSIG'),
        Metar('LFLY','LFLY 292200Z AUTO VRB03KT 350V040 5200NE 06/M00 Q1000 NOSIG'),
        Metar('LFLY','LFLY 292200Z AUTO VRB03KT 06/M00 Q1000 NOSIG'),
        Metar('LFLY','LFLY 292200Z AUTO VRB03KT 9950 06/M00 Q1000 NOSIG')

        results = [(9999,None),(9999,None),(5200,None),(5200,'NE'),None,(9950,None)]

        for k in range(len(metar)):
            self.assertEquals(metar[k].analyzeVisibility(),results[k])

unittest.main()