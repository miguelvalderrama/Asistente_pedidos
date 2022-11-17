import pandas as pd
import numpy
import os
import mysql.connector
import json

host = '10.0.2.1'
user = 'jonas.salas'
password = 'camaleon'
database = 'hptal'

dismeven = {'DESCRIPCION PRODUCTO', 'LOTE', 'SUB TOTAL PRODUCTOS EN Bs', 'CATEGORÍA', 'ARTI.','SUB TOTAL PRODUCTOS EN $', 'UNIDAD DE \nEMPAQUE', 'CODIGO DE BARRA', 'CANTIDAD', ' EQUIVALENTE EN BS', 'UNIDAD DE VENTA', 'PRECIO UNITARIO $', 'FECHA DE VENCIMIENTO', 'MARCA'}
cobeca = {'C. Prov.','existencia', 'PEDIDO', 'Precio Mayoreo', 'Cod. Art.', 'Descripción del Artículo', 'Cod. Ind.', 'OFERTAS', 'DIAS DE CREDITO ', 'Proveedor', 'PRINCIPIO ACTIVO '}
insuaminca = {'CODBARRA', 'NUEVO', 'PRECIO UNIT', 'CODIGO', 'CATEGORIA', 'PEDIDO', 'MONTO', 'OFERTA', 'DESCRIPCION', 'FEC LOTE', 'PRECIO', 'INVENTARIO'}
drolanca = {'F.Venc ', 'Existencia', 'Descripción del Material', 'Principio activo ', 'Dcto', 'Pedido', 'Laboratorio', '   Precio ', 'Bs. Pedido ', 'Precio Final ', 'Crédito ', 'Precio Si compra 18 Unid', 'Codigo de Barras', 'Código'}
vitalclinic = {'LABORATORIO', 'PSICOTROPICOS Y CONTROLADO', 'FEC LOTE', 'PROMOCION', 'MONTO', 'CATEGORIA', 'PRECIO', 'CODIGO', 'PEDIDO', 'PRINC ACTIVO', 'INVENTARIO', 'NUEVO', 'DESCRIPCION', 'PRECIO UNIT', '%', 'COD BARRAS'}
gracitana_medicinas = {'PRECIO', 'LABORATORIO', '$', 'TOTAL PEDIDO', 'PEDIDO', 'NOMBRE', 'CODIGO DE BARRA', 'VENCIMIENTO', 'CODIGO'}
gracitana_material_medico = {'MARCA', 'PRECIO', '$', 'TOTAL PEDIDO', 'PEDIDO', 'NOMBRE', 'CODIGO DE BARRA', 'VENCIMIENTO', 'CODIGO'}
drolvilla_importados = {'TOTAL $', 'CANT', 'FACTURACION TASA BCV ', 'COSTO EN BOLIVARES PARA FACTURACION', 'COSTO $', 'TOTAL BOLIVARES DIGITAL', 'MEDICINA IMPORTADA SOLO PAGO EN DOLARES', 'MARCA', 'CODIGO'}
drolvilla_nacionales = ['alterno', 'cant', 'nombre', 'precio', 'total bs', 'Unnamed: 5']
distmedic = {'Total Existe', 'PEDIDO', 'Código', 'Descripción', 'TOTAL', 'Garantía', 'ANTES', 'AHORA'}
drosalud = {'Divisa', 'PRECIO', 'Total', 'PVP', 'Columna1', 'Marca', 'Pedido', 'Descripción', 'Código'}
unipharma = {'USD', 'PEDIDO', 'TOTAL', 'CODIGO', 'DESCRIPCION'}

drogs_existentes = ['dismeven', 'cobeca', 'insuaminca', 'drolanca', 'vitalclinic', 'gracitana_medicinas', 'gracitana_material_medico', 'drolvilla_importados', 'drolvilla_nacionales', 'distmedic', 'drosalud', 'unipharma']


def connect_to_db():
    # Connect to the database
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    # Create a cursor
    mycursor = mydb.cursor()
    # Return the cursor and the connection
    return mycursor, mydb

