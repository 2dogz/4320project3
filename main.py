import lxml, requests, pygal
import os, json, datetime

apikey = "O1RSZBGP6WA65EAI"

# THIS FUNCTION ASKS THE USER FOR THE VARIABLES FOR THE CODE TO RUN (TICKER , CHART TYPE, CHART TIME SERIES, START DAY , END DAY)
def userPrompt():
    tickerSymbol = input("Please Enter a Stock Ticker Symbol: ").upper();

    chartType = chartInput()

    chartTimeSeries = timeSeriesInput()

    startDate = dateInputStart()

    endDate = dateInputEnd(startDate)

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

def dateInputStart():
    while True:
        try:
            startDate = input("\nEnter the Start Date (YYYY-MM-DD): ")
            validate(startDate)
            return startDate
        except ValueError:
            print("ERROR - Enter a Valid Date")

def dateInputEnd(startDate):
    while True:
        try:
            endDate = input("\nEnter the End Date (YYYY-MM-DD): ")
            validate(endDate)
            if endDate < startDate:
                print("The End Date Must be After The Start Date")
            else:
                return endDate
        except ValueError:
            print("ERROR - Enter a Valid Date")

def validate(date_info):
    datetime.datetime.strptime(date_info, '%Y-%m-%d')

def makeGraph(data , chartType, chartStartDate, chartEndDate):
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
        if chartStartDate == chartEndDate:
            if str(chartStartDate) in date:
                dateSplit = date.split(' ')[1]
                dates.append(dateSplit)

                dataOpening = (dataIwant[d]["1. open"])
                opening.append(float(dataOpening))

                dataHigh = (dataIwant[d]["2. high"])
                highs.append(float(dataHigh))

                dataLow = (dataIwant[d]["3. low"])
                lows.append(float(dataLow))

                dataClosing = (dataIwant[d]["4. close"])
                closing.append(float(dataClosing))
        else:
            if chartStartDate <= date <= chartEndDate:
                dates.append(date)

                dataOpening = (dataIwant[d]["1. open"])
                opening.append(float(dataOpening))

                dataHigh = (dataIwant[d]["2. high"])
                highs.append(float(dataHigh))

                dataLow = (dataIwant[d]["3. low"])
                lows.append(float(dataLow))

                dataClosing = (dataIwant[d]["4. close"])
                closing.append(float(dataClosing))

    line_chart = chartType
    line_chart.title = 'Stock Data for {}: {} to {} '.format(ticker, chartStartDate, chartEndDate)
    line_chart.x_labels = dates
    line_chart.add('Opening', opening)
    line_chart.add('High', highs)
    line_chart.add('Low', lows)
    line_chart.add('Closing', closing)
    line_chart.render_in_browser()

def getJsonPage():
    info = userPrompt()

    symbol = info[0]

    chartType = info[1]
    if chartType == 1: chartType = pygal.Bar(x_label_rotation=-20, x_labels_major_every=3, show_minor_x_labels=False)
    elif chartType == 2: chartType = pygal.Line(x_label_rotation=-45, x_labels_major_every=3, show_minor_x_labels=False)

    chartTimeSeries = info[2]
    intraDayInfo = ""
    if chartTimeSeries == 1:
        chartTimeSeries = "TIME_SERIES_INTRADAY"
        intraDayInfo = "&interval=60min"
    elif chartTimeSeries == 2: chartTimeSeries = "TIME_SERIES_DAILY"
    elif chartTimeSeries == 3: chartTimeSeries = "TIME_SERIES_WEEKLY"
    elif chartTimeSeries == 4: chartTimeSeries = "TIME_SERIES_MONTHLY"

    chartStartDate = info[3]
    chartEndDate = info[4]

    req = requests.get("https://www.alphavantage.co/query?function={}&symbol={}{}&apikey={}".format(chartTimeSeries, symbol, intraDayInfo, apikey))
    print(req.url)
    data = req.json()
    if 'Invalid API call' not in req.text:
        makeGraph(data, chartType, chartStartDate, chartEndDate)
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
