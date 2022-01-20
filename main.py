
import streamlit as st

from page_single import page_single
from page_multiple import page_multiple

def main():
    """
    Register pages to Display:
        page_single - contains page with graph of fees for a single transaction
        page_multiple - contains page with graph of fees for multiple transactions
    """

    pages = {
        "Single Transaction": page_single,
        "Multiple Transactions": page_multiple,
    }

    st.sidebar.title("Main options")

    # Radio buttons to select desired option
    page = st.sidebar.radio("Select:", tuple(pages.keys()))
                                
    # Display the selected page with the session state
    pages[page]()

    # Write About
    st.sidebar.header("About")
    st.sidebar.warning(
            """
            This app is created and maintained by 
            the nChain Research & Development team.
            """
    )


if __name__ == "__main__":
    main()