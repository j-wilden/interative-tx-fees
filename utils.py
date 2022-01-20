import streamlit as st    
import pandas as pd
import numpy as np
import toml

#  **** USEFUL FUNCTION DEFS *****+
def load_config(filename="config.toml") :
    """ Load config from toml file
    """
    try:
        with open(filename, "r") as f:
            config = toml.load(f)
        return config
    except FileNotFoundError as e:
        print(e)
        return {}

def make_expanders(expander_name, sidebar=True):
    """ Set up expanders which contains a set of options. """
    if sidebar:         
        try:
            return st.sidebar.expander(expander_name)
        except:
            return st.sidebar.beta_expander(expander_name)

def fee_calc(tx, tx_rate) :
    config = load_config("config.toml")
    return tx * tx_rate * config["bytes_in_kb"]

def fee_calc_scaled(tx, num_people, daily_tx_rate) : 
    return tx * num_people * daily_tx_rate

def generate_data( range, tx_rate ) :
    ar = np.linspace( range[0], range[1], num=10 )
    data = pd.DataFrame ({'tx_size' : ar })
    data["fee"] = fee_calc( data["tx_size"], tx_rate ) 
    return data 

@st.cache
def load_tx_data():
    data = pd.read_csv('data.csv', names=["tx"])
    data["fee"] = fee_calc(data["tx"]) 
    return data
