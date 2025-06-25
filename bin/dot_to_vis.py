#!/usr/bin/python

import pydot
import json
import sys
import argparse
import re # Import re module

def get_node_attributes(node_obj):
    attrs = {}
    raw_label = node_obj.get_label()

    if raw_label:
        # 1. Strip potential surrounding quotes from pydot
        processed_label = raw_label.strip('"')

        # 2. Correct the double escaping of backslashes for LaTeX commands
        #    If JSON shows \\\\command, it means Python string was \\command.
        #    We want Python string to be \command.
        #    This regex targets \\ followed by letters (commands) or { or }
        processed_label = re.sub(r'\\\\([a-zA-Z{}])', r'\\\1', processed_label)
        
        # Also handle cases like \\\\ for LaTeX newline inside cases, if they became \\\\ in Python string
        # This is less likely if re.sub above is specific enough.
        # If re.sub is too greedy, you might need to adjust.
        # For now, let's assume re.sub handles common LaTeX commands.

        # 3. Ensure DOT's \n for visual newlines are actual newlines
        # This should happen *after* LaTeX backslash correction if \\n was meant for LaTeX.
        # But typically \n in DOT is for visual break.
        processed_label = processed_label.replace("\\n", "\n")


        attrs['label'] = processed_label
    else:
        attrs['label'] = node_obj.get_name().strip('"')

    fillcolor = node_obj.get_fillcolor()
    if fillcolor:
        attrs['color_background'] = fillcolor.strip('"')
    
    shape = node_obj.get_shape()
    if shape:
        shape_val = shape.strip('"').lower()
        if shape_val == 'mdiamond':
            attrs['shape'] = 'diamond'
        elif shape_val == 'msquare':
            attrs['shape'] = 'square'
        else:
            attrs['shape'] = shape_val if shape_val else 'box' # Default to box if shape is empty string
    else:
        attrs['shape'] = 'box' # Default to box if no shape attribute
        
    return attrs

# ... (rest of your main function and dot_to_visjs_data from previous correct version)
def dot_to_visjs_data(dot_string):
    graphs = pydot.graph_from_dot_data(dot_string)
    if not graphs:
        print("Error: Could not parse DOT data.", file=sys.stderr)
        return None
    graph = graphs[0] 
    
    nodes_vis = []
    edges_vis = []
    
    node_ids_processed = set()

    for pydot_node in graph.get_nodes():
        node_id = pydot_node.get_name().strip('"')
        if node_id.lower() in ["graph", "node", "edge"]: 
            continue
        if node_id not in node_ids_processed:
            attrs = get_node_attributes(pydot_node)
            vis_node_data = {"id": node_id, **attrs}
            nodes_vis.append(vis_node_data)
            node_ids_processed.add(node_id)

    for pydot_edge in graph.get_edges():
        source_id = pydot_edge.get_source().strip('"')
        destination_id = pydot_edge.get_destination().strip('"')
        
        if source_id not in node_ids_processed:
            nodes_vis.append({"id": source_id, "label": source_id, "shape": "box"})
            node_ids_processed.add(source_id)
            
        if destination_id not in node_ids_processed:
            nodes_vis.append({"id": destination_id, "label": destination_id, "shape": "box"})
            node_ids_processed.add(destination_id)
            
        edges_vis.append({"from": source_id, "to": destination_id})
            
    return {"nodes": nodes_vis, "edges": edges_vis}

def main():
    parser = argparse.ArgumentParser(description="Convert DOT graph to Vis.js JSON format.")
    parser.add_argument("dotfile", type=str, help="Path to the input DOT file.")
    
    args = parser.parse_args()
    
    try:
        with open(args.dotfile, 'r', encoding='utf-8') as f:
            dot_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.dotfile}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
        
    visjs_data = dot_to_visjs_data(dot_content)
    
    if visjs_data:
        print(json.dumps(visjs_data, indent=2))

if __name__ == "__main__":
    main()
