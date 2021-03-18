import lxml, requests, pygal, re
import os, json, datetime


apikey = "O1RSZBGP6WA65EAI"

# THIS FUNCTION ASKS THE USER FOR THE VARIABLES FOR THE CODE TO RUN (TICKER , CHART TYPE, CHART TIME SERIES, START DAY , END DAY)
def userPrompt():
    tickerSymbol = input("Please Enter a Stock Ticker Symbol: ").upper();

    chartType = chartInput()

    chartTimeSeries = timeSeriesInput()

    startDate = dateInputStart()

    endDate = dateInputEnd(startDate)

    # THIS RETURNS A TUPLE TO THE getJsonPage() FUNCTION
    unit = (tickerSymbol, chartType, chartTimeSeries, startDate, endDate)
    return unit


def chartInput():
    while True:
        try:
            print("\nChart Types")
            print("------------")
            print("1. Bar")
            print("2. Line\n")
            chartType = int(input("Please Enter a Chart Type (1, 2): "));
            if chartType not in [1,2]:
                print("Enter a 1 or 2 for Chart Type")
            else:
                return chartType
        except ValueError:
             print("ERROR - Enter an Integer")

def timeSeriesInput():
    while True:
        try:
            print("\nSelect the Time Series of the chart you want to Generate")
            print("---------------------------------------------------------")
            print("1. Intraday")
            print("2. Daily")
            print("3. Weekly")
            print("4. Monthly\n")
            chartTimeSeries = int(input("Please Enter a Chart Time Series(1,2,3,4): "));
            if chartTimeSeries not in [1, 2, 3, 4]:
                print("Enter a 1, 2, 3, or 4 for Chart Time Series")
            else:
                return chartTimeSeries
        except ValueError:
             print("ERROR - Enter an Integer")


def dateNotInTheFuture(d):
    curDate = datetime.date.today().strftime('%Y-%m-%d')
    try:
        #FIRST WE CHECK TO SEE IF THE DATE IS IN THE PROPER FORMAT
        if validate(d):
            #NEXT WE CHECK IF THE INPUTTED DATE IS IN THE PAST
            if curDate > d:
                #IF THE INPUTTED DATE IS IN THE PAST, WE RETURN IT
                return d
            else:
                #IF THE INPUTTED DATE IS IN THE FUTURE, WE RAISE AN ERROR
                raise Exception
    except Exception:
        print("ERROR - Please Enter a Date That is In The Past - dateNotInTheFuture()")


def dateInputStart():
    while True:
        try:
            startDate = input("\nEnter the Start Date (YYYY-MM-DD): ")
            if dateNotInTheFuture(startDate):
                return startDate
        except ValueError:
            print("ERROR - Enter a Valid Date")


def dateInputEnd(startDate):
    while True:
        try:
            endDate = input("\nEnter the End Date (YYYY-MM-DD): ")
            if dateNotInTheFuture(endDate):
                if endDate < startDate:
                    print("The End Date Must be After The Start Date")
                else:
                    return endDate
        except ValueError:
            print("ERROR - Enter a Valid Date")



def validate(date_info):
    try:
        dateRegex = '^[0-9]{4}.(1[0-2]|0[1-9]).(3[01]|[12][0-9]|0[1-9])'
        if re.search(dateRegex, date_info):
            datetime.datetime.strptime(date_info, '%Y-%m-%d')
            return True
        else:
            raise ValueError
    except ValueError:
        print("ERROR - Incorrect data format: should be YYYY-MM-DD - Validate()")



# def makeGraph(data , chartType, chartTimeSeries, chartStartDate, chartEndDate):
#     ticker = data['Meta Data']['2. Symbol']
#     info = data['Meta Data']['1. Information']
#
#     opening = []
#     highs = []
#     lows = []
#     closing = []
#     dates = []
#
#     labels = list(data)[1]
#     dataIwant = data[labels]
#
#     for d in dataIwant:
#         date = str(d)
#         #IF THE USER WANTS A GRAPH OF 1 DAY
#         if chartStartDate == chartEndDate:
#             #CHECK IF THE TIME SERIES IS SET TO INTRADAY
#             if chartTimeSeries == 'TIME_SERIES_INTRADAY':
#                 #CHECK IF THE CHART START DATE IS IN THE STRING OF DATE1
#                 if str(chartStartDate) in date:
#                     #IF IT IS - SPLIT THEM AT THE SPACE AND ONLY TAKE THE TIME PORTION.
#                     dateSplit = date.split(' ')[1]
#                     dates.append(dateSplit)
#
#                     dataOpening = (dataIwant[d]["1. open"])
#                     opening.append(float(dataOpening))
#
#                     dataHigh = (dataIwant[d]["2. high"])
#                     highs.append(float(dataHigh))
#
#                     dataLow = (dataIwant[d]["3. low"])
#                     lows.append(float(dataLow))
#
#                     dataClosing = (dataIwant[d]["4. close"])
#                     closing.append(float(dataClosing))
#
#         #IF THE USER WANTS A GRAPH OF OVER 1 DAY
#         else:
#             if chartStartDate <= date <= chartEndDate:
#                 dates.append(date)
#
#                 dataOpening = (dataIwant[d]["1. open"])
#                 opening.append(float(dataOpening))
#
#                 dataHigh = (dataIwant[d]["2. high"])
#                 highs.append(float(dataHigh))
#
#                 dataLow = (dataIwant[d]["3. low"])
#                 lows.append(float(dataLow))
#
#                 dataClosing = (dataIwant[d]["4. close"])
#                 closing.append(float(dataClosing))
#
#     line_chart = chartType
#     line_chart.title = 'Stock Data for {}: {} to {} '.format(ticker, chartStartDate, chartEndDate)
#     line_chart.x_labels = dates
#     line_chart.add('Opening', opening)
#     line_chart.add('High', highs)
#     line_chart.add('Low', lows)
#     line_chart.add('Closing', closing)
#     if dates == []:
#         print("There Was Not Data Available For Your Input")
#     else:
#         line_chart.render_in_browser()


