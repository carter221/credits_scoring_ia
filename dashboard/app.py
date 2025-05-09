import os
import pandas as pd
import numpy as np
import requests
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # for deployment

# In a real application, this would load your data from a database
# For this example, we'll create some dummy data
def load_sample_data():
    # Create dummy data for demonstration
    np.random.seed(42)
    client_ids = [f"client_{i}" for i in range(1000)]
    
    data = {
        'client_id': client_ids,
        'age': np.random.normal(40, 10, 1000).astype(int),
        'income': np.random.normal(50000, 15000, 1000),
        'employment_years': np.random.normal(7, 4, 1000),
        'debt_to_income': np.random.normal(0.3, 0.1, 1000),
        'credit_score': np.random.normal(650, 100, 1000).astype(int),
        'num_previous_loans': np.random.poisson(2, 1000),
        'loan_amount': np.random.normal(15000, 5000, 1000),
        'loan_term': np.random.choice([12, 24, 36, 48, 60], 1000)
    }
    
    # Create a dataframe
    df = pd.DataFrame(data)
    return df

# Load sample data
df = load_sample_data()

# API endpoint
API_ENDPOINT = "http://localhost:5000/predict"

# App layout
app.layout = html.Div([
    html.H1("Home Credit - Dashboard de Scoring Crédit", 
            style={'textAlign': 'center', 'margin': '20px', 'color': '#2c3e50'}),
    
    html.Div([
        html.Div([
            html.H3("Recherche Client"),
            dcc.Input(
                id='client-search',
                type='text',
                placeholder='Entrez ID client...',
                style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}
                ),
                html.Button(
                    'Rechercher', 
                    id='search-button', 
                    style={
                    'width': '100%', 
                    'backgroundColor': '#3498db', 
                    'color': 'white', 
                    'border': 'none', 
                    'padding': '10px', 
                    'borderRadius': '5px'
                }
            ),
            html.Hr(),
            html.H3("Informations Client"),
            html.Div(id='client-info')
        ], style={'width': '30%', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.H3("Score de Crédit"),
            html.Div(id='credit-score-display'),
            html.Hr(),
            html.H3("Importance des Facteurs"),
            dcc.Graph(id='feature-importance'),
            html.Hr(),
            html.H3("Comparaison avec des Clients Similaires"),
            dcc.Graph(id='client-comparison')
        ], style={'width': '65%', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'margin': '20px'})
])

# Callback for updating client information
@app.callback(
    [Output('client-info', 'children'),
     Output('credit-score-display', 'children'),
     Output('feature-importance', 'figure'),
     Output('client-comparison', 'figure')],
    [Input('search-button', 'n_clicks')],
    [State('client-search', 'value')]
)
def update_client_info(n_clicks, client_id):
    if n_clicks is None or client_id is None:
        return [
            "Aucun client sélectionné",
            "Aucun score disponible",
            go.Figure(),
            go.Figure()
        ]
    
    # Filter dataframe for the specific client
    client_data = df[df['client_id'] == client_id]
    
    if client_data.empty:
        return [
            "Client non trouvé",
            "Aucun score disponible",
            go.Figure(),
            go.Figure()
        ]
    
    # Extract client features
    client_features = client_data.iloc[0].to_dict()
    
    try:
        # Réel appel API avec les caractéristiques du client
        response = requests.post(API_ENDPOINT, json=client_features)
        
        if response.status_code == 200:
            prediction_data = response.json()
        else:
            return [
                html.Div([
                    html.P(f"ID: {client_id}"),
                    html.P(f"Erreur API: {response.status_code} - {response.text}")
                ]),
                "Erreur lors de la récupération du score",
                go.Figure(),
                go.Figure()
            ]
        
        # Create client info display
        client_info = html.Div([
            html.P(f"ID: {client_id}"),
            html.P(f"Âge: {client_features['age']} ans"),
            html.P(f"Revenu: {client_features['income']:.2f} €"),
            html.P(f"Années d'emploi: {client_features['employment_years']:.1f} ans"),
            html.P(f"Ratio dette/revenu: {client_features['debt_to_income']:.2f}"),
            html.P(f"Score de crédit: {client_features['credit_score']}"),
            html.P(f"Nombre de prêts précédents: {client_features['num_previous_loans']}"),
            html.P(f"Montant du prêt demandé: {client_features['loan_amount']:.2f} €"),
            html.P(f"Durée du prêt: {client_features['loan_term']} mois")
        ])
        
        # Create credit score gauge
        probability = prediction_data['probability']
        decision = "Approuvé" if prediction_data['prediction'] == 1 else "Refusé"
        
        score_display = html.Div([
            dcc.Graph(
                figure=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=probability * 100,
                    title={"text": f"Probabilité de remboursement: {decision}"},
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#636EFA"},
                        'steps': [
                            {'range': [0, 33], 'color': "#EF553B"},
                            {'range': [33, 66], 'color': "#FFA15A"},
                            {'range': [66, 100], 'color': "#00CC96"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 50
                        }
                    }
                )),
                style={'height': 300}
            ),
            html.Div([
                html.H4(decision, style={'textAlign': 'center', 'color': '#00CC96' if decision == "Approuvé" else "#EF553B"}),
                html.P("Ce score indique la probabilité que le client rembourse son prêt selon notre modèle prédictif.", 
                       style={'textAlign': 'center'}),
            ])
        ])
        
        # Create feature importance chart
        feature_importance = prediction_data['feature_importance']
        feature_imp_df = pd.DataFrame({
            'Feature': list(feature_importance.keys()),
            'Importance': list(feature_importance.values())
        }).sort_values('Importance', ascending=False)
        
        feature_imp_fig = px.bar(
            feature_imp_df, 
            x='Importance', 
            y='Feature',
            title="Facteurs Influençant la Décision",
            orientation='h'
        )
        
        # Create comparison chart
        # Get similar clients (with age +/- 5 years and similar income level)
        client_age = client_features['age']
        similar_clients = df[
            (df['age'] >= client_age - 5) & 
            (df['age'] <= client_age + 5) &
            (df['client_id'] != client_id)
        ]
        
        # Calculate averages
        similar_avg = similar_clients.mean()
        
        # Select features to compare
        compare_features = ['income', 'debt_to_income', 'credit_score', 'employment_years']
        
        # Create comparison dataframe
        compare_df = pd.DataFrame({
            'Feature': compare_features,
            'Client': [client_features[f] for f in compare_features],
            'Moyenne des clients similaires': [similar_avg[f] for f in compare_features]
        })
        
        # Reshape dataframe for plotting
        compare_df = pd.melt(
            compare_df, 
            id_vars=['Feature'], 
            value_vars=['Client', 'Moyenne des clients similaires'],
            var_name='Type', 
            value_name='Valeur'
        )
        
        comparison_fig = px.bar(
            compare_df,
            x='Feature',
            y='Valeur',
            color='Type',
            barmode='group',
            title="Comparaison avec des Clients Similaires"
        )
        
        return client_info, score_display, feature_imp_fig, comparison_fig
    
    except Exception as e:
        return [
            html.Div([
                html.P(f"ID: {client_id}"),
                html.P(f"Erreur lors de la récupération des données: {str(e)}")
            ]),
            "Erreur lors de la récupération du score",
            go.Figure(),
            go.Figure()
        ]

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host='0.0.0.0', port=port, debug=True)
