import pandas as pd
import json

def detect_differences(df_old: pd.DataFrame, df_new: pd.DataFrame) -> dict:
    df_old = df_old.set_index('id')
    df_new = df_new.set_index('id')

    deleted_ids = set(df_old.index) - set(df_new.index)
    added_ids = set(df_new.index) - set(df_old.index)
    common_ids = set(df_old.index).intersection(set(df_new.index))
    modified_ids = {row_id for row_id in common_ids if not df_old.loc[row_id].equals(df_new.loc[row_id])}

    # Detectar columnas añadidas o eliminadas
    added_columns = set(df_new.columns) - set(df_old.columns)
    deleted_columns = set(df_old.columns) - set(df_new.columns)
    
    differences = {
        'deleted_rows': list(deleted_ids),
        'added_rows': df_new.loc[added_ids].to_dict(orient='index'),
        'modified_rows': {row_id: df_new.loc[row_id].to_dict() for row_id in modified_ids},
        'added_columns': list(added_columns),
        'deleted_columns': list(deleted_columns)
    }

    return differences


def store_differences(differences: dict, file_path: str):
    with open(file_path, 'w') as file:
        json.dump(differences, file, indent=4)

def apply_differences(df_base: pd.DataFrame, differences: dict) -> pd.DataFrame:
    df = df_base.copy().set_index('id', drop=False)
    
    # Eliminar y añadir columnas según sea necesario
    for col in differences.get('deleted_columns', []):
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)
    
    for col in differences.get('added_columns', []):
        if col not in df.columns:
            df[col] = None  # Inicializa con None o un valor predeterminado
    
    # Resto del código para aplicar filas añadidas, eliminadas y modificadas...

    # Eliminar filas
    df.drop(differences.get('deleted_rows', []), errors='ignore', inplace=True)
    
    # Añadir filas
    added_rows = [pd.Series(data=row_data, name=row_id) for row_id, row_data in differences.get('added_rows', {}).items()]
    if added_rows:
        df = pd.concat([df, pd.DataFrame(added_rows)], ignore_index=False)
    
    # Modificar filas
    for row_id, row_data in differences.get('modified_rows', {}).items():
        for col, value in row_data.items():
            if col in df.columns and row_id in df.index:
                df.at[row_id, col] = value

    return df.reset_index(drop=True)

