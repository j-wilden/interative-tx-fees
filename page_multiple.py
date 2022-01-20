import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from utils import make_expanders, generate_data, fee_calc_scaled, fee_calc, load_config

def page_multiple():
    """ 
    Displays the controls and graph for multiple transactions
    """

    st.sidebar.title("Control Panel")



    st.title('Transaction Fees Calculator')

    #----- SIDE BAR -----
    config = load_config("config.toml")
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
            config["min_transaction_size"], 
            config["max_transaction_size"], 
            (config["default_min"], config["default_max"]), step = 0.1,
            help="Range of transaction sizes to graph",
        )


    with make_expanders("Country Specific"):

        num_people = st.slider(
            "Number people with wallets",
            min_value=1000,
            max_value=1000000,  
            value=220000,
            step=100,
            help="Enter the expected number of people participating in Digital Cash",
        )

        daily_tx_rate = st.slider(
            "Number of transactions per person per day",
            min_value=0,
            max_value=100,  
            value=1,
            step=1,
            help="Enter the average daily number of Digital Cash transactions made per person",
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

    with make_expanders("Plot"):

        tx_size = st.slider(
            "Highlight Transaction Size (kb)",
            min_value=transaction_range[0],
            max_value=transaction_range[1],  
            value=2.0,
            step=0.5,
            help="Enter the size of the transaction in kb",
        )

    # ---- END EXPANDER --------------

    #----- END SIDE BAR -----

    # -----------------------------
    scaled_tx_data = generate_data(transaction_range, tx_rate)

    # -----------------------------
    # Chart on steroids

    # scale fees by # wallets and # transactions per day, default in satoshis
    scaled_tx_data['fee'] = fee_calc_scaled( scaled_tx_data['fee'], num_people, daily_tx_rate )
    title = "fee - satoshis"

    rule_x =  fee_calc_scaled(fee_calc(tx_size, tx_rate), num_people, daily_tx_rate )

    # 'Satoshis', 'BSV', 'GBP'
    if currency_selection != "Satoshis" :
        scaled_tx_data['fee'] = scaled_tx_data['fee'] / config["satoshis_in_bsv"]
        title = "fee - BSV"
        rule_x = rule_x / config["satoshis_in_bsv"]

        if currency_selection == "GBP" :
            scaled_tx_data['fee'] = scaled_tx_data['fee'] * exchange_rate
            title = "fee - GBP £'s"
            rule_x = rule_x * exchange_rate

    fig = (
        alt.Chart(scaled_tx_data)
        .mark_line(size=4)
        .encode(
            x=alt.X("fee", title=title),
            y=alt.Y("tx_size", title="size - kb"),
        ).interactive()
    )

    size_rule = (
        alt.Chart(pd.DataFrame({"y":[tx_size]}))
        .mark_rule(size=1, color="red")
        .encode(y="y", tooltip=[alt.Tooltip("y", title="Transaction Size")])
    )

    size_rule2 = (
        alt.Chart(pd.DataFrame({"x":[rule_x]}))
        .mark_rule(size=1, color="red")
        .encode(x="x", tooltip=[alt.Tooltip("x", title="Fee")])
    )

    fig = alt.layer(fig, size_rule, size_rule2)

    st.subheader("The cost of multiple transactions")

    if st.checkbox('Show raw for multiple transactions'):
        st.subheader('Raw data')
        st.write(scaled_tx_data)


    st.altair_chart(fig, use_container_width=True)





