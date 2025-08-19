#!/usr/bin/env python3
"""
MARROWS - Main inference entry point

This script is for running inference on new medical images using your trained model.
For training, use the notebooks in the notebooks/training/ directory.

Usage:
    python main.py --model models/final/best_model.pt --source path/to/images
"""

import argparse
from pathlib import Path
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description='MARROWS Medical Image Inference')
    parser.add_argument('--model', type=str, required=True, 
                      help='Path to trained model file (.pt)')
    parser.add_argument('--source', type=str, required=True,
                      help='Path to image or directory of images')
    parser.add_argument('--output', type=str, default='results/inference',
                      help='Output directory for results')
    parser.add_argument('--conf', type=float, default=0.5,
                      help='Confidence threshold')
    
    args = parser.parse_args()
    
    # Check if model exists
    model_path = Path(args.model)
    if not model_path.exists():
        print(f"❌ Model not found: {model_path}")
        print("💡 Train a model first using notebooks/training/02_train_yolo.ipynb")
        return
    
    # Load model
    print(f"🤖 Loading model: {model_path}")
    model = YOLO(str(model_path))
    
    # Run inference
    print(f"🔍 Running inference on: {args.source}")
    results = model(args.source, conf=args.conf, save=True, project=args.output)
    
    print(f"✅ Results saved to: {args.output}")
    print(f"📊 Processed {len(results)} images")

if __name__ == "__main__":
    main()
