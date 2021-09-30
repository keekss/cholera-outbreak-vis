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
    # className = 'app-layout',
    children = [
    html.Section(
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
                'Visualizing reported symptoms of Cholera (attacks) and related deaths in London and Naples for 42 days, beginning on August 19, 1854.'
            )
        ]
    ),
    # Referenced https://stackoverflow.com/questions/50213761/changing-visibility-of-a-dash-component-by-updating-other-component
    html.Section(
        id = 'extra-info',
        children = [
            html.H2('Extra Info - Select'),
            dcc.Dropdown(
                id = 'extra-info-dropdown',
                options = [
                    {'label': 'Data\'s Origin', 'value': 'origin'},
                    {'label': 'Visualization Tools & Libraries', 'value': 'tools'},
                    {'label': 'Author', 'value': 'author'},
                    {'label': 'None', 'value': 'none'},

                ]),
            html.H3(id = 'extra-info-box'),
        ]
    ),

    ## Extras to add if possible
    # html.H4(
    #     'Include cumulative counts?',
    # ),
    # html.Div(
    #     daq.ToggleSwitch(
    #         id = 'cumul-toggle',
    #         value = False,
    #         color = 'green',
    #     ),
    #     style = {
    #         'width': '200px',
    #         'margin': 'auto',
    #     },
    # ),

    # dcc.Slider(
    #     id = 'days-slider',
    #     min = 1,
    #     max = deaths_df.shape[0],
    #     step = 1,
    # ),

    html.Section(
        html.Div(
            children = [
                html.H1('1A: Table of Daily Incidents in London'),
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
        )
    ),

    html.Section(
        children = [
            html.H1('1B: Graph of Time-Series Incidents'),
            dcc.Graph(
                className = 'graph',
                figure = deaths_graph,
            ),
        ]
    ),

    html.Section(
        children = [
            html.H1('2A: Gender-grouped Chart of Deaths in Naples During the Same Time Period'),
            dcc.Graph(
                className = 'graph',
                figure = naples_graph
            ),
        ]
    ),
    html.Section(
        children = [
            html.H1('2B: Gender-grouped Breakdown of Age Groups from the 1851 UK Census'),
            dcc.Graph(
                className = 'graph',
                figure = census_graph,
            ),
        ]
    ),
    html.Section(
        children = [
            html.H1('3) Size-scaled Map of Death Locations'),
            dcc.Graph(
                className = 'graph',
                figure = death_locs_graph
            ),
        ]

    ),
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