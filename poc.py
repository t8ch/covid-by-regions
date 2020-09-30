#!/usr/bin/env python
# coding: utf-8

# In[8]:


get_ipython().system(' jupyter nbconvert --to python poc.ipynb')


# In[11]:


import pandas as pd
import requests
import plotly
import plotly.graph_objs as go


# In[31]:


url = "https://pt.wikipedia.org/wiki/Predefinição:Tabela_Covid-19_Portugal_região/dia_(DGS)"

r = requests.get(url, auth=('user', 'pass'))
website = r.text
tables = pd.read_html( website, encoding="UTF-8")
table = tables[0]


# In[32]:


table


# In[33]:


# select relevant columns and drop last helper rows
table = table[['data','Madeira']].drop(table.tail(4).index)
table 


# In[34]:


# drop unneeded levels 
table.columns = table.columns.droplevel([0,1])
table


# In[35]:


table = table.loc[:,['Σ', 'Δ']]


# In[36]:


table


# In[37]:


# create new, proper date column, starting from March 1st; assuming update each day
start_date = '2020-03-03'
end_date = pd.to_datetime(start_date) + pd.DateOffset(days=len(table)-1)
dates = pd.date_range(start_date, end=end_date)


# In[38]:


table['date'] = pd.Series(dates, index=table.index).values
table


# In[39]:


trace = go.Scatter(x=table['date'], y=table['Σ'], name='sum of COVID cases')
data = [trace]

updatemenus = list([
    dict(active=1,
         buttons=list([
            dict(label='Log Scale',
                 method='update',
                 args=[{'visible': [True]},
                       {'title': 'Log scale',
                        'yaxis': {'type': 'log'}}]),
            dict(label='Linear Scale',
                 method='update',
                 args=[{'visible': [True]},
                       {'title': 'Linear scale',
                        'yaxis': {'type': 'linear'}}])
            ]),
        )
    ])

layout = dict(updatemenus=updatemenus, title='Linear scale')
fig = go.Figure(data=data, layout=layout)

plotly.offline.iplot(fig)


# In[ ]:




