# import pandas as pd
# import numpy as np

# # Load your existing file
# df = pd.read_csv('Telecom_Network_Data.csv')

# # Apply controlled perturbation
# np.random.seed(42)
# synthetic_df = df.copy()
# synthetic_df['users_connected'] = (synthetic_df['users_connected'] + np.random.normal(0, 15, len(df))).clip(0).astype(int)
# synthetic_df['download_speed'] = (synthetic_df['download_speed'] + np.random.normal(0, 3.5, len(df))).clip(1.0)
# synthetic_df['upload_speed'] = (synthetic_df['upload_speed'] + np.random.normal(0, 1.0, len(df))).clip(0.5)
# synthetic_df['latency'] = (synthetic_df['latency'] + np.random.normal(0, 5.0, len(df))).clip(5.0)
# synthetic_df['congestion'] = (synthetic_df['congestion'] + np.random.choice([0, 1], size=len(df), p=[0.9, 0.1])).clip(0, 1)

# # Save to file
# synthetic_df.to_csv('Telecom_Network_Data_Perturbed.csv', index=False)
# print("Perturbed dataset generated successfully!")

# # Load perturbed dataset
# df = pd.read_csv('Telecom_Network_Data_Perturbed.csv')
# print("Loaded columns:", df.columns.tolist())
# print("Number of rows:", len(df))

# # Let's define bands for users_connected and latency if not present
# # For example: users_connected: Low (< 300), Medium (300-700), High (> 700)
# # latency: Low (< 70), Medium (70-150), High (> 150)
# def get_users_band(val):
#     if val < 300:
#         return "Low"
#     elif val <= 700:
#         return "Medium"
#     else:
#         return "High"

# def get_latency_band(val):
#     if val < 70:
#         return "Low"
#     elif val <= 150:
#         return "Medium"
#     else:
#         return "High"

# df['users_band'] = df['users_connected'].apply(get_users_band)
# df['latency_band'] = df['latency'].apply(get_latency_band)

# # Group by timestamp to format as lines
# # Observation ID starting from 13 as in the example
# obs_id_counter = 13
# lines = []

# for timestamp, group in df.groupby('timestamp'):
#     line_tuples = []
#     for _, row in group.iterrows():
#         tower_id = int(row['tower_id'])
#         obs_id = obs_id_counter
#         obs_id_counter += 1
        
#         # Add tuples for this tower and observation
#         line_tuples.append(f"<{tower_id},hasObservation,{obs_id}>")
#         line_tuples.append(f"<{tower_id},tower_id,\"{tower_id}\">")
#         line_tuples.append(f"<{obs_id},timestamp,\"{row['timestamp']}\">")
#         line_tuples.append(f"<{obs_id},users_connected,\"{row['users_connected']}\">")
#         line_tuples.append(f"<{obs_id},download_speed,\"{row['download_speed']:.6f}\">")
#         line_tuples.append(f"<{obs_id},upload_speed,\"{row['upload_speed']:.6f}\">")
#         line_tuples.append(f"<{obs_id},latency,\"{row['latency']:.6f}\">")
#         line_tuples.append(f"<{obs_id},weather,\"{row['weather']}\">")
#         line_tuples.append(f"<{obs_id},congestion,\"{int(row['congestion'])}\">")
#         line_tuples.append(f"<{obs_id},users_band,\"{row['users_band']}\">")
#         line_tuples.append(f"<{obs_id},latency_band,\"{row['latency_band']}\">")
        
#     lines.append(",".join(line_tuples))

# output_filename = 'Telecom_Tuple_Dataset.txt'
# with open(output_filename, 'w') as f:
#     f.write("\n".join(lines))

# print(f"Generated {output_filename} with {len(lines)} lines.")
# print("\nFirst line preview:")
# print(lines[0][:300] + "...")

import re
import networkx as nx
import matplotlib.pyplot as plt

raw_data = """<1,hasObservation,3438>,<1,tower_id,"1">,<3438,timestamp,"2025-01-29 13:00:00">,<3438,users_connected,"132">,<3438,download_speed,"48.426702">,<3438,upload_speed,"49.267693">,<3438,latency,"56.310808">,<3438,weather,"Clear">,<3438,congestion,"1">,<3438,users_band,"Low">,<3438,latency_band,"Low">,<2,hasObservation,3439>,<2,tower_id,"2">,<3439,timestamp,"2025-01-29 13:00:00">,<3439,users_connected,"768">,<3439,download_speed,"99.514551">,<3439,upload_speed,"43.104751">,<3439,latency,"123.238474">,<3439,weather,"Clear">,<3439,congestion,"0">,<3439,users_band,"High">,<3439,latency_band,"Medium">,<3,hasObservation,3440>,<3,tower_id,"3">,<3440,timestamp,"2025-01-29 13:00:00">,<3440,users_connected,"840">,<3440,download_speed,"38.786129">,<3440,upload_speed,"26.853585">,<3440,latency,"102.822144">,<3440,weather,"Storm">,<3440,congestion,"0">,<3440,users_band,"High">,<3440,latency_band,"Medium">,<4,hasObservation,3441>,<4,tower_id,"4">,<3441,timestamp,"2025-01-29 13:00:00">,<3441,users_connected,"950">,<3441,download_speed,"67.552355">,<3441,upload_speed,"33.112639">,<3441,latency,"134.237229">,<3441,weather,"Snow">,<3441,congestion,"1">,<3441,users_band,"High">,<3441,latency_band,"Medium">,<5,hasObservation,3442>,<5,tower_id,"5">,<3442,timestamp,"2025-01-29 13:00:00">,<3442,users_connected,"64">,<3442,download_speed,"60.859998">,<3442,upload_speed,"35.870321">,<3442,latency,"27.936693">,<3442,weather,"Clear">,<3442,congestion,"0">,<3442,users_band,"Low">,<3442,latency_band,"Low">"""

matches = re.findall(r'<([^>]+)>', raw_data)
triples = []
for m in matches:
    parts = m.split(',')
    if len(parts) == 3:
        triples.append((parts[0].strip(), parts[1].strip(), parts[2].strip()))

G = nx.DiGraph()
for subj, pred, obj in triples:
    obj_clean = obj.strip('"')
    if pred == 'hasObservation':
        G.add_edge(f"Tower {subj}", f"Obs {obj_clean}", relation=pred)
    elif pred == 'tower_id':
        pass
    else:
        obs_node = f"Obs {subj}"
        G.add_node(obs_node)
        G.nodes[obs_node][pred] = obj_clean

plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42, k=1.5)

towers = [n for n in G.nodes if n.startswith("Tower")]
observations = [n for n in G.nodes if n.startswith("Obs")]

nx.draw_networkx_nodes(G, pos, nodelist=towers, node_color='#1f77b4', node_size=3500, node_shape='s')
nx.draw_networkx_nodes(G, pos, nodelist=observations, node_color='#ff7f0e', node_size=5500, node_shape='o')
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='#7f7f7f', width=2, connectionstyle='arc3,rad=0.1')

nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', font_color='white')

obs_labels = {}
for node in observations:
    attrs = G.nodes[node]
    ts = attrs.get('timestamp', '')
    users = attrs.get('users_connected', '')
    speed = attrs.get('download_speed', '')[:5]
    weather = attrs.get('weather', '')
    obs_labels[node] = f"{node}\n{ts}\nUsers: {users}\nSpd: {speed}\nWeather: {weather}"

nx.draw_networkx_labels(G, pos, labels={n: obs_labels[n] for n in observations}, font_size=8)

plt.title("Knowledge Graph: Cellular Tower Observations (2025-01-29 13:00:00)", fontsize=14, fontweight='bold', pad=20)
plt.axis('off')
plt.tight_layout()
plt.savefig('new_tower_knowledge_graph.png')
print("New knowledge graph generated successfully.")