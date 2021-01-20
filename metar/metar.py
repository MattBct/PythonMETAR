"""
Class METAR
Author: Matthieu BOUCHET

5cfd588b1a5871105cad98a099c67d44562fb2524bf8b4d00a7e3f9baca33ee2

For documentation, you can visit : https://www.link.url
and read the ReadMe
"""

import urllib.request as url
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context


class Metar:
    """Class METAR represents a METeorogical Aerodrome Report.

    Each attribute represent each information contained in
    METAR (International METAR Code). Informations are recovered from
    text message. Units returned are units used in text.
    This class can be imported in programm.

    More informations about METAR here: 
    - https://en.wikipedia.org/wiki/METAR/
    - https://www.skybrary.aero/index.php/Meteorological_Terminal_Air_Report_(METAR)/

    Args:
    -----
    code (string): OACI code of airport searched

    Attributes:
    -----------
    - airport (string): OACI code of METAR airport
    - data_date (string): Date provided by NOAA server. None if text enter manually
    - metar (string): Complete METAR message
    - 
    """

    def __init__(self, code, text=None):
        """Constructor of class

        Args:
        -----
            code (string): OACI code of airport searched
        """
        self.airport = code

        if text is None:
            text = self.text_recover()
            self.data_date = text[0]
            self.metar = text[1]

        else:
            self.data_date = None
            self.metar = text
        
        self.metarWithoutChangements = self.metar
        self.changements = self.analyzeChangements() #delcare self.metarAnalysis
        self.auto = self.analyzeAuto()
        self.date_time = self.analyzeDateTime()
        self.wind = self.analyzeWind()
        self.rvr = self.analyzeRVR()

        self.properties = {
            'dateTime': self.date_time,
            'metar':self.metar,
            'auto':self.auto,
            'wind':self.wind,
            'rvr':self.rvr,


            'changements':self.changements

        }

    def __str__(self):
        """Overload __str__
        """
        return self.metar

    def text_recover(self):
        """`text_recover()` method recover text file from NOAA
        weather FTP server (https://tgftp.nws.noaa.gov/data/observations/metar/stations/).

        Recovers text file with `url.urlretrieve()` function.
        Read the file with `readlines()` method. This method return a list
        of lines ([0] = Datetime ; [1] = METAR).
        A `for` loop browses list to remove line break character.
        Return a list with datetime index 0 and METAR index 1.


        Require:
        --------
        `NOAAServError(Exception)` from metar_error \n
        `ulrlib.request` from built-in Pyhon modules \n
        `re` from built-in Python modules \n

        Returns:
        --------
            datas (tuple): List recovered from text file ([0] = Datetime ; [1] = METAR).

        Exception raised:
        -------
            - NOAAServError
            - ReadFileError
        """

        try:
            request = url.urlretrieve(
                "https://tgftp.nws.noaa.gov/data/observations/metar/stations/{}.TXT".format(self.airport))
        except url.HTTPError as err:
            if(err.code == 404):
                raise NOAAServError(self.airport, 404)
            else:
                raise NOAAServError(self.airport)

        except:
            raise NOAAServError(self.airport)

        try:
            file_txt = open(request[0], 'r')

        except:
            raise ReadFileError

        datas = file_txt.readlines()  # List : [0] = Datetime ; [1] = METAR

        # Remove '\n' from string
        for i in range(len(datas)):
            datas[i] = re.sub("\n", '', datas[i])

        file_txt.close()
        return datas[0], datas[1]

    def analyzeChangements(self):
        """Method analysis and erase changements portions (create metarWithoutChangements variable)

        Returns:
            (dict): Dictionnary of changements (TEMPO & BECOMING). Return None if NOSIG
        """

        def changementsRecuperation(marker):
            regex = marker+'.+'
            search = re.search(regex,self.metar)
            if search is not None:
                search = search.group()
                portion = re.sub(marker + ' ','',search)
                self.metarWithoutChangements = re.sub(regex,'',self.metarWithoutChangements)
            else:
                return None
            
            return portion
                

        ##NOSIG##
        regex_nosig = r'NOSIG'
        search_nosig = re.search(regex_nosig,self.metar)
        if search_nosig is not None:
            self.metarWithoutChangements = re.sub(regex_nosig,'',self.metar)
            return None

        ##TEMPO##
        tempo = changementsRecuperation('TEMPO')

        ##BECMG##
        becoming = changementsRecuperation('BECMG')

        ##GRADU##
        gradu = changementsRecuperation('GRADU')

        ##RAPID##
        rapid = changementsRecuperation('RAPID')

        ##INTER##
        inter = changementsRecuperation('INTER')

        ##TEND##
        tend = changementsRecuperation('TEND')

        changements = {
            'TEMPO':tempo,
            'BECMG':becoming,
            'GRADU':gradu,
            'RAPID':rapid,
            'INTER':inter,
            'TEND':tend
        }

        return changements

    def analyzeDateTime(self):
        """Method parse METAR and return datetime portion

        Returns:
            date_time (tuple): Tuple of strings (Day,Hour,Minute) in UTC.
            Ex: ("29","19","00") => 29th day of month, 19:00 UTC
            This is METAR date time.

            None (NoneType): Return None if no date time found
        """
        date_time = re.findall(r'\d{6}Z', self.metar)
        if(len(date_time) == 0 or len(date_time) > 1):  # No match
            return None

        date_time = date_time[0]
        date_time = re.sub(r'Z', '', date_time)
        date_time = (date_time[:2], date_time[2:4], date_time[4:])

        return date_time

    def analyzeAuto(self):
        """Method verify if a METAR comes form an automatic station.
        If it is a METAR AUTO, return True.

        Returns:
        --------
            boolean: True if auto, False if not auto
        """

        search = re.search(r'AUTO', self.metar)
        if search is None:
            return False

        return True

    def analyzeWind(self):
        """Method parse and analyze wind datas from METAR message and
        returns a dictionnary with wind informations.
        Support Knots (KT) and Meter Per Second (MPS) units.
        Units are not informations returned by method.
        If `analyzeWind()` can't decode wind information (in case of unavaibility
        indicated by ///////KT), method return None.

        Returns:
            wind_tot (dict): Dictionnary with wind informations.
            Keys:
                - direction (integer), direction of wind
                - direction (string), "VRB" for variable
                - speed (integer), speed of wind
                - gust_speed (integer or None), speed of gust, None if no gust
                - variation(tuple), variation of wind (tuple of integer), None if no variation
            
            None (NoneType): None if method can't decode wind informations.
        """
        search = None

        regex_list_kt = [r'\d{5}KT', r'\d{5}G\d{2}KT', r'VRB\d{2}KT']
        # [0] Normal (33005KT) [1] Gust (33010G25KT) [2] Variable direction (VRB03KT)
        regex_list_mps = [r'\d{5}MPS', r'\d{5}G\d{2}MPS', r'VRB\d{2}MPS']
        # Meters per second
        
        
        i = 0
        end = len(regex_list_kt)

        while search is None and i < end:
            search = re.search(regex_list_kt[i], self.metarWithoutChangements)
            i += 1

        if search is None: # Knot verification failed, MPS verification
            i = 0
            end = len(regex_list_mps)

            while search is None and i < end:
                search = re.search(regex_list_mps[i], self.metarWithoutChangements)
                i += 1
            
            if search is None:
                return None


        wind_tot = search.group()
        direction = wind_tot[:3]

        if direction != 'VRB':
            direction = int(direction)
        
        speed = wind_tot[3:5]
        speed = int(speed)

        if 'G' in wind_tot: #Gust
            gust_speed = int(wind_tot[6:8])
        else:
            gust_speed = None

        ##Variations##
        regex = r'\d{3}V\d{3}'
        search = re.search(regex,self.metarWithoutChangements)

        

        if search is not None:
            variation = search.group()
            variation = variation.split('V')
            variation = [int(value) for value in variation]
            variation = tuple(variation)
        else:
            variation = None
        
        wind_infos = {
            'direction':direction,
            'speed':speed,
            'gust':gust_speed,
            'variation':variation
        }

        return wind_infos

    def analyzeVisibility(self):
        """Method analyzes the Visibility (distance, direction).
        Return a tuple with meter & direction
        If CAVOK, return (9999,'')
        Else, return (distance,direction)

        Returns:
            (tuple): A tuple as (distance, direction). E.g -> (9999,'N'),(5000,None)
            Distance (tuple[0] is Integer) & Direction (tuple[1] is String or None if no direction)
        """
        verify = self.verifyWindAttribute('variation')
        if not verify:
            regex = r'KT \d{4}|KT CAVOK|KT \d{4}[A-Z]+'
        else:
            regex = r'\d{3}V\d{3} \d{4}|\d{3}V\d{3} \d{4}|\d{3}V\d{3} \d{4}[A-Z]+'

        search = re.search(regex,self.metarWithoutChangements)
        if search is None:
            return None
        
        visibility = search.group()
        #print(visibility)

        if not verify:
            visibility = re.sub(r'KT ','',visibility)
        else:
            visibility = re.sub(r'\d{3}V\d{3} ','',visibility)

        if visibility == 'CAVOK':
            return 9999,None

        return (int(visibility[:4]),visibility[4:])

    def analyzeRVR(self):
        """Method parses and recovers RVR

        Returns:
            (tuple): Tuple of dictionnries : {
                'runway':runway (string)
                'visibility':visibility (integer)
            }

            (NoneType): If no RVR mentionned
        """
        ##PORTION METAR RECOVERING##
        regex_runway = r'R\d{2}[LCR]*'
        regex_rvr = r'[MP]*\d{4}'
        regex = regex_runway + '/' + regex_rvr
        
        search = re.findall(regex,self.metarWithoutChangements)
        if search == []:
            return None

        ##DATAS RECOVERING##
        rvr = []
        for k in search:
            search_runway = re.search(regex_runway,k)
            runway = search_runway.group()
            runway = runway[1:]

            search_visibility = re.search(r'\d{4}',k)
            visibility = int(search_visibility.group())

            rvr.append(
                {
                    'runway':runway,
                    'visibility':visibility
                }
            )
        
        return tuple(rvr)
               
    def verifyWindAttribute(self, key):
        """Verify if a key exists (gust or variation)

        Returns:
            boolean: False => No key, True => Key attributed
        """
        wind = self.analyzeWind()
        if wind is None:
            return False
        
        try:
            if wind[key] is None:
                return False
            
            return True

        except KeyError:
            return False

    def getMetar(self, display=False):
        """Getter metar attribute

        Args:
            display (bool, optional): If true, print METAR. Defaults to False.

        Returns:
            self.metar (string): Entire METAR
        """
        if display:
            print(self)

        return self.metar

    def getDateTime(self, display=False):
        """Getter date_time attribute

        Args:
            display (bool, optional): If true, print date & time. Defaults to False.

        Returns:
            self.date_time (dict): DateTime
        """
        if display:
            print(self.date_time)

        return self.date_time

    def getDataDate(self,display=False):
        """Getter data_date attribute

        Args:
            display (bool, optional): If true, print attribute. Defaults to False.

        Returns:
            self.data_date (string): DateTime
        """
        if display:
            print(self.data_date)

        return self.data_date

    def getAuto(self,display=False):
        """Getter auto attribute

        Args:
            display (bool, optional): If true, print attribute. Defaults to False.

        Returns:
            self.auto (boolean): METAR AUTO
        """
        if display:
            print(self.auto)

        return self.auto

    def getWind(self,display=False):
        """Getter wind attribute

        Args:
            display (bool, optional): If true, print attribute. Defaults to False.

        Returns:
            self.wind (dict): Wind information
        """
        if display:
            print(self.wind)

        return self.wind

    def getRVR(self,display=False):
        """Getter changements attribute

        Args:
            display (bool, optional): If true, print attribute. Defaults to False.

        Returns:
            self.rvr (dict): Runway Visual Range
        """
        if display:
            print(self.rvr)

        return self.rvr

    def getChangements(self,display=False):
        """Getter changements attribute

        Args:
            display (bool, optional): If true, print attribute. Defaults to False.

        Returns:
            self.changements (dict): Changements
        """
        if display:
            print(self.changements)

        return self.changements

    def getProperties(self,display=False):
        """Getter changements attribute

        Args:
            display (bool, optional): If true, print attribute. Defaults to False.

        Returns:
            self.changements (dict): Properties
        """
        if display:
            print(self.properties)

        return self.properties

