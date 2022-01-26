#Import libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
pie_fig = go.Figure()
scatter_fig = go.Figure()
payload_range = []

#Import data
data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv") 
spacex_df = pd.DataFrame(data)

#Create dash app
app = dash.Dash(__name__)

#Create app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard', 
        style={'textAlign': 'center', 'color': '#503D36','font-size': 40}
    ),
    
    html.Div(
        ["Launch Site: "], style={'font-size': 40}
    ),
    
    #TASK 1
    #Add Launch Site drop-down Input component
    html.Div(
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
            ],
            value='ALL',
            placeholder="Select a Launch Site",
            searchable=True
        )
    ),
    
    #TASK 2
    #Add pie chart based on selected site dropdown
    html.Div([
        dcc.Graph(id='success-pie-chart', figure=pie_fig)
    ]),
    
    #TASK 3
    #Add Range Slider to select payload
    html.Div([
        dcc.RangeSlider(
            id='payload-slider',
            min=0, 
            max=10000, 
            step=1000,
            marks={
                0: '0', 
                2000: '2000',
                4000: '4000',
                6000: '6000',
                8000: '8000',
                10000: '10000'
            },
            value=[
                min(spacex_df['Payload Mass (kg)']), 
                max(spacex_df['Payload Mass (kg)'])
            ]
        )
    ]),

    #TASK 4
    #Add scatter plot based on selected dropdown and selected payload range
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart', figure=scatter_fig)
    ])
])

#TASK 2
#Add a callback function to render pie chart based on selected site dropdown
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)  

#TASK 2
#Render pie chart
def get_pie_chart(entered_site, payload_range):
    if entered_site == 'ALL':
        #Filter data for payload range for ALL sites
        filtered_df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_range[1]) 
        ]
        #Create pie chart 
        pie_fig = px.pie(
            filtered_df, 
            values='class', 
            names='Launch Site', 
            title=
                'Successful Launches By Site for Payload Mass ' + 
                str(payload_range[0]) + 'kg - ' + str(payload_range[1]) + 'kg'
        )
    else:
        #Filter data for payload range for SELECTED site
        filtered_df = spacex_df[
            (spacex_df['Launch Site'] == entered_site) &
            (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_range[1]) 
        ]      
        #Create pie chart 
        pie_fig = px.pie(
            filtered_df,
            names='class', 
            title='Successful Launches for Site ' + entered_site + ' for Payload Mass ' + 
                str(payload_range[0]) + 'kg - ' + str(payload_range[1]) + 'kg'
        ) 
    return pie_fig

#TASK 4
#Add a callback function to render the scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id='payload-slider', component_property='value')]
)

#TASK 4
#Render the scatter plot
def get_scatter_plot(entered_site, payload_range):
    if entered_site == 'ALL':
        #Filter data for payload range
        filtered_df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_range[1]) 
        ]
        #Create scatter plot for ALL sites
        scatter_fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category'
        )
    else:
        #Filter data for SELECTED site and payload range
        filtered_df = spacex_df[
            (spacex_df['Launch Site'] == entered_site) &
            (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_range[1]) 
        ]
        #Create scatter plot for SELECTED site
        scatter_fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category'
        )
    return scatter_fig

# Run app
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050, debug=True)
