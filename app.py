# Run with terminal command 'python3 app.py'
# View at http://127.0.0.1:8050/ in your web browser

# Potential extra installs:
## dash_daq
## dash_table
## dash_bootstrap_components

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


import plotly.express as px

import dash_daq as daq


# Load tsv file
deaths_df = pd.read_csv('data/choleraDeaths.tsv', sep='\t')

# Rename columns; modify original
deaths_df.rename(
    columns = {'Date': 'Date', 'Attack': 'Daily Attacks', 'Death': 'Daily Deaths'},
    inplace = True
)

# Create new columns with running totals of attacks and deaths
# Referenced https://www.geeksforgeeks.org/cumulative-sum-of-a-column-in-pandas-python/
attacks_cumul = deaths_df['Daily Attacks'].cumsum()
deaths_cumul = deaths_df['Daily Deaths'].cumsum()

# Insert cumulative columns into a new dataframe.
deaths_graph_df = deaths_df.copy()
deaths_graph_df.insert(2, 'Cumulative Attacks', attacks_cumul)
deaths_graph_df.insert(4, 'Cumulative Deaths', deaths_cumul)

deaths_graph = px.line(
    deaths_graph_df, 
    x='Date', 
    y=deaths_graph_df.columns)

app = dash.Dash(__name__)




app.layout = html.Div(
    # className = 'app-layout',
    children = [

    html.H1(
        'ICS 484 - Project 1 - Cholera Deaths Visualization',
        className = 'main-title',
    ),

    # Referenced https://stackoverflow.com/questions/50213761/changing-visibility-of-a-dash-component-by-updating-other-component
    html.Div(
        id = 'extra-info',
        children = [
            html.H4('Select extra project info to show'),
            dcc.Dropdown(
                id = 'extra-info-dropdown',
                options = [
                    {'label': 'Data\'s Origin', 'value': 'origin'},
                    {'label': 'Visualization Tools & Libraries', 'value': 'tools'},
                    {'label': 'Author', 'value': 'author'},
                    {'label': 'None', 'value': 'none'},

                ]),
            html.Div(id = 'extra-info-box')
        ]
    ),
    html.H4(
        'Include cumulative counts?',
    ),
    html.Div(
        daq.ToggleSwitch(
            id = 'cumul-toggle',
            value = False,
            color = 'green',
        ),
        style = {
            'width': '200px',
            'margin': 'auto',
        },
    ),

    dcc.Slider(
        id = 'days-slider',
        min = 1,
        max = deaths_df.shape[0],
        step = 1,
    ),

    html.Div(
        dt.DataTable(
            id = 'deaths-table',
            data = deaths_df.to_dict('records'),
            columns = [{'name': i, 'id': i} for i in deaths_df.columns],
            style_data_conditional = [{
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_cell = {
                'font-family': 'Avenir',
            },
            style_header = {
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        ),
        style = {
            'margin': 'auto',
            'width': '60%',
        }
    ),

    dcc.Graph(
        id = 'deaths-graph',
        figure = deaths_graph

    )
])

extra_info_dict = {
    'origin': 'Data were created and compiled by Robin Wilson in January 2011.  For more info, see www.rtwilson.com/academic.  Contact: robin@rtwilson.com',
    'author': 'This visu',
    'tools': 'This visualization primarily uses Dash, a python library that uses Plotly for underlying graphics.',
    'none': ''
}

@app.callback(
   Output('extra-info-box', 'children'),
   Input('extra-info-dropdown', 'value'))
def choose_extra_info(choice):
    if choice and extra_info_dict[choice]:
        return extra_info_dict[choice]
    return ""




# @app.callback(
#     Output('deaths-table', 'deaths-graph'),
#     [Input()]
# )
# def update_chart()

if __name__ == '__main__':
    app.run_server(debug=True)