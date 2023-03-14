import streamlit as st
import time
import webbrowser
from model import what_stock_to_buy

######## 
## SESSIONS STATES


## SNOW CONTROLLER
if "snow" in st.session_state:
    pass
else:
    st.snow()
    st.session_state = "snow"

if 'display_rec'  in st.session_state:
    display_rec = True
else:
    display_rec = False

# 

with open( "design/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


st.image('design/hodl.png')
st.markdown("<h2 class = head; style='text-align: center;'>Artificial Intelligence Recommandation        </h2>", unsafe_allow_html=True)

with st.columns(5)[2]:
    if st.button('DISCOVER'):
        if display_rec == False:
            with st.spinner('Wait for it...'):
                time.sleep(3)
                display_rec = True
                st.session_state = st.session_state + ' ' + 'display_rec' 

if display_rec :
    st.markdown("<h2 class = 'investment_rec'; style='text-align: center; font-family: Press Start 2P'>Buy Tesla</h2>", unsafe_allow_html=True)

st.radio(
    "Select your broker 👇",
    ["Interactive Broker", "Robinhood", "E-Trade", "Charles Schwab", "TD Ameritrade"],
    key="visibility",
    label_visibility="visible",
    horizontal=True
)

url = 'https://www.interactivebrokers.com/en/home.php'


with st.columns(9)[4]:

    if st.button('BUY'):
        st.balloons()
        time.sleep(2)
        webbrowser.open_new_tab(url)



st.write(what_stock_to_buy())
