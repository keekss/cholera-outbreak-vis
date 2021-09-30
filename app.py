# Run with terminal command 'python3 app.py'
# View at http://127.0.0.1:8050/ in your web browser

# Note: you may need to install additional libraries
# if using a virtual environment, e.g.:
## dash
## dash_bootstrap_components
## dash_daq

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go

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
# Delete dates; use integers 0 to 41 instead to represent
# days since August 19, 1854
deaths_graph_df.drop(columns=['Date'], axis=0, inplace=True)

deaths_graph = px.line(
    deaths_graph_df,
    # leave out x variable since it is (0,1,...n) by default
    y=deaths_graph_df.columns,
)
deaths_graph.update_layout(
    title='Cholera Attacks and Deaths in London',
    xaxis_title = 'Days Elapsed Since August 19, 1854',
    yaxis_title = 'Number of People',
    legend_title = '',
)

naples_df = pd.read_csv(
    'data/naplesCholeraAgeSexData.tsv',
    sep='\t',
    skiprows = 6
)

age_groups = naples_df['age']

naples_graph = go.Figure(data=[
    go.Bar(name='Male', x=age_groups, y=naples_df['male']),
    go.Bar(name='Female', x=age_groups, y=naples_df['female'])
])

naples_graph.update_layout(barmode='group')

census_df = pd.read_csv('data/UKcensus1851.csv', skiprows=3)


pump_locs_df = pd.read_csv('data/choleraPumpLocations.csv')

death_locs_df = pd.read_csv('data/choleraDeathLocations.csv', error_bad_lines=False)


death_locs_graph = px.scatter_geo(
    death_locs_df,
    lon = death_locs_df.iloc[:,1],
    lat = death_locs_df.iloc[:,2],
    size = death_locs_df.iloc[:,0]
)


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
        className = 'graph-box',
        children = [
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
            )],
        style = {
            'margin': 'auto',
            'width': '60%',
        }
    ),

    dcc.Graph(
        className = 'graph',
        figure = deaths_graph,
    ),

    dcc.Graph(
        className = 'graph',
        figure = naples_graph
    ),

    dcc.Graph(
        className = 'graph',
        figure = death_locs_graph
    ),
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