# modules.py - versi modifikasi dengan CBAM
import torch
import torch.nn as nn
import torch.nn.functional as F

# ====================
# CBAM Implementation
# ====================

class ChannelAttention(nn.Module):
    def __init__(self, in_planes, ratio=16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)

        self.fc = nn.Sequential(
            nn.Conv2d(in_planes, in_planes // ratio, 1, bias=False),
            nn.ReLU(),
            nn.Conv2d(in_planes // ratio, in_planes, 1, bias=False)
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg = self.fc(self.avg_pool(x))
        max = self.fc(self.max_pool(x))
        out = avg + max
        return self.sigmoid(out)

class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        padding = kernel_size // 2
        self.conv = nn.Conv2d(2, 1, kernel_size, padding=padding, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg = torch.mean(x, dim=1, keepdim=True)
        max, _ = torch.max(x, dim=1, keepdim=True)
        concat = torch.cat([avg, max], dim=1)
        return self.sigmoid(self.conv(concat))

class CBAM(nn.Module):
    def __init__(self, in_planes, ratio=16, kernel_size=7):
        super(CBAM, self).__init__()
        self.channel = ChannelAttention(in_planes, ratio)
        self.spatial = SpatialAttention(kernel_size)

    def forward(self, x):
        x = self.channel(x) * x
        x = self.spatial(x) * x
        return x

# ==========================
# Tempat kamu bisa menambahkan
# CBAM ke dalam YOLOv8 model
# ==========================
# Misalnya kamu akan pakai CBAM di backbone:
#
# backbone:
#   - [-1, 1, Conv, [64, 3, 2]]
#   - [-1, 1, CBAM, [64]]  ← ini akan berhasil setelah kamu load model ini

# ============================================
# Modul CBAM harus juga diregister ke YOLOv8
# ============================================

# Tambahkan CBAM ke bagian 'ultralytics/nn/tasks.py' atau model parser kamu:
# from ultralytics.nn.modules import CBAM

# ============================================
# Di bawah ini biarkan kosong atau tambahkan
# definisi layer YOLOv8 lain jika ingin kustom
# ============================================

# EOF