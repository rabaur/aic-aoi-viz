import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import yaml
from normalize_interests import normalize_interests
import matplotlib.patches as mpatches

def create_bipartite_graph(aoi_dict: dict) -> nx.Graph:
    """
    Create a bipartite graph from the areas of interest dictionary.
    
    Args:
        aoi_dict: Dictionary mapping student names to their research interests
        mapping_path: Path to the YAML mapping file
        
    Returns:
        NetworkX bipartite graph
    """
    
    # Create the graph
    G = nx.Graph()
    
    # Add nodes and edges
    for student, interests in aoi_dict.items():
        # Add student node
        G.add_node(student, bipartite=0, node_type='student')
        
        # Add interest nodes and edges
        for interest in interests:
            G.add_node(interest, bipartite=1, node_type='interest')
            G.add_edge(student, interest)
    
    return G

def visualize_bipartite_graph(G: nx.Graph, output_path: Path = None):
    """
    Visualize the bipartite graph with node sizes proportional to degree.
    """
    pos = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(30, 30))

    # Compute node degrees
    degrees = dict(G.degree())
    scale = 300  # Adjust this scale factor as needed

    # Draw student nodes (squares)
    student_nodes = [n for n, d in G.nodes(data=True) if d['node_type'] == 'student']
    student_sizes = [degrees[n] * scale for n in student_nodes]
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=student_nodes,
        node_shape='s',
        node_size=student_sizes,
        node_color='#6baed6',
        alpha=0.9,
        label='Students'
    )

    # Draw interest nodes (circles)
    interest_nodes = [n for n, d in G.nodes(data=True) if d['node_type'] == 'interest']
    interest_sizes = [degrees[n] * scale for n in interest_nodes]
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=interest_nodes,
        node_shape='o',
        node_size=interest_sizes,
        node_color='#31a354',
        alpha=0.8,
        label='Research Interests'
    )

    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=1)

    # Draw labels
    nx.draw_networkx_labels(G, pos, labels={n: n for n in student_nodes}, font_size=10, font_color='black')
    nx.draw_networkx_labels(G, pos, labels={n: n for n in interest_nodes}, font_size=8, font_color='black')

    # Custom legend
    student_patch = mpatches.Patch(color='#6baed6', label='Students')
    interest_patch = mpatches.Patch(color='#31a354', label='Research Interests')
    plt.legend(handles=[student_patch, interest_patch], loc='upper right')

    plt.axis('off')
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Example usage
    mapping_path = Path("data/processed/aoi_info_dict.yaml")

    aoi_dict = yaml.load(open(mapping_path), Loader=yaml.FullLoader)
    
    # Create and visualize the graph
    G = create_bipartite_graph(aoi_dict)
    visualize_bipartite_graph(G, Path("bipartite_graph.png"))
    
    # Print some basic statistics
    print(f"Number of students: {len([n for n, d in G.nodes(data=True) if d['node_type'] == 'student'])}")
    print(f"Number of unique interests: {len([n for n, d in G.nodes(data=True) if d['node_type'] == 'interest'])}")
    print(f"Number of edges: {G.number_of_edges()}") 