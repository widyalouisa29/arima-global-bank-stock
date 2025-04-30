import pandas as pd

bmri = pd.read_csv("BMRI.csv")
hsbc = pd.read_csv("HSBC.csv")
dbs  = pd.read_csv("DBS.csv")
c    = pd.read_csv("C.csv")
for data in [bmri, hsbc, dbs, c]:
    data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
def enrich(data, saham):
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    for column in ['Open', 'High', 'Low', 'Close',  'Volume']:
        data[column] = pd.to_numeric(data[column], errors='coerce')
    data.dropna(subset=['Date'], inplace=True)
    
    data['Adj Close'] = data['Close']  # override
    data['Change'] = data['Close'].diff()
    data['Ratio(%)'] = (data['Change'] / data['Close'].shift(1)) * 100
    data['Value(T)'] = data['Close'] * data['Volume']
    data['Saham'] = saham
    data.dropna(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%d/%m/%Y')
    return data

bmriClean = enrich(bmri, "BMRI")
hsbcClean = enrich(hsbc, "HSBC")
dbsClean  = enrich(dbs, "DBS")
cClean    = enrich(c, "C")

compiled = pd.concat([bmriClean, hsbcClean, dbsClean, cClean], ignore_index=True)
compiled.to_csv("CombinedClean2.csv", index=False)
