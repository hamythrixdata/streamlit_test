import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

st.title("Stock Dashboard")
ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

data = yf.download(ticker, start = start_date, end = end_date)
fig = px.line(data, x = data.index, y = data["Adj Close"], title = ticker)
st.plotly_chart(fig)

pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News"])

with pricing_data:
    st.header("Price Movement")
    data2 = data
    data2["% Change"] = data["Adj Close"] / data["Adj Close"].shift(1) - 1
    data2.dropna(inplace = True)
    st.write(round(data2,4))
    annual_return = data2["% Change"].mean()*252*100
    st.write('#1. Annual Return is', round(annual_return,4), '%')
    stdev = np.std(data2["% Change"])*np.sqrt(252)
    st.write('#2. Standard Deviation is', round(stdev*100,4), '%')
    st.write('#3. Risk Adj. Return is ', round(annual_return/(stdev*100),4))


# from alpha_vantage.fundamentaldata import FundamentalData
# with fundamental_data:
#     key = "GX5FR866282PD116"
#     fd = FundamentalData(key, output_format = "pandas")
#     st.header("Balance Sheet")
#     balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
#     bs = balance_sheet.T[1:]
#     bs.columns = list(balance_sheet.T.iloc[0])
#     bs_trimmed = bs.iloc[:, :3]
#     st.write(bs_trimmed.round(2))
#     st.subheader("Income Statement")
#     income_statement = fd.get_income_statement_annual(ticker)[0]
#     is1 = income_statement.T[1:]
#     is1.columns = list(income_statement.T.iloc[0])
#     is1_trimmed = is1.iloc[:, :3]
#     st.write(is1_trimmed.round(2))
#     st.subheader("Cash Flow Statement")
#     cash_flow_statement = fd.get_cash_flow_annual(ticker)[0]
#     cs = cash_flow_statement.T[1:]
#     cs.columns = list(cash_flow_statement.T.iloc[0])
#     cs_trimmed = cs.iloc[:, :3]
#     st.write(cs_trimmed.round(2))

from stocknews import StockNews
with news:
    st.header(f"Top 10 News of {ticker}")
    sn = StockNews(ticker, save_news= False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f"News {i + 1}")
        st.write(df_news["published"][i])
        st.write(df_news["title"][i])
        st.write(df_news["summary"][i])
        title_sentiment = df_news["sentiment_title"][i]
        st.write(f"Title Sentiment {title_sentiment}")
        news_sentiment = df_news["sentiment_summary"][i]
        st.write(f"News Sentiment {news_sentiment}")

