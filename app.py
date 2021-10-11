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
from dash_table.Format import Format, Group
import dash_bootstrap_components as dbc
from plotly.express import data
import dash_daq as daq
from dash.dependencies import Input, Output, State

from dash_bootstrap_templates import load_figure_template

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

theme = dict(dark = True)

app.layout = dbc.Container(fluid = True, children = [
    dbc.Container(fluid = True, children = [
        dbc.Row([
            dbc.Col(
                html.Section([
                    html.H1(
                        '1854 Cholera Outbreak Visualization',
                        id = 'main-title',
                    ),
                    html.H4(
                        'ICS 484 - Project 1 - Kiko Whiteley, Fall 2021',
                        style = {'padding-top': '0px'}
                    ),
                ]),
                width = 6
            ),
            dbc.Col(
                html.Section([
                    html.H5(html.I(
                        'Visualizing reported symptoms (attacks) of Cholera and related deaths along with population features in London and Naples for 42 days, beginning on August 19, 1854.'),
                        style = {'padding-top': '8px'}
                    ),
                    dbc.Row([
                        dbc.Col([
                            html.H4('Extra Info - Select'),
                            html.Div([
                                dcc.Dropdown(
                                    id = 'extra-info-dropdown',
                                    options = [
                                        {'label': 'Data\'s Origin', 'value': 'origin'},
                                        {'label': 'Tools & Libraries Used', 'value': 'tools'},
                                        {'label': 'Author', 'value': 'author'},
                                        {'label': 'None', 'value': 'none'},
                                    ],
                                ),
                            ])], width = 3),
                        dbc.Col(html.H5(id = 'extra-info-text'), width = 9),
                    ]),
                ])
            )
        ])
    ]),
    dbc.Container(fluid = True, children = [
        dcc.Tabs(
        id = 'tabs',
        colors = {
            'primary': 'black',
            'background': '#272727',
            'border': 'whitesmoke'
        },
        parent_className = 'custom-tabs',
        className = 'custom-tabs-container',
        children = [
            dcc.Tab(
                label = 'London: Daily & Cumulative Incidents',
                value = 'tab-1',
                className = 'graph-tab',
            ),
            dcc.Tab(
                label = 'Naples: Deaths vs. Gender & Age',
                value = 'tab-2a',
                className = 'graph-tab',
            ),
            dcc.Tab(
                label = 'UK: Gender & Age Breakdown', 
                value = 'tab-2b',
                className = 'graph-tab',
            ),
            dcc.Tab(
                label = 'London: Death & Pump Locations', 
                value = 'tab-3',
                className = 'graph-tab',
            ),
        ]),
        html.Div(id = 'tabs-content')    
    ]),
])

# Load tsv file
london_df = pd.read_csv('data/choleraDeaths.tsv', sep='\t')

# Rename columns; modify original
london_df.rename(
    columns = {'Attack': 'Attacks', 'Death': 'Deaths'},
    inplace = True
)

daily_total = london_df['Attacks'] + london_df['Deaths']
london_df.insert(3, 'Total', daily_total)

# Create new columns with running totals of attacks and deaths
# Referenced https://www.geeksforgeeks.org/cumulative-sum-of-a-column-in-pandas-python/
attacks_cumul = london_df['Attacks'].cumsum()
deaths_cumul = london_df['Deaths'].cumsum()

# Insert cumulative columns into a new dataframe
london_lineg_df = london_df.copy()
# Delete dates; use integers 0 to 41 instead to represent
# days since August 19, 1854
london_lineg_df.drop(columns=['Date'], axis=0, inplace=True)
london_lineg_df.drop(columns=['Total'], axis=0, inplace=True)
# Rename for legend
london_lineg_df.rename(
    columns = {'Attacks': 'Daily Attacks', 'Deaths': 'Daily Deaths'},
    inplace = True
)
london_lineg_df.insert(1, 'Cumulative Attacks', attacks_cumul)
london_lineg_df.insert(3, 'Cumulative Deaths', deaths_cumul)