def createData(jsonData, index, opening, highs, lows, closing, dates, mode):
    if mode == 1:
        timeonly = str(index).split(' ')[1]
        dates.append(timeonly)
    else:
        dates.append(index)

    dataOpening = (jsonData[index]["1. open"])
    opening.append(float(dataOpening))

    dataHigh = (jsonData[index]["2. high"])
    highs.append(float(dataHigh))

    dataLow = (jsonData[index]["3. low"])
    lows.append(float(dataLow))

    dataClosing = (jsonData[index]["4. close"])
    closing.append(float(dataClosing))


def reverseLists(opening, highs, lows, closing, dates):
    opening = opening.reverse()
    highs = highs.reverse()
    lows = lows.reverse()
    closing = closing.reverse()
    dates = dates.reverse()

def makeGraph(data , chartType, chartTimeSeries, chartStartDate, chartEndDate):
    ticker = data['Meta Data']['2. Symbol']
    info = data['Meta Data']['1. Information']

    opening = []
    highs = []
    lows = []
    closing = []
    dates = []

    labels = list(data)[1]
    dataIwant = data[labels]

    for d in dataIwant:
        date = str(d)
        #IF THE USER WANTS A GRAPH OF 1 DAY
        if chartStartDate == chartEndDate:
            #CHECK IF THE TIME SERIES IS SET TO INTRADAY
            if chartTimeSeries == 'TIME_SERIES_INTRADAY':
                #CHECK IF THE CHART START DATE IS IN THE STRING OF DATE1
                if str(chartStartDate) in date:
                    #IF IT IS - SPLIT THEM AT THE SPACE AND ONLY TAKE THE TIME PORTION.
                    createData(dataIwant, date, opening, highs, lows, closing, dates, 1)


        #IF THE USER WANTS A GRAPH OF OVER 1 DAY
        else:
            if chartStartDate <= date <= chartEndDate:
                createData(dataIwant, date, opening, highs, lows, closing, dates, 0)


    line_chart = chartType
    line_chart.title = 'Stock Data for {}: {} to {} '.format(ticker, chartStartDate, chartEndDate)
    reverseLists(opening, highs, lows, closing, dates)
    line_chart.x_labels = dates
    line_chart.add('Opening', opening)
    line_chart.add('High', highs)
    line_chart.add('Low', lows)
    line_chart.add('Closing', closing)
    if dates == []:
        print("There Was Not Data Available For Your Input")
    else:
        line_chart.render_in_browser()


#THE PURPOSE OF THE getJsonPage FUNCTION IS TO RUN THE PROGRAM
def getJsonPage():
    # FIRST WE CALL userPrompt() WHICH RETURNS THE Symbol, chartType, chartTimeSeries , chartStartDate, chartEndDate
    info = userPrompt()

    # THEN WE ASSIGN VARIABLES BY THE TUPLE INDEX
    symbol = info[0]

    #  THOSE VARIABLES ARE BROKEN DOWN INTO API ENDPOINT COMPONENTS E.G (TIME_SERIES_INTRADAY,TIME_SERIES_DAILY) OR THEIR RESPECTIVE DATES TO BE LOOKED FOR WITHIN THE API RESULTS
    chartType = info[1]
    if chartType == 1: chartType = pygal.Bar(x_label_rotation=-45, x_labels_major_every=3, show_minor_x_labels=False)
    elif chartType == 2: chartType = pygal.Line(x_label_rotation=-45, x_labels_major_every=3, show_minor_x_labels=False)

    chartTimeSeries = info[2]
    intraDayInfo = ""
    if chartTimeSeries == 1:
        chartTimeSeries = "TIME_SERIES_INTRADAY"
        #WE HAVE TO SET THE INTERVAL IF THE SELECTED INPUT IS INTRADAY
        intraDayInfo = "&interval=60min"
    elif chartTimeSeries == 2: chartTimeSeries = "TIME_SERIES_DAILY"
    elif chartTimeSeries == 3: chartTimeSeries = "TIME_SERIES_WEEKLY"
    elif chartTimeSeries == 4: chartTimeSeries = "TIME_SERIES_MONTHLY"

    chartStartDate = info[3]
    chartEndDate = info[4]

    # AFTER THE VARIABLES ARE ASSIGNED WE BUILD THE LINK AND EXECUTE THE GET REQUEST. -> WE PRINT THE BUILT URL TO THE CONSOLE FOR DEBUGGING PURPOSES
    req = requests.get("https://www.alphavantage.co/query?function={}&symbol={}{}&apikey={}".format(chartTimeSeries, symbol, intraDayInfo, apikey))
    print(req.url)

    # WE LOAD THE REQUEST RESPONSE INTO A VARIABLE CALLED DATA AND USE THE JSON() FUNCTION TO PARSE THE TEXT.
    data = req.json()

    # FINALLY, WE CHECK IF THERE WAS A STRING OF 'INVALID API CALL' IN THE RESPONSE AND IF THERE IS WE PRINT AN ERROR MESSAGE INSTEAD OF BUILDING THE GRAPH IN BROWSER
    if 'Invalid API call' not in req.text:
        makeGraph(data, chartType, chartTimeSeries, chartStartDate, chartEndDate)
    else:
        print("The Ticker You Entered is Not in The API\n")


def main():
    keepGoing = True
    while keepGoing:
        getJsonPage()
        flag = input("Would you like to continue? Enter (Y/N)")
        if flag.lower() != "y":
            keepGoing = False

if __name__ == '__main__':
    main()
