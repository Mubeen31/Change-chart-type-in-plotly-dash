import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd


income = pd.read_csv('data.csv', encoding='Latin1')
income['InvoiceDate'] = pd.to_datetime(income['InvoiceDate'])
income['Date'] = income['InvoiceDate'].dt.date
income['Sales'] = income['Quantity'] * income['UnitPrice']


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H3('Sales Data Analysis', style = {'margin-bottom': '0px', 'color': 'black'}),
            ])
        ], className = "create_container1 four columns", id = "title"),

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "25px"}),


    html.Div([
        html.Div([


            html.P('Select Country', className = 'fix_label', style = {'color': 'black', 'margin-top': '2px'}),
            dcc.Dropdown(id = 'select_countries',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Switzerland',
                         placeholder = 'Select Countries',
                         options = [{'label': c, 'value': c}
                                    for c in (income['Country'].unique())], className = 'dcc_compon'),




        ], className = "create_container2 four columns", style = {'margin-bottom': '20px'}),
    ], className = "row flex-display"),



    html.Div([
        html.Div([
            html.P('Select Chart Type', className = 'fix_label', style = {'color': 'black'}),
            dcc.RadioItems(id = 'radio_items',
                           labelStyle = {"display": "inline-block"},
                           options = [
                                      {'label': 'Line chart', 'value': 'line'},
                                      {'label': 'Donut chart', 'value': 'donut'},
                                      {'label': 'Horizontal bar chart', 'value': 'horizontal'}],
                           value = 'line',
                           style = {'text-align': 'center', 'color': 'black'}, className = 'dcc_compon'),

            dcc.Graph(id = 'multi_chart',
                      config = {'displayModeBar': 'hover'}),

        ], className = "create_container2 six columns"),

    ], className = "row flex-display"),

], id= "mainContainer", style={"display": "flex", "flex-direction": "column"})



@app.callback(Output('multi_chart', 'figure'),
              [Input('select_countries', 'value')],
              [Input('radio_items', 'value')])
def update_graph(select_countries, radio_items):

    # Data for line chart
    income1 = income.groupby(['Country', 'Date', 'Description'])[['Sales', 'Quantity']].sum().reset_index()
    income2 = income1[income1['Country'] == select_countries]

    # Data for donut chart
    Total_sales = income1[income1['Country'] == select_countries]['Sales'].sum()
    Total_quantity = income1[income1['Country'] == select_countries]['Quantity'].sum()
    colors = ['orange', 'green']

    top_country = income1[income1['Country'] == select_countries].sort_values(by = 'Sales', ascending = False).nlargest(10, columns=['Sales'])



    if radio_items == 'line':



     return {
        'data':[go.Scatter(
                    x=income2['Date'],
                    y=income2['Quantity'],
                    mode = 'markers+lines',
                    line = dict(width = 3, color = 'green'),
                    marker = dict(size = 5, symbol = 'circle', color = 'white',
                                  line = dict(color = 'orange', width = 2)
                                  ),
                    hoverinfo='text',
                    hovertext=
                    '<b>Country</b>: ' + income2['Country'].astype(str) + '<br>' +
                    '<b>Date</b>: ' + income2['Date'].astype(str) + '<br>' +
                    '<b>Quantity</b>: ' + [f'{x:,.0f}' for x in income2['Quantity']] + '<br>'


              )],


        'layout': go.Layout(
             plot_bgcolor='#F2F2F2',
             paper_bgcolor='#F2F2F2',
             title={
                'text': 'Total Quantities: ' + ' ' + (select_countries),

                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'black',
                        'size': 15},

             hovermode='x',
             # margin = dict(b = 160),
             xaxis=dict(title='<b>Date</b>',
                        color='black',
                        showline=True,
                        showgrid=True,
                        linecolor='black',
                        linewidth=1,


                ),

             yaxis=dict(title='<b>Quantity</b>',
                        color='black',
                        showline=False,
                        showgrid=True,
                        linecolor='black',

                ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'black',


                 )
        )

    }

    elif radio_items == 'donut':

     return {
        'data': [go.Pie(labels = ['Total Sales', 'Total Quantity'],
                        values = [Total_sales, Total_quantity],
                        marker = dict(colors = colors),
                        hoverinfo = 'label+value+percent',
                        textinfo = 'label+value',
                        textfont = dict(size = 13),
                        texttemplate = '%{label}: %{value:,f} <br>(%{percent})',
                        textposition = 'auto',
                        hole = .7,
                        # rotation = 220
                        # insidetextorientation='radial',

                        )],
        'layout': go.Layout(
            # width=800,
            # height=520,
            plot_bgcolor = '#F2F2F2',
            paper_bgcolor = '#F2F2F2',
            hovermode = 'x',
            title = {
                'text': 'Total quantities and sales : ' + ' ' + (select_countries),

                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont = {
                'color': 'black',
                'size': 15},
            legend = {
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'black')
        ),

    }

    elif radio_items == 'horizontal':

     return {
        'data': [go.Bar(x = top_country['Sales'],
                        y = top_country['Description'],
                        text = top_country['Sales'],
                        texttemplate = '%{text:,.0s}',
                        textposition = 'auto',
                        marker = dict(
                            color = top_country['Sales'],
                            colorscale = 'portland',
                            showscale = False
                        ),
                        orientation = 'h',
                        hoverinfo = 'text',
                        hovertext =
                        '<b>Country</b>: ' + top_country['Country'].astype(str) + '<br>' +
                        '<b>Descripton</b>: ' + top_country['Description'].astype(str) + '<br>' +
                        '<b>Sales</b>: $' + [f'{x:,.0f}' for x in top_country['Sales']] + '<br>'

                        )],

        'layout': go.Layout(
            plot_bgcolor = '#F2F2F2',
            paper_bgcolor = '#F2F2F2',
            title = {
                'text': 'Top Description Sales :' + ' ' + (select_countries),
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont = {
                         'color': 'black',
                         'size': 15},

            hovermode = 'closest',
            margin = dict(l = 300),

            xaxis = dict(title = '<b>Sales</b>',

                         color = 'black',
                         showline = True,
                         showgrid = True,
                         showticklabels = True,
                         linecolor = 'black',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black'
                         )

                         ),
            yaxis = dict(title = '<b></b>',
                         autorange = 'reversed',
                         color = 'black',
                         showline = False,
                         showgrid = False,
                         showticklabels = True,
                         linecolor = 'black',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black'
                         )

                         )

        )
    }




if __name__ == '__main__':
    app.run_server(debug=True)