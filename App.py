import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go # Graphic Library
import streamlit as st  # pip install streamlit
from PIL import Image  # pip install PIL
from numerize import numerize  # pip install numerize
from pathlib import Path

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="India Corona Dashboard", page_icon=":earth_asia:", layout="wide")


# Use Local Contact CSS File
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_style = current_dir / "styles" / "style.css"
image1 = current_dir / "images" / "image1.png"
image2 = current_dir / "images" / "image2.png"

with open(css_style) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---- MAINPAGE ----
page_title = "Covid-19 DashBoard"
text_style = f"<h1 style='font-family:Georgia, serif; text-align:center; color:#4169e1; font-size:45px;'>{page_title}</h1>"
st.markdown(text_style, unsafe_allow_html=True)


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
                              'Deaths - newly reported in last 24 hours'], index_col=False,
                     dtype={'Cases - cumulative total': int}
                     ).sort_values(by='Cases - newly reported in last 24 hours', ascending=False)
    return df


@st.cache
def covid19_vaccination():
    df = pd.read_csv('https://covid19.who.int/who-data/vaccination-data.csv',
                      usecols=['COUNTRY', 'DATE_UPDATED', 'TOTAL_VACCINATIONS',
                               'PERSONS_VACCINATED_1PLUS_DOSE_PER100',
                               'PERSONS_FULLY_VACCINATED_PER100',
                               'PERSONS_BOOSTER_ADD_DOSE_PER100',
                               'VACCINES_USED',
                               'PERSONS_VACCINATED_1PLUS_DOSE'])
    return df


# ---- DataFrames ----
daily_cases_df = covid19_daily_cases()
cumulative_df = covid19_cumulative()
vaccination_df = covid19_vaccination()
global_covid_data = cumulative_df.loc[cumulative_df['Name'] == 'Global']

# Global Covid KPI's
page_title = "Global Covid Tracker"
text_style = f"<h1 style='font-family:Georgia, serif; text-align:left; color:#c4c3d0; font-size:30px;'>{page_title}</h1>"
st.markdown(text_style, unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5, gap='small')
col1.metric("Total Vaccination", numerize.numerize(vaccination_df['TOTAL_VACCINATIONS'].sum()))
col2.metric("Cases In Last 24 Hours",
            numerize.numerize(int(global_covid_data['Cases - newly reported in last 24 hours'])))
col3.metric("Cases (Cumulative Total)", numerize.numerize(int(global_covid_data['Cases - cumulative total'])))
col4.metric("Deaths In Last 24 Hours",
            numerize.numerize(int(global_covid_data['Deaths - newly reported in last 24 hours'])))
col5.metric("Deaths (Cumulative Total)", numerize.numerize(int(global_covid_data['Deaths - cumulative total'])))

# ---- Plotting Graphs at world level ----
top_country_cases = cumulative_df[1:11][['Name',
                                         'Cases - newly reported in last 24 hours',
                                         'Deaths - newly reported in last 24 hours',
                                         'Cases - newly reported in last 7 days',
                                         'Deaths - newly reported in last 7 days'
                                         ]].set_index(['Name'])

tab1, tab2, tab3, tab4 = st.tabs(["Newly Reported Cases In Last 24 hours",
                                  "Newly Reported Deaths In Last 24 hours",
                                  "Reported Cases In Last 7 Days",
                                  "Reported Deaths In Last 7 Days"])
with tab1:
    st.bar_chart(top_country_cases['Cases - newly reported in last 24 hours'])
with tab2:
    st.bar_chart(top_country_cases['Deaths - newly reported in last 24 hours'])
with tab3:
    st.bar_chart(top_country_cases['Cases - newly reported in last 7 days'])
with tab4:
    st.bar_chart(top_country_cases['Deaths - newly reported in last 7 days'])

# ---- Country Wise Covid KPI's ----
col1, col2, col3 = st.columns([4, 3, 3])

with col1:
    st.write('')
    page_title = "Country Covid Tracker : "
    text_style = f"<h1 style='font-family:Georgia, serif; text-align:left; color:#c4c3d0; font-size:30px;'>{page_title}</h1>"
    st.markdown(text_style, unsafe_allow_html=True)
with col2:
    country_list = cumulative_df['Name'].values
    selected_country = st.selectbox("", country_list, index=1)
with col3:
    pass

col1, col2, col3, col4, col5 = st.columns(5, gap='small')
with col1:
    if selected_country == 'Global':
        temp = vaccination_df['TOTAL_VACCINATIONS'].sum()
    else:
        temp = vaccination_df.loc[vaccination_df['COUNTRY'] == selected_country]['TOTAL_VACCINATIONS']
    col1.metric("Total Vaccination", int(temp))
with col2:
    temp = cumulative_df.loc[cumulative_df['Name'] == selected_country]['Cases - newly reported in last 24 hours']
    col2.metric("Cases In Last 24 Hours", int(temp))