# Transform the raw data into a csv file
def transform_data():
    # Get raw data from ./Archivos
    raw_data = os.listdir('./Archivos')
    # Open temp/relacion.json
    with open('./temp/relacion.json', 'r') as json_file:
        relacion = json.load(json_file)
    # Iterate over the raw data
    for file in raw_data:
        if file.endswith('.xlsx'):
            data = pd.read_excel(f'./Archivos/{file}', engine='openpyxl')
        elif file.endswith('.xls'):
            data = pd.read_excel(f'./Archivos/{file}', engine='xlrd')
        # Get file name
        file_name = name_drog(data, file.split('.')[0])
        if file_name != "No encontrado":
            # Save relacion between file name and file name in json
            relacion[file_name] = file
            # Save the data as a csv file in temp/csv folder
            data.to_csv(f'./temp/raw_csv/{file_name}.csv', index=False)
            # Move files from archivos to temp/processed_excel if file_name not "No encontrado"
            os.rename(f'./Archivos/{file}', f'./temp/processed_excel/{file}')
    # Save the relacion in json
    with open('./temp/relacion.json', 'w') as json_file:
        # if key in relacion is not in json, add it
        json.dump(relacion, json_file)


def name_drog(data, name):
    data_iloc0 = set([x for x in data.iloc[0]])
    data_iloc5 = set([x for x in data.iloc[5]])
    data_iloc7 = set([x for x in data.iloc[7]])
    data_iloc8 = set([x for x in data.iloc[8]])
    data_iloc11 = set([x for x in data.iloc[11]])
    data_columns = [x for x in data.columns]

    if dismeven.issubset(data_iloc8):
        return "Dismeven"
    elif cobeca.issubset(data_iloc5):
        return "Cobeca"
    elif insuaminca.issubset(data_iloc8):
        return "Insuaminca"
    elif drolanca.issubset(data_iloc5):
        return "Drolanca"
    elif vitalclinic.issubset(set([x for x in data.iloc[9]])):  
        return "Vitalclinic"
    elif gracitana_medicinas.issubset(data_iloc11):
        return "Gracitana Medicinas"
    elif gracitana_material_medico.issubset(data_iloc11):
        return "Gracitana Material Medico"
    elif drolvilla_importados.issubset(data_iloc0):
        return "Drolvilla Importados"
    elif drolvilla_nacionales == data_columns:
        return "Drolvilla Nacionales"
    elif distmedic.issubset(data_iloc11):
        return "Distmedic"
    elif drosalud.issubset(data_iloc7):
        return "Drosalud"
    elif unipharma.issubset(data_iloc8):
        return "Unipharma"
    else:
        return "No encontrado"

def process_cobeca():
    # Get raw data from ./temp/raw_csv/Cobeca.csv
    data = pd.read_csv('./temp/raw_csv/Cobeca.csv')
    # New headers
    new_headers = data.iloc[5]
    # Drop the first 6 rows
    data = data[6:]
    # Rename the headers
    data.columns = new_headers
    cols_to_use = ['Descripción del Artículo', 'Precio Mayoreo', 'OFERTAS', 'existencia']
    data = data[cols_to_use]
    # Replace - with 0 in the column 'OFERTAS'
    data['OFERTAS'] = data['OFERTAS'].replace('-', 0)
    # Transform precio mayoreo and ofertas to float
    data['Precio Mayoreo'] = data['Precio Mayoreo'].str.replace(',', '.').astype(float)
    data['OFERTAS'] = data['OFERTAS'].str.replace(',', '.').astype(float)
    # if ofertas is empty, then ofertas = 0
    data['OFERTAS'] = data['OFERTAS'].replace(numpy.nan, 0)
    # If Precios Mayoreo is 0.01 or less, drop the row
    data = data[data['Precio Mayoreo'] > 0.99]
    # If existencia is 0, drop the row
    data = data[data['existencia'] != 0]
    # Precio Mayoreo * OFERTAS if OFERTAS is not 0 if OFERTAS is 0, Precio Mayoreo
    data['Precio Mayoreo'] = numpy.where(data['OFERTAS'] != 0, data['Precio Mayoreo'] - (data['Precio Mayoreo']*data['OFERTAS']), data['Precio Mayoreo'])
    # Round the column 'Precio Mayoreo' to 2 decimals
    data['Precio Mayoreo'] = data['Precio Mayoreo'].round(2)
    # Drop the column 'OFERTAS'
    data = data.drop('OFERTAS', axis=1)
    # Drop the column 'existencia'
    data = data.drop('existencia', axis=1)
    # Add column 'Proveedor'
    data['Proveedor'] = 'Cobeca'
    # Order by Descripción del Artículo
    data = data.sort_values(by=['Descripción del Artículo'])
    # Save the data as a csv file in temp/processed_csv folder
    data.to_csv('./temp/processed_csv/Cobeca.csv', index=False)

