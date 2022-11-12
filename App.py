import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from PIL import Image  # pip install PIL

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="India Corona Dashboard", page_icon=":earth_asia:", layout="wide")

# ---- MAINPAGE ----
image = Image.open('page_image.png')
col1, col2, col3 = st.columns([0.2, 5, 0.2])
col2.image(image, use_column_width=True)
st.markdown("""---""")


# ---- Data Gathering Using WHO Provided Links ----
@st.cache
def covid19_daily_cases():
    df = pd.read_csv('https://covid19.who.int/WHO-COVID-19-global-data.csv',
                     usecols=['Date_reported', 'Country', 'New_cases', 'Cumulative_cases', 'New_deaths',
                              'Cumulative_deaths'])
    return df


@st.cache
def covid19_cumulative():
    df = pd.read_csv('https://covid19.who.int/WHO-COVID-19-global-table-data.csv',
                     usecols=['Name', 'Cases - cumulative total', 'Cases - newly reported in last 7 days',
                              'Cases - newly reported in last 24 hours',
                              'Deaths - cumulative total', 'Deaths - newly reported in last 7 days',
                              'Deaths - newly reported in last 24 hours'], index_col=False
                     )
    return df


@st.cache
def covid19_vaccination():
    df = pd.read_csv('https://covid19.who.int/who-data/vaccination-data.csv',
                     usecols=['COUNTRY', 'DATE_UPDATED', 'TOTAL_VACCINATIONS'])
    return df


# ---- DataFrames ----
daily_cases_df = covid19_daily_cases()
cumulative_df = covid19_cumulative()
vaccination_df = covid19_vaccination()
global_covid_data = cumulative_df.loc[cumulative_df['Name'] == 'Global']

# ---- SIDEBAR ----
# st.sidebar.header("Please Filter Here:")
selected_country = st.sidebar.selectbox("Select the Country:",
                                        options=cumulative_df["Name"].unique(),
                                        index=2
                                        )

# Global Covid KPI's
st.header('Global Covid Tracker')

col1, col2, col3, col4, col5 = st.columns(5, gap='small')
with col1:
    temp = format(int(global_covid_data['Cases - cumulative total']), ',d')
    string = f"""<p1 style='font-family:sans-serif; color:White; font-size:18px;'>Cases (Cumulative Total) :             
                {temp}</p1>"""
    st.markdown(string, unsafe_allow_html=True)
with col2:
    temp = format(int(vaccination_df['TOTAL_VACCINATIONS'].sum()), ',d')
    string = f"""<p1 style='font-family:sans-serif; color:White; font-size:18px;'>Total Vaccination :                   
                {temp}</p1>"""
    st.markdown(string, unsafe_allow_html=True)
with col3:
    temp = format(int(global_covid_data['Cases - newly reported in last 24 hours']), ',d')
    string = f"""<p1 style='font-family:sans-serif; color:White; font-size:18px;'>Cases In Last 24 Hours :             
                {temp}</p1>"""
    st.markdown(string, unsafe_allow_html=True)
with col4:
    temp = format(int(global_covid_data['Deaths - cumulative total']), ',d')
    string = f"""<p1 style='font-family:sans-serif; color:White; font-size:18px;'>Deaths (Cumulative Total) :     
                {temp}</p1>"""
    st.markdown(string, unsafe_allow_html=True)
with col5:
    temp = format(int(global_covid_data['Deaths - newly reported in last 24 hours']), ',d')
    string = f"""<p1 style='font-family:sans-serif; color:White; font-size:18px;'>Deaths In Last 24 Hours :             
                {temp}</p1>"""
    st.markdown(string, unsafe_allow_html=True)
st.markdown("""---""")

# ---- Country Wise Covid KPI's ----
st.header(f'Country Covid Tracker : {str(selected_country)}')

