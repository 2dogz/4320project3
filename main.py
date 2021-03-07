import lxml, requests, pygal
import os, json, datetime

apikey = "O1RSZBGP6WA65EAI"

def userPrompt():
    tickerSymbol = input("Please Enter a Stock Ticker Symbol: ");

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
             print("ERROR - Please Enter an Integer")

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
             print("ERROR - Please Enter an Integer")

def dateInputStart():
    while True:
        try:
            startDate = input("\nEnter the Start Date (YYYY-MM-DD): ")
            validate(startDate)
            return startDate
        except ValueError:
            print("Please Enter Valid Date")

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
            print("please enter valid date")

def validate(date_info):
    try:
        datetime.datetime.strptime(date_info, '%Y-%m-%d')
    except ValueError:
        raise ValueError("ERROR - Incorrect data format: should be YYYY-MM-DD")

def make_graph(data , chartType):
    ticker = data['Meta Data']['2. Symbol']
    opening = []
    highs = []
    lows = []
    closing = []
    dates = []
    labels = list(data)[1]
    dataIwant = data[labels]
    for d in dataIwant:
        date = d
        dates.append(date)

        dataOpening = (dataIwant[d]["1. open"])
        opening.append(float(dataOpening))

        dataHigh = (dataIwant[d]["2. high"])
        highs.append(float(dataHigh))

        dataLow = (dataIwant[d]["3. low"])
        lows.append(float(dataHigh))

        dataClosing = (dataIwant[d]["4. close"])
        closing.append(float(dataClosing))

    line_chart = chartType
    line_chart.title = 'Stock Data for {} '.format(ticker)
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
    if chartType == 1: chartType = pygal.Bar()
    elif chartType == 2: chartType = pygal.Line()

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
    make_graph(data, chartType)


def main():
    keepGoing = True
    while keepGoing:
        getJsonPage()
        flag = input("Would you like to continue? Enter (Y/N)")
        if flag.lower() != "y":
            keepGoing = False

if __name__ == '__main__':
    main()
