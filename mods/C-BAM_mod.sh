#!/bin/bash

# === CONFIGURATION ===
SOURCE_MODULE="./modules.py"
TARGET_MODULE=".venv/lib/python3.13/site-packages/ultralytics/nn/modules/modules.py"
TASKS_FILE=".venv/lib/python3.13/site-packages/ultralytics/nn/tasks.py"

# === COPY CUSTOM MODULES.PY WITH CBAM ===
if [ ! -f "$SOURCE_MODULE" ]; then
  echo "❌ Source $SOURCE_MODULE not found!"
  exit 1
fi

echo "📦 Backing up original modules.py..."
cp "$TARGET_MODULE" "${TARGET_MODULE}.bak"

echo "📂 Copying modified modules.py to Ultralytics package..."
cp "$SOURCE_MODULE" "$TARGET_MODULE"

# === PATCH TASKS.PY TO IMPORT CBAM IF NOT PRESENT ===
echo "🛠️  Checking if CBAM is already imported in tasks.py..."
if grep -q "CBAM" "$TASKS_FILE"; then
  echo "✅ CBAM already imported."
else
  echo "➕ Adding CBAM import to tasks.py..."

  # Find the last module in the import block and insert after it
  sed -i '' '/from ultralytics.nn.modules import (/{:a;N;/)/!ba;s/)/, CBAM)/}' "$TASKS_FILE"

  echo "✅ CBAM import added successfully."
fi

echo "🚀 All done. You can now use CBAM in your model YAML."