col1, col2, col3, col4, col5 = st.columns(5, gap='small')
with col1:
    temp = format(int(cumulative_df.loc[cumulative_df['Name'] == selected_country]['Cases - cumulative total']), ',d')
    string = f"""<p1 style='font-family:sans-serif; color:White; font-size:18px;'>Cases (Cumulative Total) :             
                {temp}</p1>"""
    st.markdown(string, unsafe_allow_html=True)
with col2:
    if selected_country == 'Global':
        temp = format(int(vaccination_df['TOTAL_VACCINATIONS'].sum()), ',d')
    else:
        temp = format(int(vaccination_df.loc[vaccination_df['COUNTRY'] == selected_country]['TOTAL_VACCINATIONS']),
                      ',d')
    string = f"""<p1 style='font-family:sans-serif; color:White; font-size:18px;'>Total Vaccination :                   
                {temp}</p1>"""
    st.markdown(string, unsafe_allow_html=True)
with col3:
    temp = format(
        int(cumulative_df.loc[cumulative_df['Name'] == selected_country]['Cases - newly reported in last 24 hours']),
        ',d')
    string = f"""<p1 style='font-family:sans-serif; color:White; font-size:18px;'>Cases In Last 24 Hours :             
                {temp}</p1>"""
    st.markdown(string, unsafe_allow_html=True)
with col4:
    temp = format(int(cumulative_df.loc[cumulative_df['Name'] == selected_country]['Deaths - cumulative total']), ',d')
    string = f"""<p1 style='font-family:sans-serif; color:White; font-size:18px;'>Deaths (Cumulative Total) :       
                {temp}</p1>"""
    st.markdown(string, unsafe_allow_html=True)
with col5:
    temp = format(
        int(cumulative_df.loc[cumulative_df['Name'] == selected_country]['Deaths - newly reported in last 24 hours']),
        ',d')
    string = f"""<p1 style='font-family:sans-serif; color:White; font-size:18px;'>Deaths In Last 24 Hours :     
                {temp}</p1>"""
    st.markdown(string, unsafe_allow_html=True)
st.markdown("""---""")


# ---- DataFrame Country wise ----
df = daily_cases_df.loc[daily_cases_df['Country'] == selected_country]

# ---- Daily New Cases [Line Chart] ----
fig_daily_cases = px.line(df,
                          x='Date_reported',
                          y='New_cases',
                          title="<b>Daily  New  Cases</b>",
                          color_discrete_sequence=["#0083B8"],
                          template="plotly_white")
fig_daily_cases.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))

# ---- Cumulative Cases [Line Chart] ----
fig_cases_cumsum = px.line(df,
                           x='Date_reported',
                           y='Cumulative_cases',
                           title="<b>Cumulative  Cases</b>",
                           color_discrete_sequence=["#0083B8"],
                           template="plotly_white")
fig_cases_cumsum.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))

# ---- Deaths In Last 24 Hours [Line Chart] ----
fig_deaths_in_24hours = px.line(df,
                                x='Date_reported',
                                y='New_deaths',
                                title="<b>Deaths  In  Last  24 Hours</b>",
                                color_discrete_sequence=["#0083B8"],
                                template="plotly_white")
fig_deaths_in_24hours.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))

# ---- Cumulative Deaths [Line Chart] ----
fig_deaths_cumsum = px.line(df,
                            x='Date_reported',
                            y='Cumulative_deaths',
                            title="<b>Cumulative  Deaths</b>",
                            color_discrete_sequence=["#0083B8"],
                            template="plotly_white")
fig_deaths_cumsum.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))

col_1, col_2 = st.columns(2, gap='Small')
col_1.plotly_chart(fig_daily_cases)
col_2.plotly_chart(fig_cases_cumsum)

col_3, col_4 = st.columns(2, gap='Small')
col_3.plotly_chart(fig_deaths_in_24hours)
col_4.plotly_chart(fig_deaths_cumsum)  # , use_container_width=True

st.markdown("""---""")

# ---- Down Image ----
image = Image.open('down_image.png')
col1, col2, col3 = st.columns([0.2, 5, 0.2])
col2.image(image, use_column_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