## ERRORS ##
class NOAAServError(Exception):
    """`NOAAServError` is an exception based on Exception basic class
    This exception is raised in methods of `Metar` class if an error occured
    during connection with servor (HTTP error 404, or another)
    """

    def __init__(self, airport, code=None):
        """Constructor

        Args:
        -----
            airport (string): OACI Code of airport (airport attribute of `Metar` class)
            code (integer, optional): Error code, code possible :
            - 404 

            Defaults to None.
        """
        if code == 404:
            self.message = "No METAR found from {0}".format(airport)
        else:
            self.message = ("Problem during connection with "
                            "NOAA Weather")

        super().__init__(self.message)

class ReadingMETARError(Exception):
    """Errror raised during reading of one data from METAR
    """
    def __init__(self, data):
        """Constructor

        Args:
            data (STRING): Parameter readen during raising
            E.g->'Visibility','Wind',...
        """
        self.message = 'Error during reading of {0} data from METAR'.format(data)
        super().__init__(self.message)

class ReadFileError(Exception):
    """`ReadFileError` is an exception based on Exception basic class
    This exception is raised in methods of `Metar` class if an error occured
    during reading of file downloaded in temp file by `readlines()` method.
    """

    def __init__(self):
        """Constructor
        """
        self.message = ("Datas have been downloaded from NOAA Weather"
                        "but can't be read by system")

        super().__init__(self.message)


a = Metar('LFPO', 'LFPO 041300Z 27010G25KT 320V040 1200 R26/0400 R26R/0450 +RASH BKN040TCU 17/15 Q1015 RETS M2 26791299')
b = Metar('LFLY', 'LFLY 292200Z AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG')
c = Metar('LFPG')
d = Metar('LFLY','LFLY 192100Z AUTO 17012KT CAVOK 06/M02 Q1017 BECMG 19020G35KT')
e = Metar('LFPG','LFPG 292200Z AUTO VRB03KT CAVOK 06/M00 Q1000 NOSIG')
pass
