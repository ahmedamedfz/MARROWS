import os
import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import yaml

def count_boxes_in_folder(label_folder):
    total = 0
    for filename in os.listdir(label_folder):
        if filename.endswith(".txt"):
            path = os.path.join(label_folder, filename)
            with open(path, 'r') as f:
                total += len([line for line in f if line.strip()])
    return total

def compare_annotation_vs_prediction(gt_label_folder, pred_label_folder, output_img_path="loss_ratio_plot.png"):
    # Hitung total box
    total_gt = count_boxes_in_folder(gt_label_folder)
    total_pred = count_boxes_in_folder(pred_label_folder)

    # Hitung selisih
    diff = total_pred - total_gt
    status = "Overpredicted" if diff > 0 else "Underpredicted"

    # Plot
    fig, ax = plt.subplots()
    ax.bar(["Ground Truth", "Prediction"], [total_gt, total_pred], color=["blue", "gray"])
    ax.set_title(f"Prediction vs Annotation Box Count\n({status} by {abs(diff)} boxes)")
    ax.set_ylabel("Number of Boxes")

    # Tambahkan label angka
    for i, val in enumerate([total_gt, total_pred]):
        ax.text(i, val + max(total_gt, total_pred)*0.02, str(val), ha='center', va='bottom', fontsize=12)

    plt.tight_layout()
    plt.savefig(output_img_path)
    plt.close()
    
    return output_img_path

def load_class_names(yaml_path):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    return list(data['names'].values()) if isinstance(data['names'], dict) else data['names']

def collect_auc_data(gt_folder, pred_folder, class_names):
    auc_table = []
    roc_curves = []
    all_y_true = []
    all_y_score = []

    for class_id, class_name in enumerate(class_names):
        y_true = []
        y_score = []

        for fname in os.listdir(gt_folder):
            if not fname.endswith(".txt"):
                continue
            gt_file = os.path.join(gt_folder, fname)
            pred_file = os.path.join(pred_folder, fname)

            with open(gt_file, 'r') as f:
                gt_classes = [int(float(line.strip().split()[0])) for line in f]
            is_present = int(class_id in gt_classes)
            y_true.append(is_present)

            conf = 0.0
            if os.path.exists(pred_file):
                with open(pred_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 6 and int(float(parts[0])) == class_id:
                            conf = max(conf, float(parts[5]))
            y_score.append(conf)

        if len(set(y_true)) < 2:
            auc = 0.0
            print(f"⚠️ Class {class_name}: hanya satu jenis label, AUC di-set ke 0.")
        else:
            auc = roc_auc_score(y_true, y_score)
            fpr, tpr, _ = roc_curve(y_true, y_score)
            roc_curves.append((fpr, tpr, class_name, auc))

        all_y_true.extend(y_true)
        all_y_score.extend(y_score)
        auc_table.append((class_name, auc))

    # Macro average
    if len(set(all_y_true)) >= 2:
        macro_auc = roc_auc_score(all_y_true, all_y_score)
        fpr_macro, tpr_macro, _ = roc_curve(all_y_true, all_y_score)
        roc_curves.append((fpr_macro, tpr_macro, "Macro Avg", macro_auc))
        auc_table.append(("Macro Avg", macro_auc))

    return auc_table, roc_curves

def plot_roc_curves_with_table(roc_curves, auc_table, title="Multi-Class ROC AUC", save_path=None):
    plt.figure(figsize=(6.5, 6.5))
    for fpr, tpr, class_name, auc in roc_curves:
        if class_name == "Macro Avg":
            plt.plot(fpr, tpr, linestyle='--', linewidth=2, color='black', label=f"{class_name} (AUC: {auc:.2f})")
        else:
            plt.plot(fpr, tpr, label=f"{class_name} (AUC: {auc:.2f})")

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(title)
    plt.grid(True)

    drawn_labels = [rc[2] for rc in roc_curves]
    for class_name, auc in auc_table:
        if class_name not in drawn_labels:
            plt.plot([], [], ' ', label=f"{class_name} (AUC: {auc:.2f})")

    plt.legend(loc='lower right', fontsize=9)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"✅ ROC AUC plot saved to: {save_path}")
    plt.show()

def run_roc_analysis(yaml_path, gt_folder, pred_folder, subset_name, selection="best"):
    class_names = load_class_names(yaml_path)
    auc_table, roc_curves = collect_auc_data(gt_folder, pred_folder, class_names)

    print(f"\n📋 ROC AUC Values ({subset_name}):")
    for class_name, auc in auc_table:
        print(f"{class_name:<12}: {auc:.4f}")

    save_path = f"{selection}_roc_auc_{subset_name.lower()}.png"
    plot_roc_curves_with_table(
        roc_curves, auc_table,
        title="Multi-Class ROC AUC",
        save_path=save_path
    )