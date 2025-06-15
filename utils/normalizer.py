from typing import Literal, Union
import cv2
import numpy as np
import os
from pathlib import Path
from python_color_transfer.color_transfer import ColorTransfer

# Base directory = root of the Git repo or project
PROJECT_ROOT = Path.cwd().parent

TransferMethod = Literal["pdf", "mean_std", "lab"]

def image_stats(image):
    """Calculate the mean and std for each LAB channel."""
    l, a, b = cv2.split(image)
    return (
        l.mean(), l.std(),
        a.mean(), a.std(),
        b.mean(), b.std()
    )

def color_transfer(
    source: Union[Path, np.ndarray],
    target: Union[Path, np.ndarray],
    transfer_method: TransferMethod = "lab",
    if_test: bool = False
) -> np.ndarray:
    """
    Apply color transfer from source to target using selected method.
    
    Args:
        source (np.ndarray): Source image (BGR).
        target (np.ndarray): Target image (BGR).
        transfer_method (str): One of "pdf", "mean_std", or "lab".

    Returns:
        np.ndarray: Color-transferred image (BGR).
    """

    if if_test:
        source_rgb = cv2.imread(source) if isinstance(source, str) else source
        target_rgb = cv2.imread(target) if isinstance(target, str) else target
    else:
        source_rgb = source
        target_rgb = target

    PT = ColorTransfer()

    if transfer_method == "pdf":
        transferred = PT.pdf_transfer(img_arr_in=target_rgb,
                                      img_arr_ref=source_rgb,
                                      regrain=True)
    elif transfer_method == "mean_std":
        transferred = PT.mean_std_transfer(img_arr_in=target_rgb,
                                           img_arr_ref=source_rgb)
    elif transfer_method == "lab":
        transferred = PT.lab_transfer(img_arr_in=target_rgb,
                                      img_arr_ref=source_rgb)
    else:
        raise ValueError(f"Unsupported transfer method: {transfer_method}")
    
    return transferred

def resolve_path(path):
    """Resolves path relative to project root, if not absolute."""
    p = Path(path)
    return p if p.is_absolute() else (PROJECT_ROOT / p).resolve()

def batch_color_transfer(path_of_reference_image, samples_folder, output_folder, transfer_method: TransferMethod = "pdf"):
    path_of_reference_image = resolve_path(path_of_reference_image)
    samples_folder = resolve_path(samples_folder)
    output_folder = resolve_path(output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    source = cv2.imread(str(path_of_reference_image))
    if source is None:
        raise ValueError("Sample image could not be loaded.")

    for filename in os.listdir(samples_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            target_path = os.path.join(samples_folder, filename)
            output_path = os.path.join(output_folder, filename)

            target = cv2.imread(target_path)
            if target is None:
                print(f"Skipping unreadable file: {filename}")
                continue

            transferred = color_transfer(source, target, transfer_method=transfer_method)
            if isinstance(transferred, np.ndarray):
                cv2.imwrite(output_path, transferred)
                print(f"Saved recolored image to: {output_path}")
            else:
                print(f"Skipping file due to invalid transfer result: {filename}")