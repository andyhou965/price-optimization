from turtle import st
from dash import dcc
from dash import html
from dash import dash_table


import dash_daq as daq

# Side panel
dropdown = dcc.Dropdown(
    id="selected-var-opt",
    className="dropdown-component",
    options=[
        {"label": "Price", "value": "price"},
        {"label": "Quantity", "value": "quantity"},
    ],
    clearable=False,
    value="price",
)

range_slider = dcc.RangeSlider(
    id='my-range-slider',
    min=100,
    max=500,
    step=50,
    # marks={0: '0', 500: '500'},
    value=[200, 400],
)

numeric_input = daq.NumericInput(
    id='selected-cost-opt', size=200, min=0, max=10000, value=80
)

# Histogram
histogram_price_quantity = html.Div(
    className="panel-container",
    children=[
        html.Div(
            className="panel-header",
            children=[
                html.H1(className="panel-title", children=["PRICE VS QUANTITY"]),
                # minute_toggle,
            ],
        ),
        dcc.Graph(
            id="lineChart2",
            className="histogram-graph",
            config={"displayModeBar": False, 'displaylogo': False},
        ),
    ],
)

histogram_max_revenue = html.Div(
    className="panel-container",
    children=[
        html.Div(
            className="panel-header",
            children=[
                html.H1(className="panel-title", children=["MAXIMIZING REVENUE"]),
                # minute_toggle,
            ],
        ),
        dcc.Graph(
            id="lineChart1",
            className="histogram-graph",
            config={"displayModeBar": False, 'displaylogo': False},
        ),
    ],
)

# Data Table
data_table_result = html.Div(
    className="panel-container",
    children=[
        html.Div(
            className="panel-header",
            children=[
                html.H1(className="panel-title", children=["SIMULATED RESULT"]),
            ],
        ),
        dash_table.DataTable(
            id='heatmap',
            columns=[
                {
                    'name': 'Price',
                    'id': 'Price',
                    'type': 'numeric',
                },
                {
                    'name': 'Revenue',
                    'id': 'Revenue',
                    'type': 'numeric',
                },
                {
                    'name': 'Quantity',
                    'id': 'Quantity',
                    'type': 'numeric',
                },
            ],
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(60, 60, 60)',
                },
                {
                    'if': {
                        'row_index': 0,  # number | 'odd' | 'even'
                        'column_id': 'Revenue',
                    },
                    'backgroundColor': '#fec036',
                    'color': 'white',
                },
                {
                    'if': {
                        'row_index': 0,  # number | 'odd' | 'even'
                        'column_id': 'Price',
                    },
                    'backgroundColor': '#fec036',
                    'color': 'white',
                },
                {
                    'if': {
                        'row_index': 0,  # number | 'odd' | 'even'
                        'column_id': 'Quantity',
                    },
                    'backgroundColor': '#fec036',
                    'color': 'white',
                },
            ],
            style_header={
                'backgroundColor': 'rgb(0, 0, 0)',
                'fontWeight': 'bold',
                'color': 'white',
                'fontSize': "1rem",
                'textAlign': 'center',
                # 'border': '1px solid black'
            },
            style_data={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white',
                'fontSize': "0.9rem",
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left',
            },
            # editable=True,
            filter_action="native",
            sort_action="native",
            page_size=10,
        ),
    ],
)
