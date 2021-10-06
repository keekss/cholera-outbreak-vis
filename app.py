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
from plotly.express import data
import dash_daq as daq
from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
    # Customize colors
    # Referenced https://community.plotly.com/t/plotly-express-line-chart-color/27333/4
    color_discrete_map = {
        'Daily Attacks':        'blue',
        'Cumulative Attacks':   'darkblue',
        'Daily Deaths':         'red',
        'Cumulative Deaths':    'darkred',
    },
)

deaths_graph.update_layout(
    title='Attacks & Deaths in London vs. Time',
    title_x = 0.5,
    xaxis_title = 'Days Elapsed Since August 19, 1854',
    yaxis_title = 'Number of People',
    legend_title = '',
)

# Make cumulative lines dotted
# Referenced https://stackoverflow.com/questions/67064045/plotly-highlight-line-with-dotted-dash-and-marker-with-fig-update-traces?rq=1
deaths_graph.update_traces(
    patch = {
        'line': {'dash': 'dot'},
    },
    selector = {
        'legendgroup': 'Cumulative Attacks',
    },
)
deaths_graph.update_traces(
    patch = {
        'line': {'dash': 'dot'},
    },
    selector = {
        'legendgroup': 'Cumulative Deaths',
    },
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

naples_graph.update_layout(
    barmode='group',
    title='Deaths in Naples vs. Age Group and Gender',
    title_x = 0.5,
    xaxis_title = 'Age Group (Years)',
    yaxis_title = 'Deaths (Number of People)'
)

census_df = pd.read_csv('data/UKcensus1851.csv', skiprows=3)

# Make side-by-side pie charts for age groups grouped by gender
# Referenced https://plotly.com/python/pie-charts/
census_graph = make_subplots(
    rows = 1,
    cols = 2,
    specs=[[{'type':'domain'}, {'type':'domain'}]],
    subplot_titles = ('Male', 'Female'),
)
census_graph.add_trace(
    go.Pie(
        labels = census_df['age'],
        values = census_df['male'],
        name = 'Male',
    ), 1,1
)
census_graph.add_trace(
    go.Pie(
        labels = census_df['age'],
        values = census_df['female'],
        name = 'Female',
    ), 1, 2
)
census_graph.update_traces(hole=.3, hoverinfo="label+percent+name")

census_graph.update_layout(
    title_text="Age Groups by Gender",
    # Add annotations in the center of the donut pies.
    # annotations=[dict(text='Male', x=0.18, y=0.5, font_size=20, showarrow=False),
    #              dict(text='Female', x=0.82, y=0.5, font_size=20, showarrow=False)]
)

pump_locs_df = pd.read_csv('data/choleraPumpLocations.csv')
pump_lons = pump_locs_df.iloc[:,0]
pump_lats = pump_locs_df.iloc[:,1]


death_locs_df = pd.read_csv('data/choleraDeathLocations.csv', error_bad_lines=False)
death_lons = death_locs_df.iloc[:,1]
death_lats = death_locs_df.iloc[:,2]

death_locs_graph = px.scatter_geo(
    death_locs_df,
    lon = death_lons,
    lat = death_lats,
    size = death_locs_df.iloc[:,0]
)
death_locs_graph.add_traces(go.Scattergeo(
    lon = pump_lons,
    lat = pump_lats,
))

death_locs_graph.update_geos(fitbounds='locations')

# death_lons = death_locs_df.iloc[:,1]
# death_lats = death_locs_df.iloc[:,2]

# layout = go.Layout(
#     yaxis=dict(
#         range=[0, 100]
#     ),
#     xaxis=dict(
#         range=[100, 200]
#     )
# )

app = dash.Dash(__name__)

app.layout = html.Div(
    html.Section(children = [
        html.Section(children = [
            html.Div(
                id = 'title-container',
                children = [
                html.H1(
                    'Cholera Deaths Visualization',
                    id = 'main-title',
                ),
                html.H5(
                    'ICS 484 - Project 1 - Kiko Whiteley, Fall 2021',
                    id = 'subtitle'
                ),
                html.H3(
                    'Visualizing reported symptoms (attacks) of Cholera and related deaths along with population features in London and Naples for 42 days, beginning on August 19, 1854.'
                )
            ]),
            html.Div(
                id = 'extra-info-container',
                children = [
                html.H2('Extra Info - Select'),
                dcc.Dropdown(
                    id = 'extra-info-dropdown',
                    options = [
                        {'label': 'Data\'s Origin', 'value': 'origin'},
                        {'label': 'Visualization Tools & Libraries', 'value': 'tools'},
                        {'label': 'Author', 'value': 'author'},
                        {'label': 'None', 'value': 'none'},
                    ]
                ),
                html.H3(id = 'extra-info-text')
            ])
        ]),
        dcc.Tabs(
        id = 'tabs',
        parent_className = 'custom-tabs',
        className = 'custom-tabs-container',
        children = [
            dcc.Tab(
                label = '1: Daily & Cumulative Incidents',
                value = 'tab-1',
                className = 'graph-tab',
                children = [
                    html.Div(id = 'deaths-table', children = [
                        dt.DataTable(
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
                        )
                    ]),
                    html.Div(id = 'deaths-graph', children = [
                        dcc.Graph(
                            # className = 'graph',
                            figure = deaths_graph,
                        ),
                    ])    
                ]
            ),
            dcc.Tab(
                label = '2A: Gender-grouped Chart of Deaths in Naples During the Same Time Period',value = 'tab-2a',
                className = 'graph-tab',
            ),
            dcc.Tab(
                label = '2B: Gender-grouped Breakdown of Age Groups from the 1851 UK Census', 
                value = 'tab-2b',
                className = 'graph-tab',                
                children = [
                    dcc.Graph(
                        className = 'graph',
                        figure = census_graph
                    ),
                ]    
            ),
            dcc.Tab(
                label = '3: Size-scaled Map of Death Locations', 
                value = 'tab-3',
                className = 'graph-tab',                
                children = [
                    dcc.Graph(
                        className = 'graph',
                        figure = death_locs_graph
                    ),
                ]    
            ),
        ]),
        html.Div(id = 'tabs-content')
    ]),
)

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-2a':
        return dcc.Graph(
            className = 'graph',
            figure = naples_graph
        ),
    elif tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-2b':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 4')
        ])

extra_info_dict = {
    'origin': [
        'Data were created and compiled by Robin Wilson in January 2011.',
        html.Br(),
        'For more of Dr. Wilson\'s work, see www.rtwilson.com/academic.  Contact: robin@rtwilson.com',
    ],
    'author': 'This visualization was created by Kiko Whiteley, a student at the University of Hawaii at Manoa studying Math and Computer Science.',
    'tools': 'This visualization primarily uses Dash, a python library that uses Plotly for underlying graphics.',
    'none': ''
}

@app.callback(
   Output('extra-info-text', 'children'),
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