# from pyChatGPT import ChatGPT
# session_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..qwVeyeABAiE7ckYz._pUA8u9L3dxUTbyZeEZqoLbBCf1a8suf05umi4HPe70BrXCsLHbqgKQu8jwk-22HJ1bhxXfn1U3i7rEv3ECuXjIOjYGfOFNRRX2J_QMDVzr1F-34bwlSLYVPoygovIAtPtYoR2zdpBBb0nQXDQTET_yTQfaW4X1g341uzC2c9esBKPukPErEUt38Sf_H8Ut9p2awGSVUM9dmRjctNrM_RgRY_NPwQVV9QwVAsxB96nL1LY3EHN1PqjrBOufKK2-lm16h1EFsQfsjZ6SzEDH2Wf6s8UN-o_3xK8e2cZGlpybvKZ1TJg8-LB09uZQo8GG0ALY9xvQAP6tmUiOWTe8r-V2oTPAvTkiAhsLE8SlthKsRzryoVE_iZsshwxj3cwhi16URF0b9nqQcndXx9kYT3VwDYjZxQ8n5Xh6kVJYdnZVJG3t7ekMGqd9VXB78YUef6AymUgebuABDkQ6_ZWIERMmMpszv2PvH50C1Tf909sw3qZGbYPxouAHCzr_Dmi9GvKLdrkndL2TzQGzADAglSe7AVLMEFl9Y7eaeUkd3pgx-wErdSCthCxTXnKzOlKGKfb1QyJHJwwhcyUzDkd4cqtrNMTmF-CgVbheSv9HxEfH2h9tXfdeyh1Yd_vxZk24c2YrIOgZDCk4gyfAE8-rKiKYVenSvtFHlZZ_osaM2u_aSRm5bQg-C3-A1kqOXISU3f5QYJYBwAO2Hrbj0SimZZp8gKNp2sW0dBPQ133QAVM4yv_fkmgrSqQZrRQDLWyhXMlLgU9atRkJhL9S7Zt69YWKcS1tqnMZMOhr21SoN59xu6-55-pYV19yDhDi5NUW0ktaC984iicMKGzCU5j_wuVWiErNVGkCqbNe2sYlP32enEj-a0t6r4kmaGlKjG9j3tZq-eUWSHMeXSCxwRWorKQ7BpU5HE22wNbleg0kyCCaH0d5-uso0hieV3qh77AkO2PygcKYQrC3t8DPVlChfgpyVkVDweYfNiGAL-oc4XqwwSZIRrdIdYW8iiDiZ3kFVIbQfXOtNQQ-n7mjp6nwh2y9Xol7vy-qy4GEvSxbuIY29SuxN3x2Y4ZtIIr_tGPEj1muqqnXHGkFxrIR-FvdrCuXRnc6vHGmJVIKmcI43It6wknim5m7cwFUFONHBdVQrK5wASXfqx_zycDkuNl8pyuBNcnHeDSEXKCGKG3ZukKoMN60pOzdi5DMEJSZNJ7HRCsQDeQOWmDS20dz4N2yl6GQPAw6uxp01gsANaMPMZgY5mLAJgYnucQoEgG7u8ctMH9W6siARapl3AuBMDhv17k5rs4oBbGNfulR_pLllcY7CmlmcCebumgHawk_cKkEnWCIAGbGRvIsGJjQnL9WMWkkcz0wUmveQpVDt0fd8usTLQayDlci41M7wxmrwaakGuUwzbqk_CDtGHXH02ruZJ3-aC40g_3GAqTXi2_BeycHbB5_2c2g0hIluv0S171kV_ZXLZVT3Ml9fBWoLo3KXz1Qp82jjYyCbPsPOuVWbd4lVivfCOAIMJwDTgB6_GYl8IEnOOt-mepgkuXKi8gzBP3C1jnayU76ccjXPATQaJlB7AXdAOe-YZOcBkzKKU9zD8MEAVxgg_ckaoMwu5Hfwf0eLl_0lPLz85VrZPoMycsmPE8NgkL1Qke1xF4Kh9HzXD-YoabJeVjXVhwoUG520o_ozGq7KTXeZItFBt37LNXz4sRhg2YLSg51b3mXV6bVqLMMopt7DQPLpoHgn9nloXAGRfcfQddITggbAdK_DDqIR6uBNa4xhTUzV8MUpUnslRJD3v59X6phOx1YdCNKMGpbM80F1biYbD879DHY6g1b1tfUfaioumFnYMuJubptaeqJS4qfj762UlKEAfDstoBwWTcVNJqW_1oCn7oJ1xZjSI9zkfTbXlIC1OKcw7NlC7Lhau8BDAUbkamV8fW6ywpoS6kDiwQPxnemoFk_DcGGHNm-9k1kRKdDvBz_rBMSVPYgvtmowJUAamw50Tc9P0FeDQ9lYx0s7qTiSyWVCcxtCoPJpry8d2P4_kyQVtA-i1ACb70u0KqDw1HuwJ8F-T9iGNXXe0gsOYQUXkEniu5Yal_G7OOs78JrSsXr9jfpaM7ourDwY4jSwAYdxl2eJwig_Tts0ETFfUkoQGTthU5vIxtcuqlbQjxoezBxhUZO47kKTSzYafxPb9ceYVgoIq9sQTaUw1z7Ij9v2Q1lRxOYL0EFk2XzB5UcxnMPSG4AXmbn0igTLH6eab488BqXyPN_r4OK44TG3WK6bas6VJxOHR3tuYiwDAauKfrFDSgHT8tRdqBc6Ls8JfU8VcbP137pJItiT_ztxyeSVARgGsr2OfCNoAtEjUo7108ZWDwl8lf4rU0liuvV-dtSE5aR3BNHRaspT1_Wfu8Zsm68eXKcIufBCCY80zbq2jhRvfWdUaCSd-X-J24L7BjlbrD8ivVdyw07C07QM5mEQKYW7J5Cklyxil9aGo82I-4tgrpM2JrVU0ndi07GX9piqpGO2kvmfXXVNwt2ulj4zMCj_qb5FkLsuBfbnOITEwPc4SA1h244RWFdO6Cqreo7NxR04BK2tIZV6xVT6QcLMsv17jLg80SCUqwFCSbihv5E5dF_2iojtzFWIlmYRAzNw-A4tf-Uqy0h1L4g185MRFcpd-L7P_-Jxr7FGLspBC26nxL6loi6kBhTfAIjcXie_EmTOU_CFj1kjAcn9tUUpgN_D9K53YP4KCBrBi5r_AEdDDljFQq6Cs-zK-NFDc12LyOY8hhPEQik8UT5eeynGttgBsDQlnmAiSAUhrW3iEVYm1dnYzOD9CNBb9vUCqJkpQ2BgXK6tXAGoJ02HPIyjimgkNJM1w7EGmN7t79QD5FfG4fo1r4j8PmFiNvdb-Rg1bT0_q4KtGM1Zcg8GfFfzTU9-HFug5ki1NiCatv_aFPWsr0DnJ8xZvq3JltQTA7cPDY-3xCM_aMwIrTesIryPBvlRczrNwnB6WjZMh4_qFK7jEI85NB0.l127m6lqV1vyN6n7sotG_g"
# api2 = ChatGPT(session_token)
# buy = api2.send_message(f'3 Reasons to buy {ticker} stock')
# sell = api2.send_message(f'3 Reasons to sell {ticker} stock')
# swot = api2.send_message(f'SWOT Analysis of {ticker} stock')

# with openai1:
#     buy_reason, sell_reason, swot_analysis = st.tabs(["3 Reasons to buy", "3 Reasons to sell", "SWOT Analysis"])

#     with buy_reason:
#         st.subheader(f'3 reasons for buying {ticker} stock')
#         st.write(buy['message'])
#     with sell_reason:
#         st.subheader(f'3 reasons for selling {ticker} stock')
#         st.write(sell['message'])
#     with swot_analysis:
#         st.subheader(f'SWOT Analysis for {ticker} stock')
#         st.write(swot['message'])

    
