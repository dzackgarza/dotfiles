#!/usr/bin/env python3
import pydot
import json
import sys
import argparse
import re

# --- X11 to CSS/Hex Color Mapping ---
# Add more as needed, or use a more comprehensive library if you have many X11 colors
X11_TO_CSS_COLOR_MAP = {
    "darkolivegreen1": "#caff70", # Approx
    "khaki1": "#fff68f",         # Approx
    "thistle1": "#ffe1ff",       # Approx
    "mistyrose": "#ffe4e1",
    "honeydew2": "#e0eee0",       # Approx (honeydew is #f0fff0)
    "burlywood1": "#ffd39b",      # Approx
    "lightskyblue": "#87cefa",
    "darkolivegreen": "#556b2f",
    "darkgoldenrod": "#b8860b",
    "purple3": "#7d26cd",        # Approx for a vibrant purple
    "firebrick3": "#cd2626",      # Approx
    "seagreen": "#2e8b57",
    "sienna": "#a0522d",
    "dodgerblue": "#1e90ff",
    "lightblue": "#add8e6",
    # Standard colors that are usually fine
    "lightgrey": "#d3d3d3",
    "black": "#000000",
    "white": "#ffffff",
    "red": "#ff0000",
    "green": "#008000",
    "blue": "#0000ff",
    "orange": "#ffa500"
}

def map_color(dot_color_name, default_css_color):
    """Maps a DOT color name to a standard CSS/Hex color."""
    if not dot_color_name:
        return default_css_color
    
    clean_name = dot_color_name.strip('"').lower()
    
    if clean_name.startswith("#"): # Already a hex code
        return clean_name
    
    return X11_TO_CSS_COLOR_MAP.get(clean_name, default_css_color)


def get_node_attributes_for_cytoscape(node_obj):
    attrs = {}
    node_id = node_obj.get_name().strip('"')
    attrs['id'] = node_id
    
    raw_label_from_pydot = node_obj.get_label()
    
    if raw_label_from_pydot:
        label_content = raw_label_from_pydot.strip('"') 
        label_content = label_content.replace("\\n", "\n")
        
        label_content = re.sub(r'\\\\([a-zA-Z{}()[\],;])', r'\\\1', label_content)
        label_content = re.sub(r'\\\\(\s)', r'\\\1', label_content) 
        label_content = re.sub(r'\\\\(\d)', r'\\\1', label_content) 
        label_content = re.sub(r'\\\\([^\w\s])', r'\\\1', label_content)

        attrs['texLabel'] = label_content 
        attrs['label'] = node_id # Fallback label
    else:
        attrs['id'] = node_id
        attrs['label'] = node_id 
        attrs['texLabel'] = node_id 

    attrs['backgroundColor'] = map_color(node_obj.get_fillcolor(), "#ffffff") # Default white

    shape = node_obj.get_shape()
    cs_shape = 'rectangle' # Cytoscape default
    if shape:
        dot_shape = shape.strip('"').lower()
        if dot_shape == 'box': cs_shape = 'rectangle'
        elif dot_shape == 'mdiamond': cs_shape = 'diamond'
        elif dot_shape == 'msquare': cs_shape = 'rectangle' 
        elif dot_shape in ['ellipse', 'circle', 'triangle', 'diamond', 'pentagon', 'hexagon', 'octagon', 'star', 'vee']:
            cs_shape = dot_shape
        elif not dot_shape: cs_shape = 'rectangle'
    attrs['shape'] = cs_shape
    return attrs

def get_subgraph_style_attr(subgraph_obj, attr_name):
    """Safely gets a style attribute from a subgraph."""
    attr_val = subgraph_obj.get(attr_name) 
    if attr_val:
        if isinstance(attr_val, list):
            return attr_val[0].strip('"') 
        return attr_val.strip('"')
    return None

