#!/bin/bash

# Name of the virtual environment directory
VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"
PYTHON_BIN="python3.10"

# List of required packages
REQUIREMENTS=$(cat <<EOF
torch
torchvision
torchaudio
ipykernel
scikit-learn
python-color-transfer
ultralytics>=8.0.0
opencv-python
EOF
)

# Step 0: Create requirements.txt if it doesn't exist
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "Creating $REQUIREMENTS_FILE..."
    echo "$REQUIREMENTS" > $REQUIREMENTS_FILE
else
    echo "$REQUIREMENTS_FILE already exists. Skipping creation."
fi

# Step 1: Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR using $PYTHON_BIN..."
    $PYTHON_BIN -m venv $VENV_DIR
    echo "Virtual environment created."
else
    echo "Virtual environment already exists at $VENV_DIR"
fi

# Step 2: Activate the environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Step 3: Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Step 4: Install from requirements.txt
echo "Installing packages from $REQUIREMENTS_FILE..."
pip install -r $REQUIREMENTS_FILE

# Step 5: Done
echo "✅ Environment setup complete."
echo "Python path: $(which python)"
echo "Python version: $(python --version)"