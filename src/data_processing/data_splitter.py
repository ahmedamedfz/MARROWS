import os
import shutil
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import yaml

# Paths
RAW_IMAGE_DIR = Path("data/BulkAnnotated/images")
RAW_LABEL_DIR = Path("data/BulkAnnotated/labels")
DEST_DIR = Path("data")
SPLIT_DIR = DEST_DIR / "BulkSplitData"

# Create necessary dirs
def make_dirs(base_dir):
    (base_dir / "images").mkdir(parents=True, exist_ok=True)
    (base_dir / "labels").mkdir(parents=True, exist_ok=True)

# Feature extraction: object count and average area
def extract_features():
    features = []
    image_paths = []
    
    for label_file in RAW_LABEL_DIR.glob("*.txt"):
        with open(label_file, 'r') as f:
            lines = f.readlines()
        
        count = len(lines)
        total_area = 0
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            _, xc, yc, w, h = map(float, parts)
            total_area += w * h  # YOLO coords are normalized

        avg_area = total_area / count if count > 0 else 0
        features.append([count, avg_area])
        image_paths.append(label_file.stem + ".jpg")
    
    return np.array(features), image_paths

# Clustering into Sparse, Normal, Dense
def cluster_and_copy(features, image_paths):
    kmeans = KMeans(n_clusters=3, random_state=42)
    labels = kmeans.fit_predict(features)

    # Map clusters to folder names based on count
    cluster_avg_counts = [np.mean(features[labels == i][:, 0]) for i in range(3)]
    order = np.argsort(cluster_avg_counts)
    cluster_map = {order[0]: 'SparseData', order[1]: 'NormalData', order[2]: 'DenseData'}

    for i, img_name in enumerate(image_paths):
        cluster_folder = DEST_DIR / cluster_map[labels[i]]
        make_dirs(cluster_folder)
        img_src = RAW_IMAGE_DIR / img_name
        label_src = RAW_LABEL_DIR / (img_name.replace('.jpg', '.txt'))

        shutil.copy(img_src, cluster_folder / "images" / img_name)
        shutil.copy(label_src, cluster_folder / "labels" / (img_name.replace('.jpg', '.txt')))

    return cluster_map

# Split data into 80% train, 20% val
def split_bulk_data():
    image_files = list(RAW_IMAGE_DIR.glob("*.jpg"))
    train_files, val_files = train_test_split(image_files, test_size=0.2, random_state=42)

    for split, files in zip(['train', 'val'], [train_files, val_files]):
        for file in files:
            dest_img_dir = SPLIT_DIR / "images" / split
            dest_lbl_dir = SPLIT_DIR / "labels" / split
            dest_img_dir.mkdir(parents=True, exist_ok=True)
            dest_lbl_dir.mkdir(parents=True, exist_ok=True)

            shutil.copy(file, dest_img_dir / file.name)
            label_file = RAW_LABEL_DIR / file.with_suffix('.txt').name
            shutil.copy(label_file, dest_lbl_dir / label_file.name)

# Save bone_marrow.yaml for a split dataset
def generate_yaml(folder_path, nc, names):
    yaml_content = {
        'path': '.',
        'train': 'images/train',
        'val': 'images/val',
        'nc': nc,
        'names': names
    }
    yaml_path = folder_path / "bone_marrow.yaml"
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_content, f, default_flow_style=False)

# Load base YAML and write new ones
def generate_all_yamls():
    # Read from original YAML
    base_yaml = Path("data/BulkRawData/bone_marrow.yaml")
    with open(base_yaml, 'r') as f:
        config = yaml.safe_load(f)

    nc = config['nc']
    names = config['names']

    for folder in ['SparseData', 'NormalData', 'DenseData', 'BulkSplitData']:
        generate_yaml(DEST_DIR / folder, nc, names)

if __name__ == "__main__":
    features, img_paths = extract_features()
    cluster_map = cluster_and_copy(features, img_paths)
    split_bulk_data()
    generate_all_yamls()
    print("✅ Done. Data clustered and split successfully.")


