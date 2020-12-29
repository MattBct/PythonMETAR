"""
Class METAR
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

        self.auto = self.analyzeAuto()
        self.date_time = self.analyzeDateTime()

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

    def analyzeDateTime(self):
        """Method parse METAR and return datetime portion

        Returns:
            date_time (string): String in the form of "DDHHMMZ".
            This is METAR date time.

            False (boolean): Return False if no date time found
        """
        date_time = re.findall(r'\d{6}Z', self.metar)
        if(len(date_time) == 0):  # No match
            return False

        return date_time

    def analyzeAuto(self):
        """Method verify if a METAR comes form an automatic station.
        If it is a METAR AUTO, return True and erase AUTO from `self.metar`.
        If it's not a METAR AUTO, return False and no treatment done.

        Returns:
        --------
            boolean: True if auto, False if not auto
        """

        if("AUTO") in self.metar:
            re.sub('AUTO ', '', self.metar)  # Space after AUTO
            return True

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
        """Getter datetime attribute

        Args:
            display (bool, optional): If true, print date & time. Defaults to False.

        Returns:
            self.datetime (string): DateTime
        """
        if display:
            print(self.datetime)

        return self.datetime


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


pass
