    #     figure = {
    #         'data': [
    #             # Attempt to iterate automatically
    #             # [{'y': i for i in deaths_graph_df[col]} for col in deaths_graph_df.columns],
                
    #             # Manually get series
    #             {'y': [i for i in deaths_graph_df['Attack']]},
    #             {'y': [i for i in deaths_graph_df['Cumulative Attacks']]},
    #             {'y': [i for i in deaths_graph_df['Death']]},
    #             {'y': [i for i in deaths_graph_df['Cumulative Deaths']]},
    #         ]
    #     }



    # collapse = html.Div(
#     [
#         dbc.Button(
#             "Open collapse",
#             id="collapse-button",
#             className="mb-3",
#             color="primary",
#             n_clicks=0,
#         ),
#         dbc.Collapse(
#             dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
#             id="collapse",
#             is_open=False,
#         ),
#     ]
# )

# @app.callback(
#     Output("collapse", "is_open"),
#     [Input("collapse-button", "n_clicks")],
#     [State("collapse", "is_open")],
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open



        #     # Referenced https://stackoverflow.com/questions/50213761/changing-visibility-of-a-dash-component-by-updating-other-component
        #     html.Section(
        #         id = 'extra-info',
        #         children = [
        #             html.H2('Extra Info - Select'),
        #             dcc.Dropdown(
        #                 id = 'extra-info-dropdown',
        #                 options = [
        #                     {'label': 'Data\'s Origin', 'value': 'origin'},
        #                     {'label': 'Visualization Tools & Libraries', 'value': 'tools'},
        #                     {'label': 'Author', 'value': 'author'},
        #                     {'label': 'None', 'value': 'none'},

        #                 ]),
        #             html.H3(id = 'extra-info-box'),
        #         ]
        #     ),

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