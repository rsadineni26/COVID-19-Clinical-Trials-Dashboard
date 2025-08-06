import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the data
df = pd.read_csv("COVID clinical trials.csv")
df['Country'] = df['Locations'].apply(lambda x: str(x).split(',')[-1].strip())

# Clean column names and data
df.columns = df.columns.str.strip()
df['Country'] = df['Country'].astype(str).str.strip()
df['Status'] = df['Status'].astype(str).str.strip()
df['Funded Bys'] = df['Funded Bys'].astype(str).str.strip()

# Initialize the Dash app
app = Dash(__name__)
app.title = "COVID Clinical Trials Dashboard"

# Layout
app.layout = html.Div([
    html.H1("COVID Clinical Trials Dashboard", style={'textAlign': 'center'}),

    html.Label("Select a Country:"),
    dcc.Dropdown(
        id='country_dropdown',
        options=[{'label': c, 'value': c} for c in sorted(df['Country'].dropna().unique())],
        value='United States',
        style={'width': '50%'}
    ),

    html.Div([
        dcc.Graph(id='status_bar_chart'),
        dcc.Graph(id='funding_pie_chart')
    ])
])

# Callback to update charts
@app.callback(
    [Output('status_bar_chart', 'figure'),
     Output('funding_pie_chart', 'figure')],
    [Input('country_dropdown', 'value')]
)
def update_dashboard(selected_country):
    filtered_df = df[df['Country'] == selected_country]

    if filtered_df.empty:
        return (
            px.bar(title=f"No data found for {selected_country}"),
            px.pie(names=[], values=[], title="No data")
        )

    # Bar chart: Trial Status
    status_counts = filtered_df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    status_fig = px.bar(
        status_counts, x='Status', y='Count',
        title=f"Trial Statuses in {selected_country}",
        color='Status'
    )

    # Pie chart: Top 5 Funding Sources
    funding_counts = filtered_df['Funded Bys'].value_counts().nlargest(5).reset_index()
    funding_counts.columns = ['Funding Source', 'Count']
    funding_fig = px.pie(
        funding_counts, names='Funding Source', values='Count',
        title=f"Top 5 Funding Sources in {selected_country}",
        hole=0.4
    )

    return status_fig, funding_fig

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
