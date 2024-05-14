# Import necessary libraries
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)
server = app.server

# Load the cleaned dataset
cleaned_file_path = 'cleaned_telco_customer_churn.csv'
data = pd.read_csv(cleaned_file_path)

# App title
app.title = 'Telco Customer Churn Dashboard'

# Define the app layout
app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="Telco Customer Churn Dashboard",
        brand_href="#",
        color="primary",
        dark=True,
    ),
    dbc.Tabs([
        dbc.Tab(label='Churn Overview', tab_id='tab-churn-overview'),
        dbc.Tab(label='Customer Demographics', tab_id='tab-customer-demographics'),
        dbc.Tab(label='Service Subscription Data', tab_id='tab-service-subscription-data'),
        dbc.Tab(label='Account Information', tab_id='tab-account-information'),
        dbc.Tab(label='Charges Analysis', tab_id='tab-charges-analysis'),
    ], id="tabs", active_tab='tab-churn-overview', className='mt-4'),
    html.Div(id='content', className='mt-4'),
], fluid=True)

# Callback to update the displayed section based on the selected tab
@app.callback(
    Output('content', 'children'),
    [Input('tabs', 'active_tab')]
)
def render_content(tab):
    if tab == 'tab-churn-overview':
        return dbc.Card([
            dbc.CardBody([
                html.H2("Churn Overview", className='card-title'),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='churn-pie-chart'), md=6),
                    dbc.Col(dcc.Graph(id='churn-bar-chart'), md=6),
                ]),
            ])
        ])
    elif tab == 'tab-customer-demographics':
        return dbc.Card([
            dbc.CardBody([
                html.H2("Customer Demographics", className='card-title'),
                dcc.Dropdown(
                    id='demographics-dropdown',
                    options=[
                        {'label': 'Gender', 'value': 'gender'},
                        {'label': 'Senior Citizen', 'value': 'SeniorCitizen'},
                        {'label': 'Partner', 'value': 'Partner'},
                        {'label': 'Dependents', 'value': 'Dependents'}
                    ],
                    value='gender',
                    className='mb-4'
                ),
                dcc.Graph(id='demographics-bar-chart'),
                dcc.Graph(id='age-histogram'),
                dcc.Graph(id='demographics-heatmap'),
            ])
        ])
    elif tab == 'tab-service-subscription-data':
        return dbc.Card([
            dbc.CardBody([
                html.H2("Service Subscription Data", className='card-title'),
                dcc.Checklist(
                    id='service-checklist',
                    options=[
                        {'label': 'Phone Service', 'value': 'PhoneService'},
                        {'label': 'Multiple Lines', 'value': 'MultipleLines'},
                        {'label': 'Internet Service', 'value': 'InternetService'},
                        {'label': 'Online Security', 'value': 'OnlineSecurity'},
                        {'label': 'Online Backup', 'value': 'OnlineBackup'},
                        {'label': 'Device Protection', 'value': 'DeviceProtection'},
                        {'label': 'Tech Support', 'value': 'TechSupport'},
                        {'label': 'Streaming TV', 'value': 'StreamingTV'},
                        {'label': 'Streaming Movies', 'value': 'StreamingMovies'}
                    ],
                    value=['PhoneService'],
                    className='mb-4'
                ),
                dcc.Graph(id='service-stacked-bar-chart'),
                dcc.Graph(id='service-pie-chart'),
            ])
        ])
    elif tab == 'tab-account-information':
        return dbc.Card([
            dbc.CardBody([
                html.H2("Account Information", className='card-title'),
                dcc.Dropdown(
                    id='account-dropdown',
                    options=[
                        {'label': 'Contract Type', 'value': 'Contract'},
                        {'label': 'Payment Method', 'value': 'PaymentMethod'},
                        {'label': 'Paperless Billing', 'value': 'PaperlessBilling'}
                    ],
                    value='Contract',
                    className='mb-4'
                ),
                dcc.Slider(
                    id='tenure-slider',
                    min=data['tenure'].min(),
                    max=data['tenure'].max(),
                    value=data['tenure'].min(),
                    marks={str(tenure): str(tenure) for tenure in data['tenure'].unique()},
                    className='mb-4'
                ),
                dcc.Graph(id='tenure-line-chart'),
                dcc.Graph(id='account-bar-chart'),
                dcc.Graph(id='account-box-plot'),
            ])
        ])
    elif tab == 'tab-charges-analysis':
        return dbc.Card([
            dbc.CardBody([
                html.H2("Charges Analysis", className='card-title'),
                dcc.RangeSlider(
                    id='charges-range-slider',
                    min=data['MonthlyCharges'].min(),
                    max=data['MonthlyCharges'].max(),
                    step=5,
                    value=[data['MonthlyCharges'].min(), data['MonthlyCharges'].max()],
                    marks={str(charge): str(charge) for charge in range(int(data['MonthlyCharges'].min()), int(data['MonthlyCharges'].max())+1, 10)},
                    className='mb-4'
                ),
                dcc.Graph(id='charges-scatter-plot'),
                dcc.Graph(id='charges-box-plot'),
            ])
        ])

