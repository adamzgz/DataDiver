
Documentacion API Data_Cleaning:

Puerto: 8001

Endpoints:

/apply_cleaning -> Endpoint para tratamiento de limpieza de datos en un dataset.

Requiere JSON con las acciones de limpieza a ejecutar.

file_name (Obligatorio): Nombre del archivo csv, xls, xlsx o JSON almacenado en volumen compartido con el servicio dataset_loading.

Parametros opcionales de limpieza:

- "check_duplicates": true/false -> Comprueba si existen lineas duplicadas en el dataset y las cuenta. 
    Devuelve un JSON con:
      -  "message": "Mensaje confirmando la operacion realizada"
         "result": "Mensaje con el numero de duplicados en el dataset"

- "remove_duplicates": true/false -> Borra las lineas duplicadas en el dataset
    Devuelve un JSON con:
  
  "message": "Mensaje confirmando la operacion realizada",
  "result": "Devuelve cuantas lineas se han borrado"

- "count_missing_values": true/false -> Cuenta cuantos valores nulos hay en el dataset
    Devuelve un JSON con:
    
    "message": "Mensaje confirmando la operacion realizada",
    "result": "Devuelve una lista de cada columna y cuantos valores nulos hay en cada una".

- "treat_missing_values": mean/median/mode/drop_rows/drop_columns" -> Imputa la media, mediana o moda a los valores nulos de columnas numericas
    con drop_rows elimina las filas con valores nulos, con drop_columns elimina las columnas con valores nulos.

    Devuelve un JSON con:

    "message":"Mensaje confirmando la operacion realizada",
    "result":" "Devuelve una lista de diccionarios con el dataframe modificado"






JSON DE prueba
{
  "file_name": "diamonds.csv",
  "treat_missing_values": "mean"
}





JSON de ejemplo:
[
  {
    "data_id": "92f8a22d-4ca4-427c-918c-61c43cc146bb",
    "file_name": "train.csv"
  }
]

{
  "file_name": "04413a8e-2033-4fb4-8b09-eb97ed0b1ec7"
  "check_duplicates": true,
  "remove_duplicates": true,
  "count_missing_values": true,
  "treat_missing_values": "mean",
  "outliers": "remove",
  "normalization": "min_max",
  "encoding": "one_hot",
  "drop_columns": ["columna1", "columna2"],
  "show_info": true,
  "change_data_type": {
    "columna_fecha": "datetime",
    "columna_entero": "int"
  },
  "string_operations": "upper",
  "regex_pattern": "^abc",
  "regex_replacement": "def"
}


PRUEBAS

{
  "file_name": "3c5ecc17-9c3d-4053-856c-3bcd01ab4d53",
  "outliers": "remove"
}

[
  {
    "data_id": "3c5ecc17-9c3d-4053-856c-3bcd01ab4d53",
    "file_name": "test.csv"
  },
  {
    "data_id": "f72fd2fd-296b-4288-bc59-af00c59246dc",
    "file_name": "test_cleaned.csv"
  }
]