def dot_to_cytoscape_data(dot_string):
    graphs = pydot.graph_from_dot_data(dot_string)
    if not graphs:
        print("Error: Could not parse DOT data.", file=sys.stderr)
        return None
    graph = graphs[0] 
    
    elements = [] 
    node_ids_processed = set()
    node_to_parent_cluster = {}

    for subgraph in graph.get_subgraphs():
        subgraph_name = subgraph.get_name()
        if subgraph_name.lower().startswith('cluster_'):
            if subgraph_name not in node_ids_processed:
                cluster_label_raw = subgraph.get_label() 
                clean_cluster_label = cluster_label_raw.strip('"') if cluster_label_raw else subgraph_name
                
                fontname = get_subgraph_style_attr(subgraph, 'fontname')
                font_weight = "bold" if fontname and "bold" in fontname.lower() else "normal"

                elements.append({
                    'data': {
                        'id': subgraph_name,
                        'label': clean_cluster_label,
                        'isCluster': True,
                        # Store style data in 'data' for stylesheet to use
                        'clusterBackgroundColor': map_color(get_subgraph_style_attr(subgraph, 'fillcolor'), '#D3D3D3'),
                        'clusterBorderColor': map_color(get_subgraph_style_attr(subgraph, 'color'), 'black'),
                        'clusterFontWeight': font_weight
                    }
                })
                node_ids_processed.add(subgraph_name)

            for pydot_node in subgraph.get_nodes():
                node_id = pydot_node.get_name().strip('"')
                if node_id.lower() not in ["graph", "node", "edge"]:
                    node_to_parent_cluster[node_id] = subgraph_name
    
    all_pydot_nodes = graph.get_nodes() 
    for sg in graph.get_subgraphs():
        all_pydot_nodes.extend(sg.get_nodes())
    
    unique_nodes_to_process = {} 
    for pydot_node in all_pydot_nodes:
        node_id = pydot_node.get_name().strip('"')
        if node_id.lower() not in ["graph", "node", "edge"] and not node_id.lower().startswith('cluster_'):
            if node_id not in unique_nodes_to_process: 
                 unique_nodes_to_process[node_id] = pydot_node

    for node_id, pydot_node_obj in unique_nodes_to_process.items():
        if node_id not in node_ids_processed: 
            attrs = get_node_attributes_for_cytoscape(pydot_node_obj)
            node_data = {'id': node_id, **attrs} 
            
            if node_id in node_to_parent_cluster :
                 node_data['parent'] = node_to_parent_cluster[node_id]
            
            elements.append({'data': node_data})
            node_ids_processed.add(node_id)

    edge_id_counts = {} # To ensure unique edge IDs
    for pydot_edge in graph.get_edges():
        source_id = pydot_edge.get_source().strip('"')
        destination_id = pydot_edge.get_destination().strip('"')
        
        if source_id not in node_ids_processed:
            elements.append({'data': {'id': source_id, 'label': source_id, 'texLabel': source_id, 'shape': 'rectangle'}})
            node_ids_processed.add(source_id)
        if destination_id not in node_ids_processed:
            elements.append({'data': {'id': destination_id, 'label': destination_id, 'texLabel': destination_id, 'shape': 'rectangle'}})
            node_ids_processed.add(destination_id)

        base_edge_id = f"{source_id}_to_{destination_id}"
        edge_id_counts[base_edge_id] = edge_id_counts.get(base_edge_id, 0) + 1
        final_edge_id = f"{base_edge_id}_{edge_id_counts[base_edge_id]}" if edge_id_counts[base_edge_id] > 1 else base_edge_id
        
        edge_data = {'id': final_edge_id, 'source': source_id, 'target': destination_id}
        
        label = pydot_edge.get_label()
        color = pydot_edge.get_color()
        style = pydot_edge.get_style()

        if label:
            edge_data['label'] = label.strip('"').replace("\\n", "\n")
        if color:
            edge_data['line_color'] = map_color(color, '#ccc') # Default edge color
        if style:
            edge_data['line_style'] = style.strip('"')
        
        elements.append({'data': edge_data})
            
    return elements

def main():
    parser = argparse.ArgumentParser(description="Convert DOT graph to Cytoscape.js JSON format.")
    parser.add_argument("dotfile", type=str, help="Path to the input DOT file.")
    args = parser.parse_args()
    try:
        with open(args.dotfile, 'r', encoding='utf-8') as f:
            dot_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.dotfile}", file=sys.stderr)
        sys.exit(1)
    cytoscape_elements = dot_to_cytoscape_data(dot_content)
    if cytoscape_elements:
        print(json.dumps(cytoscape_elements, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
