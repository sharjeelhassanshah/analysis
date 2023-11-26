import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


airport = pd.read_csv('./airtraffic.csv')
airport.dropna(inplace=True)

airport1 = airport[['state', 'lat', 'long']]

list_locations = airport1.set_index('state')[['lat', 'long']].T.to_dict('dict')


app = dash.Dash(__name__, meta_tags=[
                {"name": "viewport", "content": "width=device-width"}])

server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H2("Airport Traffic Data", style={'text-align': 'center'}),
            html.P('Select State'),
            html.Div([
                dcc.Dropdown(
                    id='select_state',
                    multi=False,
                    clearable=True,
                    disabled=False,
                    style={'display': True},
                    value='FL',
                    placeholder='Select state',
                    options=[{'label': c, 'value': c}
                             for c in (airport['state'].unique())]),

            ], className='fix_dropdown'),

        ], className="three columns left_pane"),

        html.Div([
            dcc.Graph(id='map_chart'),
            dcc.Graph(id='bar_chart'),

        ], className="nine columns fix_charts charts_bg"),

    ], className="row"),

])


@app.callback(Output('map_chart', 'figure'),
              [Input('select_state', 'value')])
def update_graph(select_state):
    airport4 = airport.groupby(['state', 'airport', 'city', 'lat', 'long'])[
        'cnt'].sum().reset_index()
    airport5 = airport4[airport4['state'] == select_state]

    return {
        'data': [go.Scattermapbox(
            lon=airport5['long'],
            lat=airport5['lat'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=12,
                color=airport5['cnt'],
                colorscale='HSV',
                showscale=False,
                sizemode='area'),

            hoverinfo='text',
            hovertext='<b>State</b>: ' + airport5['state'].astype(str) + '<br>' +
            '<b>City</b>: ' + airport5['city'].astype(str) + '<br>' +
            '<b>Airport</b>: ' + airport5['airport'].astype(str) + '<br>' +
            '<b>Lat</b>: ' + [f'{x:.4f}' for x in airport5['lat']] + '<br>' +
            '<b>Long</b>: ' + [f'{x:.4f}' for x in airport5['long']] + '<br>' +

            '<b>Arrivals</b>: ' +
            [f'{x:,.0f}' for x in airport5['cnt']] + '<br>'

        )],

        'layout': go.Layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            hovermode='closest',
            mapbox=dict(
                # Create free account on Mapbox site and paste here access token
                accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
                center=dict(
                    lat=list_locations[select_state]['lat'], lon=list_locations[select_state]['long']),
                style='open-street-map',
                # style='dark',
                zoom=3,
                bearing=0
            ),
            autosize=True,

        )

    }


@app.callback(Output('bar_chart', 'figure'),
              [Input('select_state', 'value')])
def update_graph(select_state):
    airport2 = airport.groupby(['state', 'airport', 'city', 'lat', 'long'])[
        'cnt'].sum().reset_index()
    airport3 = airport2[airport2['state'] == select_state]

    return {
        'data': [go.Bar(
            x=airport3['airport'],
            y=airport3['cnt'],
            text=airport3['cnt'],
            texttemplate='%{text:,.0f}',
            textposition='auto',


            marker=dict(color=airport3['cnt'],
                        colorscale='phase',
                        showscale=False
                        ),

            hoverinfo='text',
            hovertext='<b>State</b>: ' + airport3['state'].astype(str) + '<br>' +
            '<b>City</b>: ' + airport3['city'].astype(str) + '<br>' +
            '<b>Airport</b>: ' + airport3['airport'].astype(str) + '<br>' +
            '<b>Arrivals</b>: ' +
                [f'{x:,.0f}' for x in airport3['cnt']] + '<br>'

        )],

        'layout': go.Layout(
            plot_bgcolor='#343332',
            paper_bgcolor='#343332',
            title={
                'text': 'Total Arrivals in' + ' ' + (select_state) + ' ' + 'State',

                'y': 0.95,
                'x': 0.17,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 15},

            hovermode='x',
            margin=dict(b=140, t=0),



            xaxis=dict(title='<b></b>',
                       color='white',
                       showline=True,
                       showgrid=False,
                       linecolor='white',
                       linewidth=1,
                       showticklabels=True,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white'
                       )

                       ),

            yaxis=dict(title='<b></b>',


                       color='white',
                       showline=False,
                       showgrid=False,
                       showticklabels=False,
                       linecolor='white',

                       ),

            legend={
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font=dict(
                family="sans-serif",
                size=15,
                color='white'),

        )

    }


if __name__ == "__main__":
    app.run_server(debug=True)
