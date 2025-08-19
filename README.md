# MARROWS - Medical AI Recognition and Results Optimization With YOLO System

A user-friendly YOLO training system designed for medical professionals to train bone marrow detection models.

## 🩺 For Medical Professionals

This project helps you train AI models to detect bone marrow structures in medical images. **No programming experience required** - just follow the step-by-step notebooks!

## 📁 Project Structure

```
MARROWS/
├── 📊 data/                    # Your medical datasets
├── 📝 notebooks/              # Step-by-step training guides
├── 🤖 models/                 # Trained AI models
├── 📈 results/                # Training results and reports
├── ⚙️  env/                   # Installation files
└── 📚 docs/                   # Additional documentation
```

## 🚀 Quick Start Guide

### Step 1: Install Environment
```bash
# Option 1: Using conda (recommended)
cd env/
conda env create -f environment.yml
conda activate yolov8-bone

# Option 2: Using pip
pip install -r env/requirements.txt
```

### Step 2: Prepare Your Data
1. Place your medical images in `data/raw/your_dataset_name/`
2. Ensure annotations are in YOLO format
3. Run: `notebooks/training/01_data_preparation.ipynb`

### Step 3: Train Your Model
1. Open: `notebooks/training/02_train_yolo.ipynb`
2. Follow the cells step by step
3. **Just press Shift+Enter for each cell** - no coding needed!

### Step 4: Evaluate Results
1. Open: `notebooks/training/03_evaluate_model.ipynb`
2. View your model's performance metrics
3. Check `results/evaluation_reports/` for detailed reports

## 📋 Training Workflow (No Coding Required!)

### For Standard Training:
1. **Data Preparation** → `notebooks/training/01_data_preparation.ipynb`
2. **Model Training** → `notebooks/training/02_train_yolo.ipynb`
3. **Evaluation** → `notebooks/training/03_evaluate_model.ipynb`

### For Advanced Users:
- **Hyperparameter Tuning** → `notebooks/experiments/hyperparameter_tuning.ipynb`
- **Model Comparison** → `notebooks/experiments/model_comparison.ipynb`
- **Data Analysis** → `notebooks/analysis/data_exploration.ipynb`

## 📍 Where to Find Your Results

After training, your outputs will be in these locations:

| What You're Looking For | Location | Description |
|------------------------|----------|-------------|
| **Trained Model** | `models/final/best_model.pt` | Use this file for detection |
| **Training Metrics** | `results/training_logs/` | Loss curves, accuracy graphs |
| **Performance Report** | `results/evaluation_reports/` | How well your model performs |
| **Training History** | `results/hyperparameter_studies/` | All experiment records |

## 🔄 Handing Off to Backend Team

### For Backend Integration:

1. **Model File**: Send `models/final/best_model.pt`
2. **Config File**: Include `configs/model_configs/yolov11_cbam.yaml`
3. **Performance Report**: Share `results/evaluation_reports/model_performance.html`

### Example Integration Code:
```python
from ultralytics import YOLO

# Load your trained model
model = YOLO('models/final/best_model.pt')

# Run inference
results = model('path/to/new_image.jpg')

# Get detections
for result in results:
    boxes = result.boxes.xyxy  # Bounding box coordinates
    scores = result.boxes.conf  # Confidence scores
    classes = result.boxes.cls  # Class IDs
```

## ⚠️ Troubleshooting

### Common Issues:

**"CUDA out of memory"**
- Solution: Reduce batch size in training notebook
- Look for: `batch_size = 16` → change to `batch_size = 8`

**"No training data found"**
- Check: `data/annotations/data.yaml` exists
- Ensure: Images are in `data/annotations/train/images/`
- Ensure: Labels are in `data/annotations/train/labels/`

**"Model not converging"**
- Try: Different learning rates in `notebooks/experiments/hyperparameter_tuning.ipynb`
- Check: Data quality in `notebooks/analysis/data_exploration.ipynb`

### Getting Help:
1. Check `docs/troubleshooting.md`
2. Review training logs in `results/training_logs/`
3. Contact the development team with your `results/` folder

## 📊 Data Requirements

### Image Format:
- **Supported**: `.jpg`, `.jpeg`, `.png`
- **Resolution**: Minimum 640x640 recommended
- **Quality**: High resolution medical images preferred

### Annotation Format:
- **YOLO format**: `class_id x_center y_center width height`
- **Normalized coordinates**: All values between 0 and 1
- **File structure**:
  ```
  data/annotations/
  ├── train/
  │   ├── images/
  │   └── labels/
  ├── val/
  │   ├── images/
  │   └── labels/
  └── data.yaml
  ```

## 🎯 Best Practices

### For Medical Data:
1. **Anonymize** patient data before training
2. **Balance** your dataset across different conditions
3. **Validate** annotations with medical experts
4. **Document** your data sources and preprocessing steps

### For Training:
1. **Start small** - use a subset for initial experiments
2. **Monitor** training progress in real-time
3. **Save checkpoints** regularly
4. **Test thoroughly** before deployment

## 📞 Support

- **Documentation**: Check `docs/` folder
- **Issues**: Create GitHub issues with error screenshots
- **Data Questions**: Contact medical imaging team
- **Technical Issues**: Contact AI development team

---

> **Note for Doctors**: You don't need to understand the technical details. Just follow the notebooks step by step, and the system will guide you through the process! 🩺✨
