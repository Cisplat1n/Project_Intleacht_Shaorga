########################
#Libraries
########################

import pandas as pd
import pathlib 
from io import StringIO



########################
#Data Read in function 
########################

def read_df(input):
    if isinstance(input, pd.DataFrame):
        return input
    
    try:
        path = pathlib.Path(input)

    except TypeError:
        raise TypeError("Input must be a DataFrame or a path to a CSV file")

    if path.is_file() and path.suffix == ".csv":
        return pd.read_csv(path)

    print("Error. Try pass a CSV direct or Filepath to a CSV.")
    return None



########################
#df checker 
#(should check for empty data frames and do some basic data Anonymisation)
########################

def df_checker(data):
    #shape
    shape = data.shape

    #column names
    col_names = data.columns.tolist()

    #Info as string
    buffer = StringIO()
    data.info(buf=buffer)
    info = buffer.getvalue()

    #missing values
    per_null= data.isna().mean() * 100
    num_null = data.isna().sum()

    #correlation values
    corr= data.corr(numeric_only=True)  # Pearson by default

    #categorical columns
    cat_cols = data.select_dtypes(include='object').columns

    unique_val = {col: data[col].nunique() for col in cat_cols}
    num_cat_vals = {col: data[col].value_counts() for col in cat_cols}
    cat_col_proportion = {col: data[col].value_counts(normalize=True) for col in cat_cols}


    return {
            "shape": shape,
            "info": info,
            "percent_null": per_null,
            "num_null": num_null,
            "correlation": corr,
            "unique_values": unique_val,
            "cat_value_counts": num_cat_vals,
            "cat_value_proportion": cat_col_proportion,
            "col_names": col_names
        }



#anonymise data for security purposes
#DO NOT SEND SENSITIVE DATA INTO AN LLM EVER! I AM NOT LIABLE IF YOU DO THAT!

def data_anon(data):
    return data


########################
#Data Processing Prompt + Constraints
#(you can build registries in here that help guide the LLM)
########################




########################
#Prompt builder
#(this is where the registries and the prompt will be created)
########################


########################
#API Client call
########################