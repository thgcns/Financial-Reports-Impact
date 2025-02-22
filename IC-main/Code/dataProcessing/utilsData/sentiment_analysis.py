import pandas as pd
import numpy as np
import PyPDF2
from transformers import AutoTokenizer, BertForSequenceClassification
import os
import gc
import torch


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


def extract_text_from_pdf(pdf_path):
    # Abrir o arquivo PDF
    with open(pdf_path, 'rb') as file:
        # Criar um objeto PDF Reader
        reader = PyPDF2.PdfReader(file)

        # Inicializar uma variável para armazenar o texto
        all_text = ""

        # Iterar sobre cada página e extrair o texto
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            all_text += page.extract_text()
    # Remover os caracteres de nova linha
    all_text = all_text.replace('\n', ' ')
    # Segmentar o texto usando "." como separador
    segments = all_text.split('. ')

    # Remover espaços em branco desnecessários e segmentos vazios
    segments = [segment.strip() for segment in segments if segment.strip() and len(segment.strip()) >= 15]

    return segments


pred_mapper = {
    0: 1,
    1: -1,
    2: 0
  }
tokenizer = AutoTokenizer.from_pretrained("lucas-leme/FinBERT-PT-BR")
finbertptbr = BertForSequenceClassification.from_pretrained("lucas-leme/FinBERT-PT-BR")

files = ['BB']  # os.listdir("../../dataset/transcripts")
print(files)
for file in files:
    try:
        df = pd.read_csv(f"../dataset/transcripts_and_returns/{name_prices[file]}.csv")
        for i, row in df.iterrows():
            if not pd.isna(row['positive_sentiment']):
                print(row['positive_sentiment'])
                continue
            text_extract_name = row['trimestre']
            text = extract_text_from_pdf(f'../dataset/transcripts/{file}/{text_extract_name}.pdf')
            tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

            finbertptbr_outputs = finbertptbr(**tokens)
            preds = [pred_mapper[np.argmax(pred)] for pred in finbertptbr_outputs.logits.cpu().detach().numpy()]
            posi, neut, nega = preds.count(1), preds.count(0), preds.count(-1)
            df.loc[i, 'positive_sentiment'] = posi
            df.loc[i, 'neutral_sentiment'] = neut
            df.loc[i, 'negative_sentiment'] = nega
            df.to_csv(f"../dataset/transcripts_and_returns/{name_prices[file]}.csv", index=False)

            del tokens, finbertptbr_outputs, preds
            torch.cuda.empty_cache()

    except FileNotFoundError as e:
        print(f"Erro de arquivo não encontrado: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

