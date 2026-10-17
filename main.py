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

