import pandas as pd

drolanca = {'F.Venc ', 'Existencia', 'Descripción del Material', 'Principio activo ', 'Dcto', 'Pedido', 'Laboratorio', '   Precio ', 'Bs. Pedido ', 'Precio Final ', 'Crédito ', 'Codigo de Barras', 'Código'}
drolvilla_nacionales = {'alterno', 'nombre', 'precio'}

df = pd.read_excel('./Archivos/lista_precios 02-01-2023.xls', engine='xlrd')
data_iloc0 = set([x for x in df.iloc[0]])
print(data_iloc0)
print(data_iloc0.difference(drolvilla_nacionales))
print(drolvilla_nacionales.difference(data_iloc0))
df.to_csv('Try.csv')