import os
import re
import pandas as pd
import matplotlib.pyplot as plt
# === CONFIGURATION ===
PROCESS = True
#ovs
DATA_DIR = "./data/vm2vm_sw/data/9000/20251108-042653/run1"

#h2h
DATA_DIR = "./data/data/host2host/1500/20251106-030015/run2"
DATA_DIR = "./data/data/host2host/9000/20251106-030015/run0"

## VM 2 VM
DATA_DIR = "./latest/data/9000/20251110-200310/run1"
DATA_DIR = "./latest/data/1500//20251110-200310/run0"

# 50G throughput on both channels

DATA_DIR = "./vm2vm_static/9000/20251111-194850/static/best"
DATA_DIR = "./vm2vm_static/9000/20251111-194850/best"

## VM 2 VM
DATA_DIR = "./vm2vmlatest/9000/20251112-084231/best"
DATA_DIR = "./vm2vmlatest/1500/20251111-203122/best"


DATA_DIR = "./data/data/host2host/1500/20251106-030015/best"
DATA_DIR = "./data/data/host2host/9000/20251106-030015/best"
DATA_DIR = "./vm2vmlatest/9000/20251112-084231/best"


DATA_DIR = "./data/data/host2host/9000/20251106-030015/best"
DATA_DIR = "./vm2vmlatest/9000/20251112-084231/best"


# OVS DPDK
DATA_DIR = "./vf4tests/dpdk/dpdkdata/data/9000/20251121-225208/best"
DATA_DIR = "./vf4tests/dpdk/dpdkdata/data/1500/20251121-225208/best"

# vm2vm
DATA_DIR = "./vf4tests/vf4/host2vm/data/9000/20251119-143713/best"
DATA_DIR = "./vf4tests/vf4/host2vm/data/1500/20251119-f143713/best"

# vm2vm
DATA_DIR = "./vf4tests/vf4/allother/data/9000/20251119-020654/best"
DATA_DIR = "./vf4tests/vf4/allother/data/1500/20251119-020654/best"

# vm2vm2host
PROCESS = False
DATA_DIR = "./vf4tests/vf4/allother/data/9000/20251118-231846/best_static"
DATA_DIR = "./vf4tests/vf4/allother/data/9000/20251118-231846/best"


SAVE_PLOTS = True     # Save plots as PNG files
SHOW_PLOTS = False     # Save plots as PNG files
OUTPUT_DIR = "./images/."

def parse_label(label):
    """
    Extract (number, text).
    If no number is found, use 0.
    """
    nums = re.findall(r"\d+", label)
    num = int(nums[0]) if nums else -1    # numeric part
    txt = re.sub(r"\d+", "", label).strip().lower()  # alphabetical part
    return (num, txt)
    
    
def parse_filename(filename):
    """Extract protocol, bandwidth (XG), and process count (Y) from filename."""
    match = re.match(r"(tcp|udp)_([0-9]+G)_([0-9]+)_.*\.csv", filename)
    if match:
        protocol, bandwidth, processes = match.groups()
        return protocol, bandwidth, int(processes)
    return None


def load_data(directory):
    """Load all CSV files and attach metadata."""
    all_data = []
    for file in os.listdir(directory):
        if not file.endswith(".csv"):
            continue
        parsed = parse_filename(file)
        if not parsed:
            continue

        protocol, bandwidth, processes = parsed
        filepath = os.path.join(directory, file)

        df = pd.read_csv(filepath)
        df["protocol"] = protocol
        df["bandwidth"] = bandwidth
        df["processes"] = processes
        all_data.append(df)

    if not all_data:
        raise ValueError("No valid CSV files found.")

    return pd.concat(all_data, ignore_index=True)


def summarize_throughput(df):
    """Aggregate throughput per protocol, direction, processes, and bandwidth."""
    
    df['throughput_gbps'] = df['throughput_mbps'] / 1000
    df['bandwidth'] = df["bandwidth"].str.rstrip("G").astype(int)
    grouped = (
        df
    )
    return grouped
    
    import matplotlib.pyplot as plt