table_style_cond = [{
    'if': {'row_index': 'odd'},
    'backgroundColor': '#363636'
}]
table_style_cell = {
    'backgroundColor': '#222222',
    'fontFamily': 'Avenir',
    'color': 'whitesmoke',
    'padding': '4px 10px 4px 10px',
    'width': '80px',
}
table_style_header = {
    'backgroundColor': 'black',
    'fontWeight': 'bold',
    'padding': '4px 10px 4px 10px',
    'text-align': 'center'
}

full_height = 850

london_table = dt.DataTable(
    data = london_df.to_dict('records'),
    columns = [{'name': i, 'id': i} for i in london_df.columns],
    style_data_conditional = table_style_cond,
    style_cell = table_style_cell,
    style_header = table_style_header,
    fixed_rows = {'headers': True},
    # For some reason, max height is 500px with fixed headers
    style_table = dict(
        height = full_height,
        fontSize = 22
    ),
)

london_lineg_fig = px.line(
    london_lineg_df,
    # leave out x variable since it is (0,1,...n) by default
    y = london_lineg_df.columns,
    # Customize colors
    # Referenced https://community.plotly.com/t/plotly-express-line-chart-color/27333/4
    template = 'plotly_dark',
    color_discrete_map = {
        'Daily Attacks':        'yellowgreen',
        'Cumulative Attacks':   'yellowgreen',
        'Daily Deaths':         'red',
        'Cumulative Deaths':    'darkred',
    },
)

graph_font = dict(
    family = 'Avenir',
    size = 24,
)

london_lineg_fig.update_layout(
    plot_bgcolor = '#181818',
    title = 'Attacks & Deaths in London vs. Time',
    title_x = 0.5,
    xaxis_title = 'Days Elapsed Since August 19, 1854',
    yaxis_title = 'Number of People',
    legend_title = '',
    height = 850,
    font = graph_font,
    hoverlabel_font_size = 24,
)

london_lineg_fig.update_traces(
    line = dict(width = 5)
)

# Make cumulative lines dotted
# Referenced https://stackoverflow.com/questions/67064045/plotly-highlight-line-with-dotted-dash-and-marker-with-fig-update-traces?rq=1
london_lineg_fig.update_traces(
    patch = {
        'line': {'dash': 'dot'},
    },
    selector = {
        'legendgroup': 'Cumulative Attacks',
    },
)
london_lineg_fig.update_traces(
    patch = {
        'line': {'dash': 'dot'},
    },
    selector = {
        'legendgroup': 'Cumulative Deaths',
    },
)

london_lineg = dcc.Graph(
    figure = london_lineg_fig,
    className = 'graph'
)

tab_1 = dbc.Row([
    dbc.Col(london_table, width = 3),
    dbc.Col(london_lineg, width = 9),
]),


naples_df = pd.read_csv(
    'data/naplesCholeraAgeSexData.tsv',
    sep='\t',
    skiprows = 6
)

naples_df.rename(
    columns = {'age': 'Age', 'male': 'Male', 'female': 'Female'},
    inplace = True
)

naples_table = dt.DataTable(
    data = naples_df.to_dict('records'),
    columns = [{'name': i, 'id': i} for i in naples_df.columns],
    style_data_conditional = table_style_cond,
    style_cell = table_style_cell,
    style_header = table_style_header,
    style_table = dict(fontSize = 20),
)

age_groups = naples_df['Age']

naples_fig = go.Figure(data=[
    go.Bar(name='Male', x=age_groups, y=naples_df['Male']),
    go.Bar(name='Female', x=age_groups, y=naples_df['Female']),
])

naples_fig.update_layout(
    template = 'plotly_dark',
    barmode='group',
    title='Deaths in Naples vs. Age Group & Gender',
    title_x = 0.5,
    xaxis_title = 'Age Group (Years)',
    yaxis_title = 'Deaths Per 10,000 People',
    height = 850,
    font = graph_font,
    hoverlabel_font_size = 24,
)