def process_dismeven():
    # Get raw data from ./temp/raw_csv/Dismeven.csv
    data = pd.read_csv('./temp/raw_csv/Dismeven.csv')
    # New headers
    new_headers = data.iloc[8]
    # Drop the first 9 rows
    data = data[9:]
    # Rename the headers
    data.columns = new_headers
    cols_to_use = ['DESCRIPCION PRODUCTO', ' EQUIVALENTE EN BS']
    data = data[cols_to_use]
    # Transform 'EQUIVALENTE EN BS' to float
    data[' EQUIVALENTE EN BS'] = data[' EQUIVALENTE EN BS'].str.replace(',', '.').astype(float)
    # Round the column 'EQUIVALENTE EN BS' to 2 decimals
    data[' EQUIVALENTE EN BS'] = data[' EQUIVALENTE EN BS'].round(2)
    # Rename the columns
    data = data.rename(columns={'DESCRIPCION PRODUCTO': 'Descripción del Artículo', ' EQUIVALENTE EN BS': 'Precio Mayoreo'})
    # Add column 'Proveedor'
    data['Proveedor'] = 'Dismeven'
    # Save the data as a csv file in temp/processed_csv folder
    data.to_csv('./temp/processed_csv/Dismeven.csv', index=False)

def process_drolanca():
    # Get raw data from ./temp/raw_csv/Drolanca.csv
    data = pd.read_csv('./temp/raw_csv/Drolanca.csv')
    # New headers    
    new_headers = data.iloc[5]
    # Drop the first 10 rows
    data = data[10:]
    # Rename the headers
    data.columns = new_headers
    cols_to_use = ['Descripción del Material', 'Precio Final ']
    data = data[cols_to_use]
    # Transform 'Precio Final' to float
    data['Precio Final '] = data['Precio Final '].str.replace(',', '.').astype(float)
    # Round the column 'Precio Final' to 2 decimals
    data['Precio Final '] = data['Precio Final '].round(2)
    # Rename the columns
    data = data.rename(columns={'Descripción del Material': 'Descripción del Artículo', 'Precio Final ': 'Precio Mayoreo'})
    # Add column 'Proveedor'
    data['Proveedor'] = 'Drolanca'
    # Save the data as a csv file in temp/processed_csv folder
    data.to_csv('./temp/processed_csv/Drolanca.csv', index=False)

def process_gracitana_medicinas():
    # Get raw data from ./temp/raw_csv/Gracitana Medicinas.csv
    data = pd.read_csv('./temp/raw_csv/Gracitana Medicinas.csv')
    # New headers
    new_headers = data.iloc[11]
    # Drop the first 12 rows
    data = data[12:]
    # Rename the headers
    data.columns = new_headers
    cols_to_use = ['NOMBRE', 'PRECIO']
    data = data[cols_to_use]
    # Rename the columns
    data = data.rename(columns={'NOMBRE': 'Descripción del Artículo', 'PRECIO': 'Precio Mayoreo'})
    # Add column 'Proveedor'
    data['Proveedor'] = 'Gracitana Medicinas'
    # Save the data as a csv file in temp/processed_csv folder
    data.to_csv('./temp/processed_csv/Gracitana Medicinas.csv', index=False)

def process_gracitana_material_medico():
    # Get raw data from ./temp/raw_csv/Gracitana Material Medico.csv
    data = pd.read_csv('./temp/raw_csv/Gracitana Material Medico.csv')
    # New headers
    new_headers = data.iloc[11]
    # Drop the first 12 rows
    data = data[12:]
    # Rename the headers
    data.columns = new_headers
    cols_to_use = ['NOMBRE', 'PRECIO']
    data = data[cols_to_use]
    # Rename the columns
    data = data.rename(columns={'NOMBRE': 'Descripción del Artículo', 'PRECIO': 'Precio Mayoreo'})
    # Add column 'Proveedor'
    data['Proveedor'] = 'Gracitana Material Medico'
    # Save the data as a csv file in temp/processed_csv folder
    data.to_csv('./temp/processed_csv/Gracitana Material Medico.csv', index=False)

