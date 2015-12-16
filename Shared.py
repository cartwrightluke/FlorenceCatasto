import urllib.request
import urllib.parse
import csv

def getCatastoData():

    catastoUrlBase = "http://cds.library.brown.edu/projects/catasto/newsearch/tabdel.php?dbname=Catasto&rawquery="
    sqlQuery = "SELECT location, trade, bocche, taxable FROM catasto ORDER BY trade LIMIT 100000"

    requestUrl = str(catastoUrlBase) + urllib.parse.quote(str(sqlQuery))
    response = urllib.request.urlopen(requestUrl)
    data = csv.reader(response.read().decode('utf: "8').splitlines(), delimiter='\t')

    next(data)
    tradesmen = {}
    tradeWealth = {}
    population = {}
    neighbourhoodList = getNeighbourhoods().keys()
    for neighbourhood in neighbourhoodList:
        tradesmen[neighbourhood] = {}
        tradeWealth[neighbourhood] = {}
        population[neighbourhood] = 0
        for trade in range(0,100):
            tradesmen[neighbourhood][trade] = 0
            tradeWealth[neighbourhood][trade] = 0

    for line in data:
        neighbourhood = int(line[0])
        trade = int(line[1]) % 100
        housePop = int(line[2])
        wealth = int(line[3])
        if(neighbourhood in neighbourhoodList):
            tradesmen[neighbourhood][trade] += 1
            population[neighbourhood] += housePop
            tradeWealth[neighbourhood][trade] += wealth

    return tradesmen, population, tradeWealth


def neighbourhoodNameToIndex(neighbourhood):
    if type(neighbourhood) is str:
        neighbourhood = getNeighbourhoods().index(neighbourhood)
    return neighbourhood

def getNeighbourhoods():
    neighbourhoodList = {
      11: "Scala",
      12: "Nicchio",
      13: "Ferza",
      14: "Drago",
      21: "Carro",
      22: "Bue",
      23: "Leon Nero",
      24: "Ruote",
      31: "Vipera",
      32: "Unicorno",
      33: "Leon Rosso",
      34: "Leon Bianco",
      41: "Leon D'Oro",
      42: "Drago",
      43: "Chiavi",
      44: "Vaio"
    }
    return neighbourhoodList

def getTradeName(tradeNumber):
    tradeNames = {  0: "No Trade",
                    1: "Peasant landlord",
                    2: "Peasant leasing land",
                    3: "Share-cropper",
                    4: "Agricultural laborer",
                    5: "Shepherd",
                    6: "Fisherman",
                    7: "Grocer",
                    8: "Knights, bishops, high ecclesiastics",
                    9: "Cotton Wholesaler",
                    10: "Sailor, Shipbuilder / servicer",
                    11: "Servant of private family",
                    12: "Servant of ecclesiastical institution",
                    13: "Employee of commune",
                    14: "Soldier",
                    15: "Employee of guild",
                    16: "Cook",
                    17: "Grave-digger).",
                    18: "Scribes, non-accredited notaries",
                    19: "Miscellaneous",
                    20: "Transporter of persons or goods",
                    21: "Judges and Notaries",
                    22: "Great merchant",
                    23: "Money changer",
                    24: "Wool manufacturer or merchant",
                    25: "Silk merchant, silk weaver",
                    26: "Seller of spices",
                    27: "Furrier",
                    28: "Butcher",
                    29: "Shoemaker",
                    30: "Smith",
                    31: "Linen cloth retailer",
                    32: "Medical doctor",
                    33: "Wine dealers",
                    34: "Innkeepers",
                    35: "Oil & merchants, Candlemakers",
                    36: "Tanner",
                    37: "Belt-maker",
                    38: "Maker of armor plating",
                    39: "Key and lock makers",
                    40: "Carpenters",
                    41: "Bakers",
                    42: "Miller",
                    43: "Cloth bleacher and dyers",
                    44: "Barber",
                    45: "Wool carder",
                    46: "Weaver of wool",
                    47: "Prepared food retailer",
                    48: "Coopers",
                    49: "Jewelers, Goldsmiths, Engravers, Sculptors",
                    50: "Urban labourer",
                    51: "Earthenware maker or dealer",
                    52: "Peddler",
                    53: "Raw wool cleaner",
                    54: "Stone worker",
                    55: "Leather horse good makers",
                    56: "Paper makers and dealers",
                    57: "Blacksmith",
                    58: "Doublet maker",
                    59: "Kiln makers and operators, glassblowers",
                    60: "Wool cloth finisher",
                    61: "Wool combers, carders and sorters",
                    62: "Wool shearer",
                    63: "Makers of purses and containers",
                    64: "Weavers of silk and linen",
                    65: "Slipper makers",
                    66: "Weigher, maker or seller of scales",
                    67: "Tailer",
                    68: "Makers of cloaks and dressing gowns",
                    69: "Town crier, auctioneer",
                    70: "Priest",
                    71: "Religious",
                    72: "Begger or Ward of the Church",
                    73: "Leather seller, saddler",
                    74: "Hat maker",
                    75: "Non-ferrous metal dealers or workers",
                    76: "Iron worker or dealer",
                    77: "Teacher or student of letters or abacus",
                    78: "Leather tanner or dresser",
                    79: "Broker, Middleman",
                    80: "Thread maker or Spinner",
                    81: "Type of leather worker",
                    82: "Religious lady sequestered at home",
                    83: "Musician or Jester",
                    84: "Washer of cloths",
                    85: "Cutter, cutler.",
                    86: "Mule driver, horse or ass dealer",
                    87: "Sewer of wool cloth, Embroider, Threader",
                    88: "Employee of mint",
                    89: "Rural noble",
                    90: "Jew",
                    91: "Wool stretcher",
                    92: "Mattress maker, bed maker",
                    93: "Wool manufacturer",
                    94: "Workers in weapons and armour",
                    95: "Artist, Painter or Miniature-maker",
                    96: "Grain dealers",
                    97: "Rope maker or Bag makers",
                    98: "Raw wool beaters and cleaners",
                    99: "Lawyer"
                    }
    return tradeNames[tradeNumber]