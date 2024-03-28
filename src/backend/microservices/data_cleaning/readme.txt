JSON de prueba

{
  "file_name": "train.csv",
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