def process_insuaminca():
    # Get raw data from ./temp/raw_csv/Insuaminca.csv
    data = pd.read_csv('./temp/raw_csv/Insuaminca.csv')
    # New headers
    new_headers = data.iloc[8]
    # Drop the first 9 rows
    data = data[9:]
    # Rename the headers
    data.columns = new_headers
    cols_to_use = ['DESCRIPCION', 'PRECIO']
    data = data[cols_to_use]
    # Transform 'PRECIO' to float
    data['PRECIO'] = data['PRECIO'].str.replace(',', '.').astype(float)
    # Get a connection to the database
    cursor, conn = connect_to_db()
    # Get tasa de cambio
    cursor.execute("SELECT precio_compra_moneda_nacional FROM tipo_moneda WHERE nombre_singular = 'DOLAR'")
    tasa_cambio = cursor.fetchone()[0]
    # Close the connection
    conn.close()
    # Transform 'PRECIO' to bolivares
    data['PRECIO'] = data['PRECIO'] * float(tasa_cambio)
    # Round the column 'PRECIO' to 2 decimals
    data['PRECIO'] = data['PRECIO'].round(2)
    # Rename the columns
    data = data.rename(columns={'DESCRIPCION': 'Descripción del Artículo', 'PRECIO': 'Precio Mayoreo'})
    # Add column 'Proveedor'
    data['Proveedor'] = 'Insuaminca'
    # Save the data as a csv file in temp/processed_csv folder
    data.to_csv('./temp/processed_csv/Insuaminca.csv', index=False)

def process_vitalclinic():
    # Get raw data from ./temp/raw_csv/Vitalclinic.csv
    data = pd.read_csv('./temp/raw_csv/Vitalclinic.csv')
    # New headers
    new_headers = data.iloc[9]
    # Drop the first 10 rows
    data = data[10:]
    # Rename the headers
    data.columns = new_headers
    cols_to_use = ['DESCRIPCION', 'PRECIO']
    data = data[cols_to_use]
    # Drop duplicated columns
    data = data.loc[:,~data.columns.duplicated(keep='last')].copy()
    # Transform 'PRECIO' to float
    data['PRECIO'] = data['PRECIO'].str.replace(',', '.').astype(float)
    # Get a connection to the database
    cursor, conn = connect_to_db()
    # Get tasa de cambio
    cursor.execute("SELECT precio_compra_moneda_nacional FROM tipo_moneda WHERE nombre_singular = 'DOLAR'")
    tasa_cambio = cursor.fetchone()[0]
    # Close the connection
    conn.close()
    # Transform 'PRECIO' to bolivares
    data['PRECIO'] = data['PRECIO'] * float(tasa_cambio)
    # Round the column 'PRECIO' to 2 decimals
    data['PRECIO'] = data['PRECIO'].round(2)
    # Rename the columns
    data = data.rename(columns={'DESCRIPCION': 'Descripción del Artículo', 'PRECIO': 'Precio Mayoreo'})
    # Add column 'Proveedor'
    data['Proveedor'] = 'Vitalclinic'
    # Save the data as a csv file in temp/processed_csv folder
    data.to_csv('./temp/processed_csv/Vitalclinic.csv', index=False)

'''def process_distmedic():
    # Get raw data from ./temp/raw_csv/Distmedic.csv
    data = pd.read_csv('./temp/raw_csv/Distmedic.csv')
    # New headers
    new_headers = data.iloc[23]
    # Drop the first 12 rows
    data = data[:]
    # Rename the headers
    data.columns = new_headers
    print(data.columns)'''

def process_drosalud():
    # Get raw data from ./temp/raw_csv/Drosalud.csv
    data = pd.read_csv('./temp/raw_csv/Drosalud.csv')
    # New headers
    new_headers = data.iloc[7]
    # Drop the first 10 rows
    data = data[8:]
    # Rename the headers
    data.columns = new_headers
    cols_to_use = ['Descripción', 'PRECIO']
    data = data[cols_to_use]
    # Transform 'PRECIO' to float
    data['PRECIO'] = data['PRECIO'].str.replace(',', '.').astype(float)
    # Get a connection to the database
    cursor, conn = connect_to_db()
    # Get tasa de cambio
    cursor.execute("SELECT precio_compra_moneda_nacional FROM tipo_moneda WHERE nombre_singular = 'DOLAR'")
    tasa_cambio = cursor.fetchone()[0]
    # Close the connection
    conn.close()
    # Transform 'PRECIO' to bolivares
    data['PRECIO'] = data['PRECIO'] * float(tasa_cambio)
    # Round the column 'PRECIO' to 2 decimals
    data['PRECIO'] = data['PRECIO'].round(2)
    # Rename the columns
    data = data.rename(columns={'Descripción': 'Descripción del Artículo', 'PRECIO': 'Precio Mayoreo'})
    # Add column 'Proveedor'
    data['Proveedor'] = 'Drosalud'
    # Save the data as a csv file in temp/processed_csv folder
    data.to_csv('./temp/processed_csv/Drosalud.csv', index=False)

def process_drolvilla_nacionales():
    # Get raw data from ./temp/raw_csv/Drolvilla_nacionales.csv
    data = pd.read_csv('./temp/raw_csv/Drolvilla Nacionales.csv')
    cols = ['nombre', 'precio']
    data = data[cols]
    # Rename the columns
    data = data.rename(columns={'nombre': 'Descripción del Artículo', 'precio': 'Precio Mayoreo'})
    # Get index where precio mayoreo = 'Sub - Total Factura:'
    index = data[data['Precio Mayoreo'] == 'Sub - Total Factura:'].index
    # Drop rows from index to the end
    data = data.drop(data.index[index[0]:])
    # Add column 'Proveedor'
    # Transform 'PRECIO' to float
    data['Precio Mayoreo'] = data['Precio Mayoreo'].str.replace(',', '.').astype(float)
    data['Proveedor'] = 'Drolvilla Nacional'
    # Save the data as a csv file in temp/processed_csv folder
    data.to_csv('./temp/processed_csv/Drolvilla Nacional.csv', index=False)

def process_drolvilla_importados():
    # Get raw data from ./temp/raw_csv/Drolvilla_importados.csv
    data = pd.read_csv('./temp/raw_csv/Drolvilla Importados.csv')
    # New headers
    new_headers = data.iloc[0]
    # Drop the first row
    data = data[1:]
    # Rename the headers
    data.columns = new_headers
    cols_to_use = ['MEDICINA IMPORTADA SOLO PAGO EN DOLARES', 'COSTO EN BOLIVARES PARA FACTURACION']
    data = data[cols_to_use]
    # Transform 'PRECIO' to float
    data['COSTO EN BOLIVARES PARA FACTURACION'] = data['COSTO EN BOLIVARES PARA FACTURACION'].str.replace(',', '.').astype(float)
    # Round the column 'PRECIO' to 2 decimals
    data['COSTO EN BOLIVARES PARA FACTURACION'] = data['COSTO EN BOLIVARES PARA FACTURACION'].round(2)
    # Rename the columns
    data = data.rename(columns={'MEDICINA IMPORTADA SOLO PAGO EN DOLARES': 'Descripción del Artículo', 'COSTO EN BOLIVARES PARA FACTURACION': 'Precio Mayoreo'})
    # Add column 'Proveedor'
    data['Proveedor'] = 'Drolvilla Importado'
    # Save the data as a csv file in temp/processed_csv folder
    data.to_csv('./temp/processed_csv/Drolvilla Importado.csv', index=False)

