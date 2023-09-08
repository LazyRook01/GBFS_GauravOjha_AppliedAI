import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Define the graph
start_node = '1'
goal_node = '7'
graph_relation = {
    "1": ["2", "3", "4"],
    "2": ["5", "6", "7"],
    "3": ["7"],
    "4": ["7"],
    "5": [],
    "6": [],
    "7": [],
}

# Define the heuristic values
heuristic = {
    "1": 8,
    "2": 8,
    "3": 4,
    "4": 3,
    "5": float('inf'),
    "6": float('inf'),
    "7": 0,
}

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for node, neighbors in graph_relation.items():
    G.add_node(node, heuristic=heuristic[node])
    G.add_edges_from([(node, neighbor) for neighbor in neighbors])

# Define the positions for the nodes (you can customize this if needed)
pos = nx.spring_layout(G)

# Get the heuristic labels
heuristic_labels = {node: f'h={data["heuristic"]}' for node, data in G.nodes(data=True)}

# Initialize Streamlit app
st.title('GBFS Visualization')

visited = {}  # Store visited nodes and their predecessors

def best_first_search(graph, start, goal, heuristic, pos):
    que = [(heuristic[start], start)]
    visited[start] = None

    while que:
        node_value, peak_node = heapq.heappop(que)

        if peak_node == goal:
            break

        # Visualization: Display the current node
        plt.figure(figsize=(8, 4))
        plt.title('GBFS Visualization - Exploring Node ' + peak_node)
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_color='black')
        nx.draw_networkx_labels(G, pos, labels=heuristic_labels, font_size=10, font_color='red', verticalalignment="bottom")
        nx.draw_networkx_nodes(G, pos, nodelist=[peak_node], node_color='red', node_size=500)
        st.pyplot(plt)

        for neighbour in graph[peak_node]:
            if neighbour not in visited:
                heapq.heappush(que, (heuristic[neighbour], neighbour))
                visited[neighbour] = peak_node

    return visited

if st.button("Run GBFS"):
    visited = best_first_search(graph_relation, start_node, goal_node, heuristic, pos)

    # Visualization: Highlight the final path
    plt.figure(figsize=(8, 4))
    plt.title('GBFS Visualization - Final Path')
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_color='black')
    path_nodes = list(visited.keys())
    nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_color='green', node_size=500)
    st.pyplot(plt)

    # Reconstruct the path
    node = goal_node
    path = [node]
    while node != start_node:
        node = visited[node]
        path.append(node)
    path.reverse()
    st.write("GBFS path from", start_node, "to", goal_node, ":", path)
