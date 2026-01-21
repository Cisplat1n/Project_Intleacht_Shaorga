########################
#Libraries
########################

import pandas as pd
import pathlib 



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


    return 




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