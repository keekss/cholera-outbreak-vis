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