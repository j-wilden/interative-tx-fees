import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from utils import make_expanders, generate_data, load_config


def page_single():
    """ 
    Displays the controls and graph for a single transaction
    """

    config = load_config("config.toml")
    st.sidebar.title("Control Panel")

    #----- SIDE BAR -----
    st.sidebar.subheader("Expand the sections below to configure variables:")

    # ---- EXPANDER --------------

    with make_expanders("Miner Fee"):

        tx_rate = st.number_input(
            "Default is 1 sat/B (satoshi per byte)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="TAAL charge 0.5 sat/B transaction fee, plus 0.25 sat/B relay fee",
        )

    with make_expanders("Transaction Size"):

        transaction_range = st.slider(
            "Select a range of transaction sizes (kb)", 
            config["min_transaction_size"], config["max_transaction_size"], 
            (config["default_min"], config["default_max"]), step = 0.1,
            help="Range of transaction sizes to graph",
        )


 
    with make_expanders("Currency Rate & Display"):
        
        currency_selection = st.radio("Select Display Currency Format:", ( 'Satoshis', 'BSV', 'GBP'))  
        
        exchange_rate = st.slider(
            "BSV to GBP exchange rate (£'s)",
            min_value=40,
            max_value=400,  
            value=80,
            step=1,
            help="Enter the exchange rate, BSV to GBP",
        )

    # ---- END EXPANDER --------------
    #----- END SIDE BAR -----

    st.title('Transaction Fees Calculator')
    single_tx_data = generate_data(transaction_range, tx_rate)

    # -----------------------------
    # Basic line chart

    st.subheader("The cost of a single transaction. ")
    

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(single_tx_data)


    # 'Satoshis', 'BSV', 'GBP'
    if currency_selection == "BSV" :
        single_tx_data['fee'] = single_tx_data['fee'] / config["satoshis_in_bsv"]
        st.write("Size (kb) vs Fees (BSV)")

    elif currency_selection == "GBP" :
        single_tx_data['fee'] = single_tx_data['fee'] / config["satoshis_in_bsv"]
        single_tx_data['fee'] = single_tx_data['fee'] * exchange_rate
        st.write("Size (kb) vs Fees (GBP £'s)")
    
    else :
        st.write("Size (kb) vs Fees (satoshis)")

    st.line_chart(single_tx_data.set_index('fee'))

  


