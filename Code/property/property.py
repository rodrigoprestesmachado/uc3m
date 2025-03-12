import sys
import os
import pandas as pd

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../rag')))

from orion_rag_chroma_client import OrionChromaDBClient

# Caminho para o arquivo CSV
file_path = 'property.csv'

# Leitura do arquivo CSV
df = pd.read_csv(file_path)

# Filtrar epenas para a coluna ESPECIFICAÇÃO
df = df[['ESPECIFICAÇÃO']]
print(df.head())

# Pra cada registro adicionar a coleção
client = OrionChromaDBClient("property")
client.add_chunks_to_db(df['ESPECIFICAÇÃO'].tolist())
