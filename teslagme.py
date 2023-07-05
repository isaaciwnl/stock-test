import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# MAKE_GRAPH
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    
    revenue_data_specific["Revenue"] = revenue_data_specific["Revenue"].str.replace(',', '').str.replace('$', '').astype(float)  # Convert Revenue column to float
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)
    fig.show()

# TSLA
tesla = yf.Ticker("TSLA")
tesla_data = pd.DataFrame(tesla.history(period="max"))
tesla_data.reset_index(inplace=True)
tsla_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
tsla_html_data = requests.get(tsla_url).text
tesla_beautiful_soup = BeautifulSoup(tsla_html_data, "html.parser")
tesla_revenue = pd.DataFrame(columns=["Date","Revenue"])
quarter_table_tsla = tesla_beautiful_soup.find_all("tbody")[1]

for row in quarter_table_tsla.find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    
    tesla_revenue = tesla_revenue._append({"Date":date, "Revenue":revenue}, ignore_index=True) 

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"") 
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
make_graph(tesla_data, tesla_revenue, 'Tesla')


# GME
gme = yf.Ticker("GME")
gme_data = pd.DataFrame(gme.history(period="max"))
gme_data.reset_index(inplace=True)
gme_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
gme_html_data = requests.get(gme_url).text
gme_beautiful_soup = BeautifulSoup(gme_html_data, "html.parser")
gme_revenue = pd.DataFrame(columns=["Date","Revenue"])
quarter_table_gme = gme_beautiful_soup.find_all("tbody")[1]

for row in quarter_table_gme.find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    
    gme_revenue = gme_revenue._append({"Date":date, "Revenue":revenue}, ignore_index=True) 

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"") 
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
make_graph(gme_data, gme_revenue, 'GameStop')
