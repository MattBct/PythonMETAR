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
            'gust_speed':None,
            'variation':None
        })
        
        metar = Metar('LFLY','LFLY 292200Z AUTO 22005KT CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.analyzeWind(),{
            'direction':220,
            'speed':5,
            'gust_speed':None,
            'variation':None
        })
        
        metar = Metar('LFLY','LFLY 292200Z AUTO 22010G25KT 040V210 CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.analyzeWind(),{
            'direction':220,
            'speed':10,
            'gust_speed':25,
            'variation':(40,210)
        })
        
        metar = Metar('LFLY','LFLY 292200Z AUTO /////KT CAVOK 06/M00 Q1000 NOSIG')
        self.assertEquals(metar.analyzeWind(),None)

unittest.main()