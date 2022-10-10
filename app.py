from dash import dash, dcc, html, dcc, Input, Output, State
from dash.dependencies import Input, Output 

import pandas as pd

import numpy as np

import plotly.graph_objects as go
import plotly.express as px

import datetime
from datetime import timedelta

#import os, psutil


import dash

app = dash.Dash()
server = app.server

df_cidades = pd.read_csv('df_cidades.csv')
df = pd.read_csv('datasets/4100103.csv', compression='gzip')
df_inf_atuais = pd.read_csv('inf_atuais.csv', compression='gzip')


base = datetime.date(2020,3,1) 
date_list = [base + timedelta(days=x) for x in range(808)]
date_list=pd.to_datetime(date_list)


def init_time_graph_positive(a):
    """_summary_

    Args:
        a (int): um número inserido pelo usuario

    Returns:
        _type_: se esse numero for menor que 0 retorna 0
    """
    if a<0:
        a=0
        return a 

app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),

        dcc.Dropdown( id = 'dropdown',
        options = [{'label':row['nome_cidades'], 'value':row['codigos_ibge'] } for index, row in df_cidades.iterrows()],
        value = '4100103'),

        dcc.Dropdown( id = 'dropdown2',
        options = [{'label':var.strftime('%d/%m/%Y'), 'value':index } for index, var in enumerate(date_list)],
        value = '1'),
        dcc.Graph(id = 'bar_plot')
    ])

@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value'),\
               Input(component_id='dropdown2', component_property= 'value')])
def graph_update(dropdown_value,dia_do_ano):
#    print(dropdown_value)
    
#    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    if dia_do_ano == None:
        dia_do_ano = 0

    if dropdown_value == None:
        dropdown_value = 4100103
    df = pd.read_csv(f'datasets/{dropdown_value}.csv', compression='gzip')

    
    fig = go.Figure([go.Scatter(x = date_list[int(dia_do_ano):], y = np.fromstring(df['{}'.format(dropdown_value)][int(dia_do_ano)].replace('\n','').replace('[','').replace(']',''), dtype=float, sep='  '),\
                     line = dict(color = 'firebrick', width = 2)),\
                     go.Scatter(x = date_list, y = df_inf_atuais['{}'.format(dropdown_value)],\
                     line = dict(color = 'gray', width = 2))   
                     ])

    graph_y_max = df_inf_atuais['{}'.format(dropdown_value)].max() * 1.1
    
    fig.update_layout(title = 'Predição do Espalhamento da Covid-19 na cidade de {} no dia {}.'.format(df_cidades[df_cidades.codigos_ibge==4100103]['nome_cidades'].item(),date_list[int(dia_do_ano)].strftime('%d/%m/%Y')),
                      xaxis_title = 'Dia',
                      yaxis_title = 'Infectados Atuais',
                      yaxis_range = [-graph_y_max * 0.1,graph_y_max],
                      xaxis_range = [date_list[init_time_graph_positive(int(dia_do_ano)-50)],date_list[807]]
                      )
    
#    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)


    return fig  



if __name__ == '__main__': 
    app.run_server()