def process_unipharma():
    # Get raw data from ./temp/raw_csv/Unipharma.csv
    data = pd.read_csv('./temp/raw_csv/Unipharma.csv')
    # New headers
    new_headers = data.iloc[8]
    # Drop the first row
    data = data[9:]
    # Rename the headers
    data.columns = new_headers
    cols = ['DESCRIPCION', -0.05]
    data = data[cols]
    # Rename the columns
    data = data.rename(columns={'DESCRIPCION': 'Descripción del Artículo', -0.05: 'Precio Mayoreo'})
    # Drop rows where 'Precio Mayoreo' is 'NaN' or empty
    data = data.dropna(subset=['Precio Mayoreo'])
    # Transform 'PRECIO' to float
    data['Precio Mayoreo'] = data['Precio Mayoreo'].astype(float)
    # Connect to the database
    cursor, conn = connect_to_db()
    # Get tasa de cambio
    cursor.execute("SELECT precio_compra_moneda_nacional FROM tipo_moneda WHERE nombre_singular = 'DOLAR'")
    tasa_cambio = cursor.fetchone()[0]
    # Close the connection
    conn.close()
    # Transform 'PRECIO' to bolivares
    data['Precio Mayoreo'] = data['Precio Mayoreo'] * float(tasa_cambio)
    # Round the column 'PRECIO' to 2 decimals
    data['Precio Mayoreo'] = data['Precio Mayoreo'].round(2)
    # Add column 'Proveedor'
    data['Proveedor'] = 'Unipharma'
    # Save the data as a csv file in temp/processed_csv folder
    data.to_csv('./temp/processed_csv/Unipharma.csv', index=False)

def prepare_final_csv():
    transform_data()
    if os.path.exists('./temp/raw_csv/'):
        list_not_found = []
        if not os.listdir('./temp/raw_csv/'):
            return Exception('No se encontraron archivos en la carpeta ./temp/raw_csv/')
        # Get all the files in temp/raw_csv folder
        files = os.listdir('./temp/raw_csv/')
        # Loop through the files
        for file in files:
            # Get the name of the file
            file_name = file.split('.')[0]
            # Call the function that matches the file name
            if file_name == 'Gracitana Medicinas':
                process_gracitana_medicinas()
            elif file_name == 'Gracitana Material Medico':
                process_gracitana_material_medico()
            elif file_name == 'Insuaminca':
                process_insuaminca()
            elif file_name == 'Vitalclinic':
                process_vitalclinic()
            elif file_name == 'Cobeca':
                process_cobeca()
            elif file_name == 'Drolanca':
                process_drolanca()
            elif file_name == 'Dismeven':
                process_dismeven()
            elif file_name == 'Drosalud':
                process_drosalud()
            elif file_name == 'Drolvilla Nacionales':
                process_drolvilla_nacionales()
            elif file_name == 'Drolvilla Importados':
                process_drolvilla_importados()
            elif file_name == 'Unipharma':
                process_unipharma()
            else:
                list_not_found.append(file_name)
    # If not files in ('./temp/processed_csv/') folder break the function
    if not os.listdir('./temp/processed_csv/'):
        return Exception('No se encontraron archivos en la carpeta ./temp/processed_csv/')
    # Get all the csv files in temp/processed_csv folder
    files = os.listdir('./temp/processed_csv/')
    # Create a list to store the dataframes
    list_df = []
    # Loop through the files
    for file in files:
        # Read the csv file
        df = pd.read_csv('./temp/processed_csv/' + file)
        # Append the dataframe to the list
        list_df.append(df)
    # Concatenate all the dataframes in the list
    data = pd.concat(list_df)
    # Drop nan rows
    data = data.dropna()
    # Drop rows where Precios Mayoreo is 'PRECIO'
    data = data[data['Precio Mayoreo'] != 'PRECIO']
    # Open the file 'farmacias.json'
    with open('./farmacias.json') as json_file:
        # Load the json file
        farmacias = json.load(json_file)
    # Create a list to store the actives farmacias
    list_farmacias_abrev = []
    # Loop through the farmacias
    for farmacia in farmacias:
        # Check if the farmacia is active
        if farmacias[farmacia]['estado'] == 'Activo':
            # Append the farmacia to the list
            list_farmacias_abrev.append(farmacias[farmacia]['abreviatura'])
    # Create a column for each farmacia
    for farmacia in list_farmacias_abrev:
        data[farmacia] = 0
    # Save the data as a csv file in temp/final_csv folder
    data.to_csv('./temp/final_csv.csv', index=False)