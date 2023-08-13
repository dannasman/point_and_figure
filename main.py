import sys
from point_and_figure import PointAndFigure 

def main():
    try:
        ticker = sys.argv[1]
    except:
        print("invalid or missing ticker")
    try:
        step = float(sys.argv[2])
    except:
        print("invalid or missing step value")
    try:
        startDate = sys.argv[3]
    except:
        print("invalid or missing start date")
    try:
        model = PointAndFigure(step, ticker, startDate)
        print(model.chart())
    except:
        print("failed to create the chart")

main()