# Callbacks for Churn Overview Section
@app.callback(
    Output('churn-pie-chart', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_churn_pie_chart(tab):
    if tab == 'tab-churn-overview':
        churn_counts = data['Churn'].value_counts()
        churn_counts.index = ['Not Churned', 'Churned']
        fig = px.pie(values=churn_counts, names=churn_counts.index, title='Churn Distribution', color_discrete_sequence=px.colors.qualitative.Set2)
        return fig

@app.callback(
    Output('churn-bar-chart', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_churn_bar_chart(tab):
    if tab == 'tab-churn-overview':
        churn_by_gender = data.groupby('gender')['Churn'].mean().reset_index()
        fig = px.bar(churn_by_gender, x='gender', y='Churn', title='Churn Rate by Gender', color='gender', color_discrete_map={'Female': 'pink', 'Male': 'blue'})
        return fig

# Callbacks for Customer Demographics Section
@app.callback(
    Output('demographics-bar-chart', 'figure'),
    [Input('demographics-dropdown', 'value')]
)
def update_demographics_bar_chart(selected_demographic):
    if selected_demographic == 'gender':
        demographic_counts = data[selected_demographic].value_counts()
        fig = px.bar(demographic_counts, title=f'Distribution of {selected_demographic.capitalize()}', color=demographic_counts.index, color_discrete_map={'Male': 'blue', 'Female': 'pink'})
    else:
        demographic_counts = data[selected_demographic].value_counts()
        demographic_counts.index = ['No', 'Yes']
        fig = px.bar(demographic_counts, title=f'Distribution of {selected_demographic.capitalize()}', color=demographic_counts.index,color_discrete_map={'Yes': 'blue', 'No': 'red'})
    return fig

@app.callback(
    Output('age-histogram', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_age_histogram(tab):
    if tab == 'tab-customer-demographics':
        fig = px.histogram(data, x='tenure', title='Distribution of Tenure', color_discrete_sequence=px.colors.qualitative.Set2)
        return fig

@app.callback(
    Output('demographics-heatmap', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_demographics_heatmap(tab):
    if tab == 'tab-customer-demographics':
        # Convert categorical variables to dummy/indicator variables
        df_encoded = pd.get_dummies(data[['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Churn']], drop_first=True)
        
        # Calculate the correlation matrix
        correlation = df_encoded.corr()
        
        # Create the heatmap
        fig = px.imshow(correlation, title='Correlation Heatmap', color_continuous_scale='Viridis')
        return fig

# Callbacks for Service Subscription Data Section
@app.callback(
    Output('service-stacked-bar-chart', 'figure'),
    [Input('service-checklist', 'value')]
)
def update_service_stacked_bar_chart(selected_services):
    service_data = data[selected_services]
    service_counts = service_data.apply(pd.Series.value_counts).fillna(0)
    fig = px.bar(service_counts, barmode='stack', title='Service Subscription Counts', color_discrete_sequence=px.colors.qualitative.Set2)
    return fig

@app.callback(
    Output('service-pie-chart', 'figure'),
    [Input('service-checklist', 'value')]
)
def update_service_pie_chart(selected_services):
    # Create a DataFrame with only the selected services
    service_data = data[selected_services]

    # Count the number of customers with 'Yes' for each selected service
    service_sums = service_data.apply(lambda x: x[x == 'Yes'].count())

    # Normalize the counts to get the proportion
    service_proportions = service_sums / service_sums.sum()

    # Create the pie chart
    fig = px.pie(values=service_proportions, names=service_proportions.index, title='Service Subscription Distribution', color_discrete_sequence=px.colors.qualitative.Set2)
    return fig

# Callbacks for Account Information Section
@app.callback(
    Output('tenure-line-chart', 'figure'),
    [Input('tenure-slider', 'value')]
)
def update_tenure_line_chart(selected_tenure):
    filtered_data = data[data['tenure'] <= selected_tenure]
    tenure_trend = filtered_data.groupby('tenure').size()
    fig = px.line(tenure_trend, title='Tenure Trend Over Time', color_discrete_sequence=px.colors.qualitative.Set2)
    return fig

@app.callback(
    Output('account-bar-chart', 'figure'),
    [Input('account-dropdown', 'value')]
)
def update_account_bar_chart(selected_account_feature):
    account_data = data[selected_account_feature].value_counts()
    if selected_account_feature in ['PaperlessBilling']:
        account_data.index = ['No', 'Yes']
    fig = px.bar(account_data, title=f'{selected_account_feature} Distribution', color=account_data.index, color_discrete_sequence=px.colors.qualitative.Set2)
    return fig

@app.callback(
    Output('account-box-plot', 'figure'),
    [Input('account-dropdown', 'value')]
)
def update_account_box_plot(selected_account_feature):
    if selected_account_feature in ['Contract']:
        fig = px.box(data, y='MonthlyCharges', x=selected_account_feature, title='Monthly Charges Distribution', color=selected_account_feature, color_discrete_sequence=px.colors.qualitative.Set2)
    else:
        fig = px.box(data, y='MonthlyCharges', x=selected_account_feature, title='Monthly Charges Distribution', color=selected_account_feature, color_discrete_sequence=px.colors.qualitative.Set2)
    return fig

# Callbacks for Charges Analysis Section
@app.callback(
    Output('charges-scatter-plot', 'figure'),
    [Input('charges-range-slider', 'value')]
)
def update_charges_scatter_plot(selected_range):
    filtered_data = data[(data['MonthlyCharges'] >= selected_range[0]) & (data['MonthlyCharges'] <= selected_range[1])]
    fig = px.scatter(filtered_data, x='MonthlyCharges', y='TotalCharges', color='Churn', title='Charges Scatter Plot',
                     labels={'Churn': 'Customer Status'},
                     color_discrete_map={'0': 'blue', '1': 'yellow'})
    return fig

@app.callback(
    Output('charges-box-plot', 'figure'),
    [Input('charges-range-slider', 'value')]
)
def update_charges_box_plot(selected_range):
    filtered_data = data[(data['MonthlyCharges'] >= selected_range[0]) & (data['MonthlyCharges'] <= selected_range[1])]
    fig = px.box(filtered_data, y='MonthlyCharges', color='Churn', title='Charges Box Plot',
                 labels={'0': 'Not Churned', '1': 'Churned'},
                 color_discrete_map={'0': '#2ca02c', '1': '#d62728'})
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0')
