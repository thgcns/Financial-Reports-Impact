import pandas as pd
import os

name_prices = {
    'azul': 'AZUL4.SA',
    'BB': 'BBAS3.SA',
    'bradesco': 'BBDC4.SA',
    'brf': 'BRFS3.SA',
    'ccr': 'CCRO3.SA',
    'cosan': 'CSAN3.SA',
    'cpfl_energia': 'CPFE3.SA',
    'dasa': 'DASA3.SA',
    'fleury': 'FLRY3.SA',
    'gol': 'GOLL4.SA',
    'hapvida': 'HAPV3.SA',
    'itau': 'ITUB4.SA',
    'locaweb': 'LWSA3.SA',
    'magazine_luiza': 'MGLU3.SA',
    'mrv_engenharia': 'MRVE3.SA',
    'natura': 'NTCO3.SA',
    'petrobras': 'PETR4.SA',
    'santander': 'SANB11.SA',
    'sul_america': 'SULA11.SA',
    'totvs': 'TOTS3.SA',
    'vale': 'VALE3.SA',
    'via_varejo': 'BHIA3.SA'

}


def contar_indicadores(dataframe1, dataframe2, indicador, tipo=1):
    contagem = []
    for i, row in dataframe1.iterrows():
        inicio = row['data']
        fim = row['prox_reuniao']
        if not pd.isna(fim):
            filtro = dataframe2[(dataframe2['Date'] >= inicio) & (dataframe2['Date'] <= fim) & (dataframe2[f'Indicator_{indicador}'] == tipo)]
        else:
            fim = inicio + pd.DateOffset(months=3)
            filtro = dataframe2[(dataframe2['Date'] >= inicio) & (dataframe2['Date'] <= fim) & (dataframe2[f'Indicator_{indicador}'] == tipo)]
        contagem.append(len(filtro))
    return contagem


file_data_transcripts = os.listdir('../../dataset/transcripts')
for file in file_data_transcripts:
    if os.path.exists(f'../../dataset/transcripts_and_returns/{name_prices[file]}.csv'):
        print("Transcript and returns file already exists for: " + name_prices[file])
        continue
    if not os.path.exists(f'../../dataset/transcripts/{file}/datas.csv'):
        print("Data file does not exist: "+file)
        continue
    df = pd.read_csv(f'../../dataset/transcripts/{file}/datas.csv')
    df = df.sort_values(by=['data'], ignore_index=True)
    df['data'] = pd.to_datetime(df['data'])
    df['prox_reuniao'] = df['data'].shift(-1)
    df['prox_reuniao'] = pd.to_datetime(df['prox_reuniao'])
    prices = pd.read_csv(f'../../dataset/prices_processed/{name_prices[file]}.csv')
    prices['Date'] = pd.to_datetime(prices['Date'])
    df['Daily_Return_Positive'] = contar_indicadores(df, prices, 'Daily_Return', tipo=1)
    df['Daily_Return_Neutral'] = contar_indicadores(df, prices, 'Daily_Return', tipo=0)
    df['Daily_Return_Negative'] = contar_indicadores(df, prices, 'Daily_Return', tipo=-1)
    df['Daily_Return_Total'] = df['Daily_Return_Positive'] + df['Daily_Return_Neutral'] + df['Daily_Return_Negative']
    df['Week_Return_Positive'] = contar_indicadores(df, prices, 'Week_Return', tipo=1)
    df['Week_Return_Neutral'] = contar_indicadores(df, prices, 'Week_Return', tipo=0)
    df['Week_Return_Negative'] = contar_indicadores(df, prices, 'Week_Return', tipo=-1)
    df['Week_Return_Total'] = df['Week_Return_Positive'] + df['Week_Return_Neutral'] + df['Week_Return_Negative']
    df['Month_Return_Positive'] = contar_indicadores(df, prices, 'Month_Return', tipo=1)
    df['Month_Return_Neutral'] = contar_indicadores(df, prices, 'Month_Return', tipo=0)
    df['Month_Return_Negative'] = contar_indicadores(df, prices, 'Month_Return', tipo=-1)
    df['Month_Return_Total'] = df['Month_Return_Positive'] + df['Month_Return_Neutral'] + df['Month_Return_Negative']
    df.to_csv(f'../../dataset/transcripts_and_returns/{name_prices[file]}.csv', index=False)
    print(f"Transcript and return created in: {name_prices[file]}.csv")

