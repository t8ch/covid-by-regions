import streamlit as st
import pandas as pd
import requests
import plotly
import plotly.graph_objs as go


# import table
url = "https://pt.wikipedia.org/wiki/Predefinição:Tabela_Covid-19_Portugal_região/dia_(DGS)"

r = requests.get(url, auth=('user', 'pass'))
website = r.text
tables = pd.read_html( website, encoding="UTF-8")
table = tables[0]



# select relevant columns and drop last helper rows
table = table[['data','Madeira']].drop(table.tail(4).index)

# drop unneeded levels 
table.columns = table.columns.droplevel([0,1])
table = table.loc[:,['Σ', 'Δ']]

# create new, proper date column, starting from March 1st; assuming update each day
start_date = '2020-03-03'
end_date = pd.to_datetime(start_date) + pd.DateOffset(days=len(table)-1)
dates = pd.date_range(start_date, end=end_date)

table['date'] = pd.Series(dates, index=table.index).dt.date.values

#### app content
st.header('Madeira COVID cases')

# st.dataframe(table.T, height= 600)

# plotting
fig = plotly.tools.make_subplots(rows=2, cols=1,
                    shared_xaxes=True, 
                    vertical_spacing=0.02)

trace = go.Scatter(x=table['date'], y=table['Σ'], name='sum of COVID cases')
trace2 = go.Bar(x=table['date'], y=table['Δ'], name='diff. of COVID cases')
data = [trace, trace2]

updatemenus = list([
    dict(x = 0,
        xanchor='left',
        yanchor = 'bottom',
        active=1,
         buttons=list([
            dict(label='Log Scale',
                 method='update',
                 args=[{'visible': [True, True]},
                       {'title': 'Log scale',
                        'yaxis': {'type': 'log', 'domain': [0.35, 1]}}
                        ])
                        ,
            dict(label='Linear Scale',
                 method='update',
                 args=[{'visible': [True, True]},
                       {'title': 'Linear scale',
                        'yaxis': {'type': 'linear', 'domain': [0.35, 1]}}])
            ]),
        )
    ])

layout = dict(updatemenus=updatemenus, title='Linear scale', width = 900, height=700, autosize=False,
                yaxis1=dict(domain=[0.35, 1]), yaxis2=dict(domain=[0, .3]),
               )
fig.update_layout(layout)

fig.add_trace(trace, row=1, col=1)
fig.add_trace(trace2, row=2, col=1)

st.plotly_chart(fig, use_container_width=False)

# st.plotly_chart(go.Figure(go.Bar(x=table['date'], y=table['Δ'], name='diff. of COVID cases')))

