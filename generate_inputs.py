import os
import random
import pandas as pd

def build_graph_database_and_logs(kaggle_csv_path="telecom_network_data.csv", num_graphs=400, num_queries=150):
    print("--- Step 1: Processing Real-World Telecom Entities (Kaggle Data Source) ---")
    
    towers = []
    if os.path.exists(kaggle_csv_path):
        # Example of loading real entities from a Kaggle CSV file
        df = pd.read_csv(kaggle_csv_path)
        # Assuming the CSV contains a column like 'tower_id'
        if 'tower_id' in df.columns:
            towers = df['tower_id'].unique().tolist()
            print(f"Loaded {len(towers)} unique telecom towers from Kaggle CSV.")
    
    # Fallback if Kaggle file isn't downloaded locally yet
    if not towers:
        print("Kaggle CSV not found locally. Initializing standard telecom tower pool synthetically...")
        towers = [f"LTE_Tower_{i:03d}" for i in range(1, 150)]

    print(f"--- Step 2: Generating Database.txt (Graph Database D) ---")
    # Each line represents an individual network graph database item: Graph_ID : Edges
    with open("Database.txt", "w") as f_db:
        for i in range(1, num_graphs + 1):
            graph_id = f"Region_Graph_{i}"
            # Randomly select a sub-mesh of connected towers for this graph entry
            num_edges = random.randint(3, 9)
            edges = set()
            for _ in range(num_edges):
                src, dst = random.sample(towers, 2)
                if src != dst:
                    edges.add(f"{src},{dst}")
            
            # Fallback safeguard
            if not edges:
                edges.add(f"{towers[0]},{towers[1]}")
                
            f_db.write(f"{graph_id}:{';'.join(edges)}\n")
            
    print(f"Successfully generated Database.txt with {num_graphs} regional graphs.")

    print(f"--- Step 3: Generating QLog.txt (Query Log Q) ---")
    # Each line represents a query log workload item evaluating path/subgraph presence
    with open("QLog.txt", "w") as f_q:
        for j in range(1, num_queries + 1):
            query_id = f"Q{j}"
            # Queries target patterns or connectivity checks between towers
            src, dst = random.sample(towers, 2)
            f_q.write(f"{query_id}:PATH_CHECK:{src}->{dst}\n")
            
    print(f"Successfully generated QLog.txt with {num_queries} query workloads.")

if __name__ == "__main__":
    # Point this to your downloaded Kaggle dataset filename if available
    build_graph_database_and_logs("telecom_network_data.csv", num_graphs=500, num_queries=200)