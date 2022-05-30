import pathlib
import dash
from dash import dcc
from dash import html
from components import *
import os
import pandas as pd
import numpy as np
import logging
from dash.dependencies import Input, Output
from optimizer import optimize_price
from optimizer import optimize_quantity
import dash_daq as daq

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
# app._favicon = os.path.join(APP_PATH, os.path.join("assets", "favicon.ico"))
app.title = "Price Optimization Application"
server = app.server
app.config["suppress_callback_exceptions"] = True

# Load the data
df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "price.csv")))

side_panel_layout = html.Div(
    id="panel-side",
    children=[
        # html.H1(id="title", children=["Price & Quantity Optimization"]),
        html.H1(id="title", children=["Price Optimization"]),
        html.Div(id="dropdown", children=dropdown),
        html.Br(),
        html.H3("Optimization Range"),
        # html.Div(id='output-container-range-slider'),
        range_slider,
        html.Br(),
        html.H3("Fixed Cost"),
        html.Div(
            [numeric_input],
            style={"display": "flex", "justify-content": "center"},
        ),
        html.Br(),
        html.H3("Recommendation"),
        html.P(id="id-insights", className="description"),
    ],
)


# Main Panel
main_panel_layout = html.Div(
    id="panel-upper-lower",
    children=[
        dcc.Interval(id="interval", interval=1 * 2000, n_intervals=0),
        html.Div(
            id="panel",
            children=[
                histogram_price_quantity,
                html.Br(),
                histogram_max_revenue,
                html.Br(),
                data_table_result,
            ],
        ),
    ],
)

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

# Root
root_layout = html.Div(
    id="root",
    children=[
        side_panel_layout,
        main_panel_layout,
    ],
)

app.layout = root_layout


# @app.callback(
#     dash.dependencies.Output('output-container-range-slider', 'children'),
#     [dash.dependencies.Input('my-range-slider', 'value')],
# )
# def update_output(value):
#     return "{}".format(value)


@app.callback(
    [
        Output("heatmap", 'data'),
        Output("lineChart1", 'figure'),
        Output("lineChart2", 'figure'),
        Output("id-insights", 'children'),
    ],
    [
        Input("selected-var-opt", "value"),
        Input("my-range-slider", "value"),
        Input("selected-cost-opt", "value"),
    ],
)
def update_output_all(var_opt, var_range, var_cost):

    try:
        if var_opt == 'price':
            (
                res,
                fig_PriceVsRevenue,
                fig_PriceVsQuantity,
                opt_Price,
                opt_Revenue,
            ) = optimize_price.fun_optimize(var_opt, var_range, var_cost, df)
            res = np.round(res.sort_values('Revenue', ascending=False), decimals=2)

            if opt_Revenue > 0:
                return [
                    res.to_dict('records'),
                    fig_PriceVsRevenue,
                    fig_PriceVsQuantity,
                    f'The maximum revenue of {opt_Revenue} is achieved by optimizing {var_opt} of {opt_Price}, fixed cost of {var_cost} and optimization was carried for {var_opt} range between {var_range}',
                ]
            else:
                return [
                    res.to_dict('records'),
                    fig_PriceVsRevenue,
                    fig_PriceVsQuantity,
                    f'For the fixed cost of {var_cost} and {var_opt} range between {var_range}, you will incur loss in revenue',
                ]

        else:
            (
                res,
                fig_QuantityVsRevenue,
                fig_PriceVsQuantity,
                opt_Quantity,
                opt_Revenue,
            ) = optimize_quantity.fun_optimize(var_opt, var_range, var_cost, df)
            res = np.round(res.sort_values('Revenue', ascending=False), decimals=2)

            if opt_Revenue > 0:
                return [
                    res.to_dict('records'),
                    fig_QuantityVsRevenue,
                    fig_PriceVsQuantity,
                    f'The maximum revenue of {opt_Revenue} is achieved by optimizing {var_opt} of {opt_Quantity}, fixed cost of {var_cost} and optimization was carried for {var_opt} range between {var_range}',
                ]
            else:
                return [
                    res.to_dict('records'),
                    fig_QuantityVsRevenue,
                    fig_PriceVsQuantity,
                    f'For the fixed cost of {var_cost} and {var_opt} range between {var_range}, you will incur loss in revenue',
                ]

    except Exception as e:
        logging.exception('Something went wrong with interaction logic:', e)


if __name__ == "__main__":
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=8002,
        dev_tools_hot_reload=True,
        dev_tools_ui=False,
    )
