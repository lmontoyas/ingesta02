import mysql.connector
import pandas as pd
import boto3

# Conectar a la base de datos MySQL
conn = mysql.connector.connect(
    host="tu_host_mysql",
	port="44.221.218.236",
    user="root", 
    password="utec",
    database="tienda"
)

cursor = conn.cursor()

# Consultar los registros de una tabla
query = "SELECT * FROM tienda"
cursor.execute(query)

# Obtener los datos
rows = cursor.fetchall()

# Convertir a un DataFrame de Pandas para facilitar la exportación a CSV
df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])

# Guardar los datos en un archivo CSV
csv_file = "data.csv"
df.to_csv(csv_file, index=False)

# Subir el archivo CSV a un bucket S3
s3 = boto3.client('s3')
bucket_name = "gcr-output-02"
s3.upload_file(csv_file, bucket_name, csv_file)

print("Ingesta completada y archivo subido a S3")

# Cerrar conexión
cursor.close()
conn.close()
