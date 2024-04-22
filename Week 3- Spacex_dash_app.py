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
                                dcc.Dropdown(
                                    id='site-dropdown',
                                     options=[{'label': 'All Sites', 'value': 'ALL'},
                                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}                                     
                                     ],
                                     value='ALL',
                                     placeholder='Select a Launch Site',
                                     searchable = True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='playload_slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0', 100: '100'},
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
   
    if entered_site == 'ALL':
        success_by_all_sites_df = spacex_df[spacex_df['class'] == 1].groupby('Launch Site')['class'].count().reset_index()
        fig_all_sites = px.pie(success_by_all_sites_df, 
        values='class', 
        names='Launch Site', 
        title='Success launches By Sites')       
         # return the outcomes piechart for a selected site
        return fig_all_sites       

    else: # only show the success/fail rate of the selected site
        # Filter the DataFrame by the launch site
        selected_site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Group by the 'class' column and count the occurrences of each class
        success_fail_count = selected_site_df.groupby('class').size()
        fig_selected_site = px.pie(success_fail_count, 
        values= success_fail_count, 
        names=success_fail_count.index, 
        title=f'Success/Fail launches of the Launch Site {entered_site}'   
        )     
        # return the outcomes piechart for a selected site
        return fig_selected_site 


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
   Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="playload_slider", component_property="value")]
    )

def get_scatter_chart( entered_site, playload_slider):
    if entered_site == 'ALL':
        fig_scatter_all = px.scatter(spacex_df, 
                 x='Payload Mass (kg)', 
                 y='class', 
                 color='Booster Version Category',
                 title='Payload Mass vs. Success Rate by Booster Version Category',
                 labels={'Payload Mass (kg)': 'Payload Mass', 'class': 'Success Rate'}
                )
        return fig_scatter_all
    else: #filter by selected site and the payload mass range
        filtered_df = spacex_df.loc[(spacex_df['Launch Site'] == entered_site) & 
                             (spacex_df['Payload Mass (kg)'] >= playload_slider[0]) & 
                             (spacex_df['Payload Mass (kg)'] <= playload_slider[1])]
        fig_scatter_by_site = px.scatter(filtered_df , 
                x='Payload Mass (kg)', 
                y='class', 
                 color='Booster Version Category',
                 title='Payload Mass vs. Success Rate by Booster Version Category',
                 labels={'Payload Mass (kg)': 'Payload Mass', 'class': 'Success Rate'}
                )
        return fig_scatter_by_site



def update_output_container(payloadmass, selected_site):
   get_pie_chart(selected_site)

# Run the app
if __name__ == '__main__':
    app.run_server()