def plot_total_throughput(df_summary, x_axis="processes", test="default", combined=False):
    if x_axis not in ("processes", "bandwidth"):
        raise ValueError("x_axis must be either 'processes' or 'bandwidth'")
        
    # unique labels
    labels = df_summary["label"].unique()

    # default matplotlib color cycle
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # map each label to a color (wrap if labels > colors)
    label_to_color = {label: colors[i % len(colors)] for i, label in enumerate(labels)}
    
    
    for protocol in sorted(df_summary["protocol"].unique()):
        subset = df_summary[df_summary["protocol"] == protocol]

        directions = sorted(subset["direction"].unique())
        if protocol == "tcp" or combined == True:
            plt.figure(figsize=(8, 5))

        for direction in directions:
            if(direction == "Upload"):
                style = "-"
            else:
                style = "dashed"
                
            sub = subset[subset["direction"] == direction].copy()
            if protocol == "udp" and combined == False:
                plt.figure(figsize=(8, 5))

            title_label = ""
            
            if(combined == False):
                title_label = f"({sub['label'].iloc[0]})"
                
                
            plt.title(f"{title_label} {protocol.upper()} Total Throughput vs {x_axis.capitalize()}")
            plt.xlabel(x_axis.capitalize())
            plt.ylabel("Total Throughput (Gbps)")

            if x_axis == "bandwidth":
                # Pivot by processes and label
                pivot = sub.pivot_table(
                    values="throughput_gbps",
                    index="bandwidth",
                    columns=["processes", "label"],
                    aggfunc="sum"
                ).sort_index()

                # Convert bandwidth to numeric for sorting
                pivot = pivot.sort_index()
                # Plot each combination of processes and label
                for (proc, lbl) in pivot.columns:
                    plt.plot(
                        pivot.index.to_numpy(),
                        pivot[(proc, lbl)].to_numpy(),
                        color = label_to_color[lbl],
                        marker="o",
                        linestyle=style,
                        label=f"{direction.capitalize()} {proc} streams ({lbl})"
                    )
            else:  # x_axis == processes
                # Sort the data by process (x-axis)
                grouped = sub.sort_values(x_axis)
                

                # Plot each bandwidth separately
                for bw, grp in grouped.groupby("bandwidth"):
                    if bw in [0, 1, 2, 4, 5, 8, 10]:
                        plt.plot(
                            grp[x_axis].to_numpy(),
                            grp["throughput_gbps"].to_numpy(),
                            marker="o",
                            linestyle=style,
                            label=f"{bw}G BW {direction}"   # or Gbps, depending on your data
                        )

            plt.grid(True)
            handles, labels = plt.gca().get_legend_handles_labels()

            # Sort by label
            labels, handles = zip(*sorted(zip(labels, handles),
                                          key=lambda x: parse_label(x[0])))

            plt.legend(handles, labels)
            
            
            
            
            plt.tight_layout()

            if protocol == "udp" and combined == False:
                outname = f"{test}_{protocol}_{direction}_throughput_{x_axis}.png"
                plt.savefig(os.path.join(OUTPUT_DIR, outname))
                if(SHOW_PLOTS):
                    plt.show()
                    plt.clf()

        if protocol == "tcp" or combined == True:
            outname = f"{test}_{protocol}_throughput_{x_axis}.png"
            plt.savefig(os.path.join(OUTPUT_DIR, outname))
            if(SHOW_PLOTS):
                plt.show()


def plot_cpu_utilization(df, x_axis="processes"):
    if x_axis not in ("processes", "bandwidth"):
        raise ValueError("x_axis must be either 'processes' or 'bandwidth'")

    for proto in sorted(df["protocol"].unique()):
        subset = df[df["protocol"] == proto]    
        if subset.empty:
            continue

        plt.figure(figsize=(8, 5))
        plt.title(f"{proto.upper()} CPU Utilization vs {x_axis.capitalize()}")
        plt.xlabel(x_axis.capitalize())
        plt.ylabel("CPU Utilization (%)")

        for direction in sorted(subset["direction"].unique()):
            dir_df = subset[subset["direction"] == direction]

            cpu_summary = (
                dir_df.groupby([x_axis], as_index=False)
                .agg(
                    cpu_host_avg=("cpu_host_total", "mean"),
                    cpu_remote_avg=("cpu_remote_total", "mean"),
                )
                .sort_values(x_axis)
            )
           

            plt.plot(cpu_summary[x_axis].to_numpy(), cpu_summary["cpu_host_avg"].to_numpy(), "o-", 
                     label=f"{direction.capitalize()} Host")
            plt.plot(cpu_summary[x_axis].to_numpy(), cpu_summary["cpu_remote_avg"].to_numpy(), "o--", 
                     label=f"{direction.capitalize()} Remote")

        plt.grid(True)
        plt.legend(title=f"{proto.upper()} Direction/Side")
        if SAVE_PLOTS:
            plt.savefig(os.path.join(OUTPUT_DIR, f"{proto}_cpu_utilization_by_{x_axis}.png"))
        
        if(SHOW_PLOTS):
            plt.show()

