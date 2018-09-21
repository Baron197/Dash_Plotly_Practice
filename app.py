import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from categoryplot import dfTips, getPlot

app = dash.Dash() # make python obj with Dash() method

color_set = {
    'sex': ['#ff3fd8','#4290ff'],
    'smoker': ['#32fc7c','#ed2828'],
    'time': ['#0059a3','#f2e200'],
    'day': ['#ff8800','#ddff00','#3de800','#00c9ed']
}

app.title = 'Purwadhika Dash Plotly'; # set web title

# function to generate HTML Table
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col,className='table_dataset') for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col],className='table_dataset') for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
        ,className='table_dataset'
    )

#the layout/content
app.layout = html.Div(children=[
    dcc.Tabs(id="tabs", value='tab-1', 
        style={
            'fontFamily': 'system-ui'
        },
        content_style={
            'fontFamily': 'Arial',
            'borderLeft': '1px solid #d6d6d6',
            'borderRight': '1px solid #d6d6d6',
            'borderBottom': '1px solid #d6d6d6',
            'padding': '44px'
        }, 
        children=[
            dcc.Tab(label='Tips Data Set', value='tab-1', children=[
                html.Div([
                    html.H1('Tips Data Set'),
                    generate_table(dfTips)
                ])
            ]),
            dcc.Tab(label='Scatter Plot', value='tab-2', children=[
                html.Div([
                    html.H1('Scatter Plot Tips Data Set'),
                    html.Table([
                        html.Tr([
                            html.Td(html.P('Hue : ')),
                            html.Td([
                                dcc.Dropdown(
                                    id='ddl-hue-scatter-plot',
                                    options=[{'label': 'Sex', 'value': 'sex'},
                                            {'label': 'Smoker', 'value': 'smoker'},
                                            {'label': 'Day', 'value': 'day'},
                                            {'label': 'Time', 'value': 'time'}],
                                    value='sex'
                                )]
                            )
                        ])
                    ],style={ 'width': '300px', 'paddingBottom': '30px' }),
                    dcc.Graph(
                        id='scatterPlot',
                        figure={
                            'data': []
                        }
                    )
                ])
            ]),
            dcc.Tab(label='Categorical Plot', value='tab-3', children=[
                html.Div([
                    html.H1('Categorical Plot Tips Data Set'),
                    html.Table([
                        html.Tr([
                            html.Td([
                                html.P('Jenis : '),
                                dcc.Dropdown(
                                    id='ddl-jenis-plot-category',
                                    options=[{'label': 'Bar', 'value': 'bar'},
                                            {'label': 'Violin', 'value': 'violin'},
                                            {'label': 'Box', 'value': 'box'}],
                                    value='bar'
                                )
                            ]),
                            html.Td([
                                html.P('X Axis : '),
                                dcc.Dropdown(
                                    id='ddl-x-plot-category',
                                    options=[{'label': 'Smoker', 'value': 'smoker'},
                                            {'label': 'Sex', 'value': 'sex'},
                                            {'label': 'Day', 'value': 'day'},
                                            {'label': 'Time', 'value': 'time'}],
                                    value='sex'
                                )
                            ])
                        ])
                    ], style={ 'width' : '700px', 'margin': '0 auto'}),
                    dcc.Graph(
                        id='categoricalPlot',
                        figure={
                            'data': []
                        }
                    )
                ])
            ])
    ])
], 
style={
    'maxWidth': '1000px',
    'margin': '0 auto'
})

@app.callback(
    dash.dependencies.Output('scatterPlot', 'figure'),
    [dash.dependencies.Input('ddl-hue-scatter-plot', 'value')])
def update_scatter_graph(ddlHueScatterPlot):
    return {
            'data': [
                go.Scatter(
                    x=dfTips[dfTips[ddlHueScatterPlot] == col]['total_bill'], 
                    y=dfTips[dfTips[ddlHueScatterPlot] == col]['tip'], 
                    mode='markers', 
                    # line=dict(color=color_set[i], width=1, dash='dash'), 
                    marker=dict(color=color_set[ddlHueScatterPlot][i], size=10, line={'width': 0.5, 'color': 'white'}), name=col)
                for col,i in zip(dfTips[ddlHueScatterPlot].unique(),range(len(color_set[ddlHueScatterPlot])))
            ],
            'layout': go.Layout(
                xaxis={'title': 'Total Bill'},
                yaxis={'title': 'Tip'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                hovermode='closest'
            )
    };

@app.callback(
    Output('categoricalPlot', 'figure'),
    [Input('ddl-jenis-plot-category', 'value'),
    Input('ddl-x-plot-category', 'value')])
def update_category_graph(ddljeniscategory, ddlxcategory):
    return {
            'data': getPlot(ddljeniscategory,ddlxcategory),
            'layout': go.Layout(
                xaxis={'title': ddlxcategory.capitalize()}, yaxis={'title': 'US$'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1.2}, hovermode='closest',
                boxmode='group',violinmode='group'
                # plot_bgcolor= 'black', paper_bgcolor= 'black',
            )
    };

if __name__ == '__main__':
    # run server on port 1997
    # debug=True for auto restart if code edited
    app.run_server(debug=True, port=1997) 

