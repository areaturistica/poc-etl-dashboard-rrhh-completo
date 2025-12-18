import csv
import mysql.connector
from mysql.connector import Error

def load_csv_to_mysql(csv_filepath, table_name):
    connection = None
    try:
        # Configuración de la conexión
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='rrhh'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            with open(csv_filepath, mode='r', encoding='utf-8') as file:
                csv_data = csv.reader(file)
                header = next(csv_data)  # Obtener cabeceras
                
                # Construcción dinámica de la consulta INSERT con IGNORE para evitar duplicados por ID
                cols = ", ".join(header)
                placeholders = ", ".join(["%s"] * len(header))
                sql = f"INSERT IGNORE INTO {table_name} ({cols}) VALUES ({placeholders})"
                
                # Carga de datos
                count = 0
                for row in csv_data:
                    cursor.execute(sql, row)
                    if cursor.rowcount > 0:
                        count += 1
                
                connection.commit()
                print(f"Éxito: Se han insertado {count} registros en la tabla '{table_name}'.")

    except Error as e:
        print(f"Error conectando a MySQL: {e}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{csv_filepath}'.")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada.")

if __name__ == "__main__":
    load_csv_to_mysql('personas.csv', 'personas')
