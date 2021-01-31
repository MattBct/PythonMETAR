# Python-METAR
Python library for aeronautical METAR (METeorological Aerodrome Report). 

## Installation

### PIP

You can use pip in order to install package.

```python
pip install -i https://test.pypi.org/simple/ Python-METAR-MattBOUCHET
```

### Source code

You can also download source code from https://github.com/MatthieuBOUCHET/Python-METAR

Decompress folder and copy `metar/metar.py` in your project folder.

## Usage

### Import

Use 

```python
from metar import *
```

or

```python
from metar import Metar,NOAAServError,ReadingMETARError,ReadFileError
```

### Declare a METAR

#### Retrieve a live METAR

```python
#example = Metar('OACICODE')
example = Metar('LFLY') #Lyon-Bron Airport (LFLY)
```

#### Declare a METAR with data

```python
#example = Metar('OACICODE','METARDATAS')
example = Metar('LFQN','METAR LFQN 201630Z 18005KT 4000 -SHRA SCT030 BKN050 18/12 Q1014 NOSIG=') #Saint-Omer Airfield (LFLY)
```

### Get informations

#### List of attributes analyzed

- `airport` (string): OACI code of METAR airport
- `data_date` (string): Date provided by NOAA server. None if text enter manually
- `metar` (string): Complete METAR message
- `changements` (string) : Changements
- `auto` (boolean): Define if a METAR isfrom an automatic station or not
- `date_time` (tuple): Tuple of date with day, hour & minutes
- `wind` (dictionary): Dictionary with wind information
- `rvr` (tuple): Tuple of dictionnaries with RVR information
- `weather` (dictionnary): Dictionnary of tuple with significant weather information

  \- cloud (tuple): Tuple of dictionnaries with cloud detected information

  \- temperatures (dictionnary): Dictionnary of integers with temperature and dewpoint information

  \- qnh (integer OR float): Information of QNH (integer if hPA, float if inHG)

  \- properties(dictionary): Dictionnary of METAR's attribute