naples_graph = dcc.Graph(
    figure = naples_fig,
    className = 'graph'
)

# Arbitrary choice: mean age of 80+ is 85.5 (81-90 approximation)
age_means = [0.5, 3.5, 8, 13, 18, 30.5, 50.5, 70.5, 85.5]

naples_df['Mean Age'] = age_means


naples_lineg_fig = px.line(
    naples_df,
    x = 'Mean Age',
    y = naples_df.columns[1:3],
    template = 'plotly_dark',
)

naples_lineg_fig.update_layout(
    # plot_bgcolor = '#181818',
    title = 'Deaths in Naples vs. Age Group & Gender',
    title_x = 0.5,
    title_y = 0.97,
    yaxis_title = 'Deaths Per 10,000 People',
    xaxis_title = 'Mean Age (Years)',
    legend_title = 'Gender',
    height = full_height,
    font = graph_font,
    hoverlabel_font_size = 24,
)

naples_lineg = dcc.Graph(
    figure = naples_lineg_fig,
    className = 'graph',
)

tab_2a = dbc.Row([
    dbc.Col(naples_table, width = 2),
    dbc.Col(naples_graph, width = 5),
    dbc.Col(naples_lineg, width = 5),
])

census_df = pd.read_csv('data/UKcensus1851.csv', skiprows = 3)

census_df.rename(
    columns = {'age': 'Age', 'male': 'Male', 'female': 'Female'},
    inplace = True
)

# Append entries for 'Total' row
total_row = [
    'Total',
    census_df['Male'].sum(),
    census_df['Female'].sum(),
]

census_table_df = census_df.copy()
census_table_df.loc[-1] = total_row

census_table = dt.DataTable(
    data = census_table_df.to_dict('records'),
    columns = [
        dict(name = 'Age', id = 'Age'),
        dict(name = 'Male', id = 'Male', type = 'numeric', format = Format().group(True)),
        dict(name = 'Female', id = 'Female', type = 'numeric', format = Format().group(True)),        
    ],
    style_table = dict(
        width = 460,
        fontSize = 18,
    ),
    style_data_conditional = table_style_cond,
    style_cell = table_style_cell,
    style_header = table_style_header,
)

gender_fig = px.pie(
    values = [census_df['Male'].iloc[-1], census_df['Female'].iloc[-1]],
    names =  ['Male', 'Female'],
    title = 'Proportion of Population by Gender',
    template = 'plotly_dark',
    width = 442,
)

gender_fig.update_layout(
    title_x = 0.5,
    font = dict(
        family = 'Avenir',
        size = 18
    ),
    hoverlabel_font_size = 24
)

gender_pie = dcc.Graph(
    figure = gender_fig,
    className = 'graph',
)

# Make side-by-side pie charts for age groups grouped by gender
# Referenced https://plotly.com/python/pie-charts/
census_fig = make_subplots(
    rows = 1,
    cols = 2,
    specs=[[{'type':'domain'}, {'type':'domain'}]],
    # subplot_titles = ('Male', 'Female'),
)
census_fig.add_trace(
    go.Pie(
        title = 'Male',
        title_font_size = 36,
        labels = census_df['Age'],
        values = census_df['Male'],
        marker = dict(colors = px.colors.sequential.Viridis),
        legendgrouptitle = dict(text = 'Age')
        # color_discrete_sequence = px.colors.sequential.GnBu
    ), 1, 1
)
census_fig.add_trace(
    go.Pie(
        title = 'Female',
        title_font_size = 36,
        labels = census_df['Age'],
        values = census_df['Female'],
    ), 1, 2
)
census_fig.update_traces(
    hole = .5,
    hoverinfo = "label+percent+name"
)

census_fig.update_layout(
    template = 'plotly_dark',
    font_family = 'Avenir',
    font_size = 24,
    title_text = "Age Groups by Gender",
    title_x = 0.5,
    title_font_size = 40,
    width = 1450,
    height = 547,
    hoverlabel_font_size = 24,   
)

