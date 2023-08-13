import yfinance as yf
import pandas as pd
import math

class PointAndFigure:
    def __init__(self, step, ticker, startDate, endDate=None):
        self.step = step
        self.ticker = ticker
        self.startDate = startDate
        self.endDate = None
        self.instrument = yf.Ticker(ticker)
        self.months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C']

    def floor_to_nearest(self, price):
        return round(math.floor(price / self.step) * self.step, 2)
    
    def get_month_index(self, date):
        month = str(date).split("-")[1]
        match month:
                case '01':
                    return 0
                case '02':
                    return 1
                case '03':
                    return 2
                case '04':
                    return 3
                case '05':
                    return 4
                case '06':
                    return 5
                case '07':
                    return 6
                case '08':
                    return 7
                case '09':
                    return 8
                case '10':
                    return 9
                case '11':
                    return 10
                case '12':
                    return 11

    def chart(self):
        hist = self.instrument.history(start=self.startDate, end=self.endDate)
        df = pd.DataFrame({'Date':hist['Close'].index, 'Close': hist['Close'].values})

        close_prices = df['Close']
        dates = df['Date']

        current = self.floor_to_nearest(close_prices[0])
        min_price = self.floor_to_nearest(min(close_prices))
        max_price = self.floor_to_nearest(max(close_prices))

        height = round((max_price-min_price)/self.step)+1
        width = 100
        grid = [[' ' for _ in range(width)] for _ in range(height)]

        #set starting position to price of the start date
        row = round((max_price-current)/self.step)
        col = 0

        #these values are later used when chart is printed
        startRow = row
        b = current
        

        th = 3 #threshold for changing trend direction
        monthIndex = self.get_month_index(dates[0]) #get starting month
        grid[row][col] = self.months[monthIndex] #set the mark of starting position to starting month
        trend = 0 #trend is zero at the beginning

        #calculate chart for rest of the prices
        dateIndex = 1
        newMonth = False
        for close_price in close_prices[1:]:
            oldMonthIndex = monthIndex
            monthIndex = self.get_month_index(dates[dateIndex])

            if oldMonthIndex != monthIndex:
                    newMonth = True

            price_rounded = self.floor_to_nearest(close_price)
            if trend == 1:
                if price_rounded > current:
                    for i in range(0, round((price_rounded-current)/self.step)):
                        if newMonth:
                            grid[row-i-1][col] = self.months[monthIndex]
                            newMonth = False
                        else:
                            grid[row-i-1][col] = 'X'

                    row -= round((price_rounded-current)/self.step)
                    current = price_rounded

                elif price_rounded <= current - th*self.step:
                    col += 1
                    for i in range(0, round((current-price_rounded)/self.step)):
                        if newMonth:
                            grid[row+i+1][col] = self.months[monthIndex]
                            newMonth = False
                        else:
                            grid[row+i+1][col] = 'O'

                    row -= round((price_rounded-current)/self.step)
                    current = price_rounded
                    trend = -1

            elif trend == -1:
                if price_rounded < current:
                    for i in range(0, round((current-price_rounded)/self.step)):
                        if newMonth:
                            grid[row+i+1][col] = self.months[monthIndex]
                            newMonth = False
                        else:
                            grid[row+i+1][col] = 'O'

                    row -= round((price_rounded-current)/self.step)
                    current = price_rounded

                elif price_rounded >= current + th*self.step:
                    col += 1
                    for i in range(0, round((price_rounded-current)/self.step)):
                        if newMonth:
                            grid[row-i-1][col] = self.months[monthIndex]
                            newMonth = False
                        else:
                            grid[row-i-1][col] = 'X'

                    row -= round((price_rounded-current)/self.step)
                    current = price_rounded
                    trend = 1
            else:
                if price_rounded >= current + th*self.step:
                    for i in range(0, round((price_rounded-current)/self.step)):
                        if newMonth:
                            grid[row-i-1][col] = self.months[monthIndex]
                            newMonth = False
                        else:
                            grid[row-i-1][col] = 'X'

                    row -= round((price_rounded-current)/self.step)
                    current = price_rounded
                    trend = 1

                elif price_rounded <= current - th*self.step:
                    col += 1
                    for i in range(0, round((current-price_rounded)/self.step)):
                        if newMonth:
                            grid[row+i+1][col] = self.months[monthIndex]
                            newMonth = False
                        else:
                            grid[row+i+1][col] = 'O'

                    row -= round((price_rounded-current)/self.step)
                    current = price_rounded
                    trend = -1
            dateIndex += 1

        #print the chart
        chart = ""
        for i in range(height):
            chart += "{:>4.1f} ".format((startRow-i)*self.step+b)
            for j in range(width):
                chart += grid[i][j]
            chart += "\n"
        return chart