def plot_jitter_and_loss(df, x_axis="processes", test="default", combined=False):
    """
    Plot jitter (ms) and loss (%) vs number of processes or bandwidth.
    Each bandwidth (or process count) gets its own series, showing all points (no averaging).
    """
    if x_axis not in ("processes", "bandwidth"):
        raise ValueError("x_axis must be either 'processes' or 'bandwidth'")
    
    if x_axis == "processes":
        group_key = "bandwidth"
        x_label = "Processes"
        legend_append ="G"
    else:
        group_key = "processes"
        x_label = "Bandwidth (G)"
        legend_append =""
    
    
    for proto in sorted(df["protocol"].unique()):
        proto_df = df[df["protocol"] == proto]

        if combined:
            plt.figure(figsize=(8, 5))

        for (direction, label), sub in proto_df.groupby(["direction", "label"]):

            if direction == "Upload":   # Keep your filter
                continue

            sub = sub.copy()
            if sub.empty:
                continue

            # Sort by x_axis
            sub = sub.sort_values(x_axis)

            # ---- Determine grouping key based on x_axis ----
            # If x_axis=processes → group by bandwidth
            # If x_axis=bandwidth → group by processes




            # ---- JITTER PLOT ----
            if not combined:
                plt.figure(figsize=(8, 5))
                plt.title(f"({label}) {proto.upper()} Jitter vs {x_axis.capitalize()}")
            else:
                plt.title(f"{proto.upper()} Jitter vs {x_axis.capitalize()}")
                

            plt.xlabel(x_label)
            plt.ylabel("Jitter (ms)")

            for group_value, proc_group in sub.groupby(group_key):
                if combined:
                    label_string = f"{label} ({group_key}={group_value}{legend_append})"
                else:
                    label_string = f"{group_key}={group_value}{legend_append}"
                    
                if group_value in [0, 1, 2, 4, 5, 8, 10]:
                    proc_group = proc_group.sort_values(x_axis)

                    plt.plot(
                        proc_group[x_axis].to_numpy(),
                        proc_group["jitter_ms"].to_numpy(),
                        "o-",
                        label=label_string
                    )

            plt.grid(True)
            
            handles, labels = plt.gca().get_legend_handles_labels()

            # Sort by label
            
            labels, handles = zip(*sorted(zip(labels, handles),
                                          key=lambda x: parse_label(x[0])))

            plt.legend(handles, labels)
            plt.tight_layout()

            if SAVE_PLOTS:
                outname = f"{test}_{proto}_{direction}_{label}_jitter_by_{x_axis}.png"
                plt.savefig(os.path.join(OUTPUT_DIR, outname))

            if not combined:
                if(SHOW_PLOTS):
                    plt.show()
                    plt.clf()

        if combined:
            if(SHOW_PLOTS):
                plt.show()



        # ========== LOSS PLOTS ==========

        for proto in sorted(df["protocol"].unique()):
            proto_df = df[df["protocol"] == proto]

            if combined:
                plt.figure(figsize=(8, 5))

            for (direction, label), sub in proto_df.groupby(["direction", "label"]):

                sub = sub.copy()
                if sub.empty:
                    continue

                # Sort by x_axis
                sub = sub.sort_values(x_axis)


                # ---- LOSS PLOT ----
                if not combined:
                    plt.figure(figsize=(8, 5))
                    plt.title(f"({label}) {proto.upper()} Loss % vs {x_axis.capitalize()}")
                else:
                    plt.title(f"{proto.upper()} Loss % vs {x_axis.capitalize()}")
                    
                plt.xlabel(x_label)
                plt.ylabel("Loss (%)")

                for group_value, proc_group in sub.groupby(group_key):
                    if group_value in [0, 1, 2, 4, 5, 8, 10]:
                        if combined:
                            label_string = f"{label} ({group_key}={group_value}{legend_append})"
                        else:
                            label_string = f"{group_key}={group_value}{legend_append}"
                            
                        proc_group = proc_group.sort_values(x_axis)

                        plt.plot(
                            proc_group[x_axis].to_numpy(),
                            proc_group["loss_percent"].to_numpy(),
                            "o-",
                            label=label_string
                        )

                plt.grid(True)
                
                handles, labels = plt.gca().get_legend_handles_labels()

                # Sort by label
                labels, handles = zip(*sorted(zip(labels, handles),
                                              key=lambda x: parse_label(x[0])))

                plt.legend(handles, labels)
                plt.tight_layout()

                if SAVE_PLOTS:
                    outname = f"{test}_{proto}_{direction}_{label}_loss_by_{x_axis}.png"
                    plt.savefig(os.path.join(OUTPUT_DIR, outname))



                if not combined:
                    if(SHOW_PLOTS):
                        plt.show()
                    plt.clf()

            if combined:
                if(SHOW_PLOTS):
                    plt.show()
                    plt.clf()
                    plt.clf()

               
            
