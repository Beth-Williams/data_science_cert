# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                 dcc.Dropdown(id='site-dropdown',
                                 options= [{'label': 'ALL', 'value': 'ALL'},
                                            {'label': 'LC-40', 'value': 'LC-40'},
                                            {'label': 'SLC-40', 'value': 'SLC-40'},
                                            {'label': 'SLC-4E', 'value': 'SLC-4E'},
                                            {'label': 'LC-39A', 'value': 'LC-39A'}],
                                            value='ALL',
                                            placeholder= "Launch Sites",
                                            searchable=True),
                                html.Br(),

                               
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[0, 10000]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                                                ])
                                # Function decorator to specify function input and output
 # TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output                               
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
    )
                                 
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    lc40 = spacex_df[spacex_df["Launch Site"]=="CCAFS LC-40"]
    slc40 = spacex_df[spacex_df["Launch Site"]=="CCAFS SLC-40"]
    slc4E = spacex_df[spacex_df["Launch Site"]=="VAFB SLC-4E"]
    lc39A = spacex_df[spacex_df["Launch Site"]=="KSC LC-39A"]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='All')
        fig.update_layout(transition_duration=500)
        return fig
    elif entered_site =='LC-40':
        fig = px.pie([lc40[lc40["class"]==0].count(), lc40[lc40["class"]==1].count()], values='class', 
        names='class', 
        title='LC-40')
        fig.update_layout(transition_duration=500)
        return fig
    elif entered_site == 'SLC-40':
        fig = px.pie(slc40.groupby(['class'])['class'].count(), values='class', 
        names='class', 
        title='SLC-40')
        fig.update_layout(transition_duration=500)
        return fig
    elif entered_site == 'SLC-4E':
        fig = px.pie(slc4E.groupby(['class'])['class'].count(), values='class', 
        names='class', 
        title='SLC-4E')
        fig.update_layout(transition_duration=500)
        return fig
    elif entered_site == 'LC-39A':
        fig = px.pie(lc39A.groupby(['class'])['class'].count(), values='class', 
        names='class', 
        title='LC-39A')
        fig.update_layout(transition_duration=500)
        return fig
    
    # return the outcomes piechart for a selected site

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")
)

def get_scatter_chart(entered_site, payload):
    filtered_df = spacex_df
    lc40 = spacex_df[spacex_df["Launch Site"]=="CCAFS LC-40"]
    slc40 = spacex_df[spacex_df["Launch Site"]=="CCAFS SLC-40"]
    slc4E = spacex_df[spacex_df["Launch Site"]=="VAFB SLC-4E"]
    lc39A = spacex_df[spacex_df["Launch Site"]=="KSC LC-39A"]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        fig.update_layout(transition_duration=500)
        return fig
    elif entered_site =='LC-40':
        fig = px.scatter(lc40, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        fig.update_layout(transition_duration=500)
        return fig
    elif entered_site == 'SLC-40':
        fig = px.scatter(slc40, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        fig.update_layout(transition_duration=500)
        return fig
    elif entered_site == 'SLC-4E':
        fig = px.scatter(slc4E, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        fig.update_layout(transition_duration=500)
        return fig
    elif entered_site == 'LC-39A':
        fig = px.scatter(lc39A, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        fig.update_layout(transition_duration=500)
        return fig
    






# Run the app
if __name__ == '__main__':
    app.run_server()
