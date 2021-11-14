import requests
import sqlite3
import sys

def main(filetype,filename):
    api = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'
    r = requests.get(api)
    json_output = r.json()
    time_series = json_output["Time Series (Daily)"]

    
    Totalopen = 0
    Totalclose = 0
    Totalhigh = 0
    Totallow = 0
    for date, values in time_series.items():
        open = values["1. open"]
        close = values["4. close"]
        high = values["2. high"]
        low = values["3. low"]

        Totalopen += float(open)
        Totalclose += float(close)
        Totalhigh += float(high)
        Totallow += float(low)
        # print(open, close, high, low)
    
    if(filetype == "csv"):
        print(filename)
        with open(filename, "w") as f:
            print("Open,High,Low,Close", file=f)
            print(Totalopen, Totalhigh, Totallow, Totalclose, file=f)
    if(filetype == "db"):
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS stock (open REAL, close REAL, high REAL, low REAL)")
        c.execute("INSERT INTO stock VALUES (?,?,?,?)", (Totalopen/len(time_series), Totalclose/len(time_series), Totalhigh/len(time_series), Totallow/len(time_series)))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    arguments = sys.argv
    # print(len(arguments))
    if len(arguments) == 1:
        main()
    else:
        if arguments[1] == '--help':
            print('Options:')
            print('--symbol TEXT                   [default: IBM]')
            print('--csv / --no-csv                [default: True]')
            print('--csvfile TEXT                  [default: ]')
            print('--database / --no-database      [default: False]')
            print('--databasefile TEXT             [default: ]')
            print('--xlsx / --no-xlsx              [default: False]')
            print('--xlsxfile TEXT                 [default: ]')
            print('--help                          [default: False]')
        elif arguments[1] == '--csv':
            if arguments[2] == '--csvfile':
                if len(arguments) == 4:
                    main('csv',arguments[3])
                else:
                    print('Please enter a filename')
            else:
                print("Please provide arguements, refer help --help flag")
        elif arguments[1] == '--database':
            if arguments[2] == '--databasefile':
                if len(arguments) == 4:
                    main('db',arguments[3])
                else:
                    print('Please enter a filename')
            else:
                print("Please provide arguements, refer help --help flag")
    # main()