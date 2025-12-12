import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.cm as cm

root = Path("127_data/vm2vm/")
processes = [1, 4, 8, 16]

# ==========================================================
# 1. Build df_plot (ratio = bps / MTU)
# ==========================================================
rows = []

for mtu_dir in sorted(root.iterdir()):
    if not mtu_dir.is_dir():
        continue

    try:
        mtu = int(mtu_dir.name)  # directory name is MTU
    except ValueError:
        continue

    date_dir = next(mtu_dir.iterdir())
    best_dir = date_dir / "best"

    for p in processes:
        f = best_dir / f"udp_10G_{p}_avg.csv"
        if not f.exists():
            continue

        df = pd.read_csv(f)
        upload_row = df.loc[df["direction"] == "Download"]
        if upload_row.empty:
            continue

        bps = upload_row["bits_per_second"].iloc[0]
        ratio = bps / mtu

        rows.append({"mtu": mtu, "P": p, "ratio": ratio})

df_plot = pd.DataFrame(rows)

# ==========================================================
# 2. Build df_mbps (Mbps per P per MTU)
# ==========================================================
mbps_rows = []

for mtu_dir in sorted(root.iterdir()):
    if not mtu_dir.is_dir():
        continue

    try:
        mtu = int(mtu_dir.name)
    except ValueError:
        continue

    date_dir = next(mtu_dir.iterdir())
    best_dir = date_dir / "best"

    for p in processes:
        f = best_dir / f"udp_10G_{p}_avg.csv"
        if not f.exists():
            continue

        df_m = pd.read_csv(f)
        upload_row = df_m.loc[df_m["direction"] == "Upload"]
        if upload_row.empty:
            continue

        mbps = upload_row["throughput_mbps"].iloc[0]

        mbps_rows.append({"mtu": mtu, "P": p, "mbps": mbps})

df_mbps = pd.DataFrame(mbps_rows)

# ==========================================================
# 3. Grouped bars + line per P
# ==========================================================
mtus = sorted(df_plot["mtu"].unique())
processes = sorted(df_plot["P"].unique())
x = np.arange(len(mtus))

# nice distinct colors
cmap = cm.get_cmap("tab10")
colors = {p: cmap(i) for i, p in enumerate(processes)}

# bar width so groups fit nicely
width = 0.8 / len(processes)

fig, ax1 = plt.subplots(figsize=(12, 6))
# -------- Grouped bars: ratio per P (slightly transparent) --------
for i, p in enumerate(processes):
    ratios = (
        df_plot[df_plot["P"] == p]
        .set_index("mtu")["ratio"]
        .reindex(mtus)
    )

    ax1.bar(
        x + (i - (len(processes) - 1) / 2) * width,
        ratios.to_numpy(),
        width=width,
        color=colors[p],
        edgecolor="black",
        linewidth=0.8,
        alpha=0.65,        # <<< slight transparency
        label=f"P={p}",
    )
ax1.set_xticks(x)
ax1.set_xticklabels(mtus)
ax1.set_xlabel("MTU (bytes)")
ax1.set_ylabel("PPS")

# -------- Lines: Mbps per P (with black outline) --------
ax2 = ax1.twinx()
ax2.set_ylabel("Throughput (Mbps)")

for p in processes:
    mbps_series = (
        df_mbps[df_mbps["P"] == p]
        .set_index("mtu")["mbps"]
        .reindex(mtus)
    )

    y = mbps_series.to_numpy()
    if np.isnan(y).all():
        continue

    # 1) Black outline (thicker)
    ax2.plot(
        x,
        y,
        color="black",
        linewidth=4,
        alpha=0.9,
        zorder=5,
    )

    # 2) Colored line on top
    ax2.plot(
        x,
        y,
        color=colors[p],
        marker="o",
        linewidth=2,
        zorder=6,
        label=f"P={p} Mbps",
    )
# -------- Combined legend --------
bars_h, bars_l = ax1.get_legend_handles_labels()
line_h, line_l = ax2.get_legend_handles_labels()
ax1.legend(bars_h + line_h, bars_l + line_l, loc="upper left")

plt.tight_layout()
plt.show()