census_graph = dcc.Graph(
    figure = census_fig,
    className = 'graph'
)

img_box = dict(
    paddingBottom = '8px',
)

tree_map_ma = html.Div([
    html.Img(
        src = app.get_asset_url('tree_map_ma.png'),
        className = 'image',
    )],
    style = img_box
)
tree_map_fe = html.Div([
    html.Img(
        src = app.get_asset_url('tree_map_fe.png'),
        className = 'image',
    )],
    style = img_box
)

tab_2b = dbc.Container(fluid = True, children = [
    dbc.Row([
        dbc.Col([
            dbc.Row(census_table),
            dbc.Row(gender_pie, style = dict(paddingTop = 10)),
        ], width = 3),
        dbc.Col([
            dbc.Row(
                census_graph,
                style = dict(paddingBottom = 16)),
            dbc.Row([
                dbc.Col([
                    html.H2('Male'),
                    dbc.Row(tree_map_ma)
                ],
                align = 'center',
                width = 6),
                dbc.Col([
                    html.H2('Female'),
                    dbc.Row(tree_map_fe)
                ], width = 6),
            ])
        ], width = 9)
    ])
])

pump_locs_df = pd.read_csv(
    'data/choleraPumpLocations.csv',
    names = ['Lon', 'Lat'])
pump_lons = pump_locs_df.iloc[:,0]
pump_lats = pump_locs_df.iloc[:,1]


death_locs_df = pd.read_csv(
    'data/choleraDeathLocations.csv',
    names = ['Deaths', 'Lon', 'Lat'],
    error_bad_lines = False)

death_locs_fig = px.scatter_mapbox(
    death_locs_df,
    lon = death_locs_df['Lon'],
    lat = death_locs_df['Lat'],
    size = death_locs_df['Deaths'],
    color_discrete_sequence = ['indianred'],
    center = dict(
        lon = death_locs_df['Lon'].mean(),
        lat = death_locs_df['Lat'].mean(),
    ),
    zoom = 16,
    height = 800,
    template = 'plotly_dark',
)

death_locs_fig.add_traces(go.Scattermapbox(
    name = 'Deaths',
    lon = pump_lons,
    lat = pump_lats,
))

death_locs_fig.add_traces(go.Scattermapbox(
    name = 'Pumps',
    lon = pump_lons,
    lat = pump_lats,
    marker = go.scattermapbox.Marker(
        size = 20,
        color = 'yellowgreen',
    )
))

death_locs_fig.update_layout(
    legend = dict(
        font = dict(
            family = 'Avenir',
            size = 36
        )
    ),
    mapbox = dict(style = 'carto-darkmatter'),
    font = graph_font,
    margin = dict(l=4, r=4, b=4, t=4),
    hoverlabel_font_size = 24,
)

deaths_graph = dcc.Graph(figure = death_locs_fig)

tab_3 = dbc.Col([
    html.H1('(Amount Proportional to Dot Size)'),
    deaths_graph
], className = 'graph')

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return tab_1
    elif tab == 'tab-2a':
        return tab_2a
    elif tab == 'tab-2b':
        return tab_2b
    elif tab == 'tab-3':
        return tab_3

extra_info_dict = dict(
    origin = [
        'The dataset was created and compiled by Robin Wilson in January 2011.',
        html.Br(),
        'For more of Dr. Wilson\'s work, see www.rtwilson.com/academic.',
        html.Br(),
        'Contact: robin@rtwilson.com'
    ],
    author = 'This visualization was created by Kiko Whiteley, a student at the University of Hawaii at Manoa studying Math and Computer Science.',
    tools = 'This visualization uses Dash, a python library that uses Plotly for underlying graphics.  Graphs were made with Plotly Express and Dash Bootstrap components.',
    none = ''
)

@app.callback(
   Output('extra-info-text', 'children'),
   Input('extra-info-dropdown', 'value'))
def choose_extra_info(choice):
    if choice and extra_info_dict[choice]:
        return extra_info_dict[choice]
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
