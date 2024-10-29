from flask import Flask, render_template
from markupsafe import Markup
import networkx as nx
import plotly.graph_objs as go
from collections import Counter
from itertools import combinations
import re

app = Flask(__name__)

# Route for the main dashboard page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the Network Graph page
@app.route('/network-graph')
def network_graph():
    # Generate the network graph HTML
    graph_html = generate_network_graph_interactive()
    return render_template('network_graph.html', graph_html=Markup(graph_html))

# Route for Sentiment Overview detailed page
@app.route('/sentiment-overview')
def sentiment_overview():
    return render_template('sentiment-overview.html')

# Route for Sentiment Trend detailed page
@app.route('/sentiment-trend')
def sentiment_trend():
    return render_template('sentiment-trend.html')

@app.route('/index3')
def index3():
    return render_template('index3.html')

@app.route('/Pdo-Hackathon')
def Pdo_Hackathon():
    return render_template('Pdo_Hackathon.html')

# Route for Platform Distribution detailed page
@app.route('/platform-distribution')
def platform_distribution():
    return render_template('platform-distribution.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')

# Route for Engagement Data detailed page
@app.route('/engagement-data')
def engagement_data():
    return render_template('engagement-data.html')

# Route for Engagement Timeline detailed page
@app.route('/engagement-timeline')
def engagement_timeline():
    return render_template('engagement-timeline.html')

# Route for Top Influencers detailed page
@app.route('/top-influencers')
def top_influencers():
    return render_template('top-influencers.html')

@app.route('/tweet-sentiment-scale')
def tweet_sentiment_scale():
    return render_template('tweet-sentiment-scale.html')

# Function to generate the network graph using Plotly and NetworkX
def generate_network_graph_interactive():
    # Sample data for testing purposes
    replies = [
        "I think the project needs improvement in efficiency.",
        "It's really good to see progress being made!",
        "I am not happy with the current performance."
    ]
    
    # Preprocess the replies
    processed_replies = []
    stopwords = set(['is', 'to', 'on', 'the', 'a', 'it', 'by', 'in', 'needs', 'really'])

    for reply in replies:
        words = re.sub(r'[^\w\s]', '', reply).lower().split()  # Remove punctuation and lowercase
        words = [word for word in words if word not in stopwords]  # Remove stopwords
        processed_replies.append(words)

    # Count co-occurrences of words
    co_occurrence = Counter()

    for words in processed_replies:
        for pair in combinations(set(words), 2):  # Create word pairs
            co_occurrence[pair] += 1

    # Create a graph using NetworkX
    G = nx.Graph()

    # Add edges based on co-occurrence data
    for (word1, word2), weight in co_occurrence.items():
        G.add_edge(word1, word2, weight=weight)

    # Get node positions using a layout
    pos = nx.spring_layout(G, k=0.5)

    # Extract node and edge information
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=15,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    # Add node degree as a color scale
    node_adjacencies = []
    for node in G.nodes():
        adjacencies = list(G.adj[node])
        node_adjacencies.append(len(adjacencies))

    node_trace.marker.color = node_adjacencies

    # Create the figure using Plotly
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Network graph from user replies',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # Generate the HTML for the graph
    graph_html = fig.to_html(full_html=False)
    return graph_html

if __name__ == '__main__':
    app.run(debug=True)