def main():

    # vm2vm2host
    print("vm2vm2host")
    PROCESS = False
    DATA_DIR = "./127_data/vm2vm2host/9000/20251208-153853/best"
    DATA_DIR = "./127_data/vm2vm2host_reverse/9000/20251208-161615/best"
    # DATA_DIR = "./vf4tests/vf4/allother/data/9000/20251118-231846/best"

    df = load_data(DATA_DIR)
    df["label"] = "vm2vm"
    
    
    
    DATA_DIR = "./127_data/vm2vm2host/9000/20251208-153853/best_static"
    DATA_DIR = "./127_data/vm2vm2host_reverse/9000/20251208-161615/best_static"
    # DATA_DIR = "./vf4tests/vf4/allother/data/9000/20251118-231846/best_static"
    df2 = load_data(DATA_DIR)
    df2["label"] = "vm2host"
    combined = pd.concat([df, df2], ignore_index=True)
    print(combined)
    

    df_summary = summarize_throughput(combined)
    plot_total_throughput(df_summary, x_axis="bandwidth", test="vm2vm2host", combined=True)
    plot_cpu_utilization(df, x_axis="bandwidth")
    plot_jitter_and_loss(df_summary, x_axis="bandwidth", test="vm2vm2host", combined=True)
    
    
    print("ovs dpdk")
    DATA_DIR = "./ovsdpdk/9000/20251205-104319/best"
    # DATA_DIR = "./vf4tests/dpdk/dpdkdata/data/9000/20251121-225208/best"
    df = load_data(DATA_DIR)
    df["label"] = "ovs dpdk"
    df_summary = summarize_throughput(df)
    plot_total_throughput(df_summary, x_axis="processes", test="ovsdpdk9000")
    plot_cpu_utilization(df, x_axis="processes")
    plot_jitter_and_loss(df_summary, x_axis="processes", test="ovsdpdk9000")
    
    
    
    # vm2vm
    print("vm2host")
    DATA_DIR = "./vf4tests/vf4/host2vm/data/9000/20251119-143713/best"
    # DATA_DIR = "./vf4tests/dpdk/dpdkdata/data/1500/20251121-225208/best"
    df = load_data(DATA_DIR)
    df["label"] = "vm2host"
    df_summary = summarize_throughput(df)
    plot_total_throughput(df_summary, x_axis="processes", test="vm2host9000")
    plot_cpu_utilization(df, x_axis="processes")
    plot_jitter_and_loss(df_summary, x_axis="processes", test="vm2host9000")
    
    DATA_DIR = "./vf4tests/vf4/host2vm/data/1500/20251119-143713/best"
    df = load_data(DATA_DIR)
    df["label"] = "vm2host"
    df_summary = summarize_throughput(df)
    plot_total_throughput(df_summary, x_axis="processes", test="vm2host1500")
    plot_cpu_utilization(df, x_axis="processes")
    plot_jitter_and_loss(df_summary, x_axis="processes", test="vm2host1500")
    

    # vm2vm
    print("vm2vm")
    #DATA_DIR = "./vf4tests/vf4/allother/data/9000/20251119-020654/best"
    DATA_DIR = "./127_data/vm2vm/9000/20251207-005241/best"
    df = load_data(DATA_DIR)
    df["label"] = "vm2vm"
    df_summary = summarize_throughput(df)
    plot_total_throughput(df_summary, x_axis="processes", test="vm2vm9000")
    plot_cpu_utilization(df, x_axis="processes")
    plot_jitter_and_loss(df_summary, x_axis="processes", test="vm2vm9000")
    
    
    # DATA_DIR = "./vf4tests/vf4/allother/data/1500/20251119-020654/best"

    # df = load_data(DATA_DIR)
    # df["label"] = "vm2vm"
    
    # df_summary = summarize_throughput(df)
    # plot_total_throughput(df_summary, x_axis="processes", test="vm2vm1500")
    # plot_cpu_utilization(df, x_axis="processes")
    # plot_jitter_and_loss(df_summary, x_axis="processes", test="vm2vm1500")
    


if __name__ == "__main__":
    main()