with col3:
    temp = cumulative_df.loc[cumulative_df['Name'] == selected_country]['Cases - cumulative total']
    col3.metric("Cases (Cumulative Total)", int(temp))
with col4:
    temp = cumulative_df.loc[cumulative_df['Name'] == selected_country]['Deaths - newly reported in last 24 hours']
    col4.metric("Deaths In Last 24 Hours", int(temp))
with col5:
    temp = cumulative_df.loc[cumulative_df['Name'] == selected_country]['Deaths - cumulative total']
    col5.metric("Deaths (Cumulative Total)", int(temp))

# ---- DataFrame Country wise ----
df = daily_cases_df.loc[daily_cases_df['Country'] == selected_country]

tab1, tab2, tab3, tab4 = st.tabs(["New  Cases  Per  Day",
                                  "Cumulative  Cases",
                                  "Deaths per Day",
                                  "Cumulative  Deaths"])
with tab1:
    # ---- Daily New Cases [Line Chart] ----
    fig_daily_cases = px.line(df,
                              x='Date_reported',
                              y='New_cases',
                              color_discrete_sequence=["#0083B8"],
                              template="plotly_white")
    fig_daily_cases.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))
    tab1.plotly_chart(fig_daily_cases)
with tab2:
    # ---- Cumulative Cases [Line Chart] ----
    fig_cases_cumsum = px.area(df,
                               x='Date_reported',
                               y='Cumulative_cases',
                               color_discrete_sequence=["#0083B8"],
                               template="plotly_white")
    fig_cases_cumsum.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))
    tab2.plotly_chart(fig_cases_cumsum)
with tab3:
    # ---- Deaths In Last 24 Hours [Line Chart] ----
    fig_deaths_in_24hours = px.line(df,
                                    x='Date_reported',
                                    y='New_deaths',
                                    color_discrete_sequence=["#0083B8"],
                                    template="plotly_white")
    fig_deaths_in_24hours.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))
    tab3.plotly_chart(fig_deaths_in_24hours)
with tab4:
    # ---- Cumulative Deaths [Line Chart] ----
    fig_deaths_cumsum = px.area(df,
                                x='Date_reported',
                                y='Cumulative_deaths',
                                color_discrete_sequence=["#0083B8"],
                                template="plotly_white")
    fig_deaths_cumsum.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))
    tab4.plotly_chart(fig_deaths_cumsum)

# Country Covid Vaccine KPI's
para_title = f'{selected_country} Covid Vaccine Tracker'
text_style = f"<h1 style='font-family:Georgia, serif; text-align:left; color:#8c92ac; font-size:20px;'>{para_title}</h1>"
st.markdown(text_style, unsafe_allow_html=True)

# Vaccine DataFrame
vacc_df = vaccination_df.loc[vaccination_df['COUNTRY'] == selected_country]

col1, col2 = st.columns([4, 4])
with col1:
    para_title = 'Vaccines Used For Vaccination :'
    text_style = f"<h1 style='font-family:Georgia, serif; text-align:left; color:#c4c3d0; font-size:15px;'>{para_title}</h1>"
    st.markdown(text_style, unsafe_allow_html=True)
    # Vaccine list
    vacc_list = vacc_df['VACCINES_USED'].iloc[0]
    for vaccine in vacc_list.split(','):
        st.write(f'- {vaccine}')

with col2:
    para_title = f"Cumulative Vaccination (At-least Single Dose): {numerize.numerize(int(vacc_df['PERSONS_VACCINATED_1PLUS_DOSE']))}"
    text_style = f"<h1 style='font-family:Georgia, serif; text-align:left; color:#c4c3d0; font-size:15px;'>{para_title}</h1>"
    st.markdown(text_style, unsafe_allow_html=True)

    # Labels for Donut
    labels = ['Fully Vaccinated', 'Not Vaccinated']
    # Values for Donut
    fully_vacc = vacc_df['PERSONS_FULLY_VACCINATED_PER100'].iloc[0]
    not_vacc = 100 - fully_vacc
    values = [fully_vacc, not_vacc]
    # Figure for Donut
    fig = go.Figure(data=[go.Pie(labels=labels, values=values,
                                 hole=.5, hoverinfo="label+percent")])
    col2.plotly_chart(fig)

# ---- Down Image ----
img1 = Image.open(image1)
col1, col2, col3 = st.columns([.5, 9, .5])
col2.image(img1, use_column_width=True)

img2 = Image.open(image2)
col1, col2, col3 = st.columns([.5, 9, .5])
col2.image(img2, use_column_width=True)


# Other Useful links
col1, col2, col3 = st.columns([6.5, 3, .5])
with col2:
    with st.expander("Other Useful links"):
        links = {
            "www.mohfw.gov.in": "https://www.mohfw.gov.in/",
            "www.covid19.who.int/": "https://covid19.who.int/"
                }
        for web_name, url in links.items():
            st.write(f"[🔗 {web_name}]({url})")


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
