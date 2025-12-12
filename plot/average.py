import os
import pandas as pd
import re
import argparse

DIR = "./vm2vmlatest/9000/20251112-084231/"
DEST = "best"
FILTER = r"run[0-9](?!_static)"
def parse_filename(filename):
    """
    Extract protocol, bandwidth, and process count from filenames like:
    tcp_10G_5_random.csv
    Returns (protocol, bandwidth, processes)
    """
    match = re.match(r"(tcp|udp)_([0-9]+G)_([0-9]+)_.*\.csv$", filename, re.IGNORECASE)
    if match:
        return match.group(1).lower(), match.group(2), match.group(3)
    return None


def collect_run_dirs():
    """Return sorted list of run directories (run0, run1, …)."""
    return sorted(
        d for d in os.listdir(DIR)
        if re.match(FILTER, d) and os.path.isdir(os.path.join(DIR, d))
    )


def main():
    run_dirs = collect_run_dirs()
    print(run_dirs)
    if not run_dirs:
        print("No run directories found.")
        return

    # Map of (proto, bw, proc) → list of CSV paths
    file_map = {}

    for run in run_dirs:
        run_path = os.path.join(DIR, run)
        for filename in os.listdir(run_path):
            if not filename.endswith(".csv"):
                continue

            parsed = parse_filename(filename)
            if not parsed:
                continue

            key = parsed  # (proto, bw, proc)
            file_map.setdefault(key, []).append(os.path.join(run_path, filename))

    best_dir = os.path.join(DIR, DEST)
    os.makedirs(best_dir, exist_ok=True)

    for (proto, bw, proc), paths in sorted(file_map.items()):
        dfs = []
        for path in paths:
            try:
                df = pd.read_csv(path)
                
                # Add a new column that stores the proto, bw, and proc values
                df['proto_bw_proc'] = f"{proto}_{bw}_{proc}"
                
                dfs.append(df)
            except Exception as e:
                print(f"[!] Failed to read {path}: {e}")

        if not dfs:
            print(f"[!] No valid data for {proto}_{bw}_{proc}")
            continue

        # Combine all DataFrames for the current proto, bw, proc
        combined = pd.concat(dfs, ignore_index=True)

        # Ensure 'direction' column exists
        if "direction" not in combined.columns:
            print(f"[!] Skipping {proto}_{bw}_{proc}: no 'direction' column found")
            continue

        result_rows = []
        
        # Optional: print the combined DataFrame
        print(combined)

        # Average separately for upload and download, then combine into one DataFrame
        for direction, group_df in combined.groupby("direction", sort=False):
            if group_df.empty:
                continue

            numeric_cols = group_df.select_dtypes(include="number").columns
            non_numeric_cols = [c for c in group_df.columns if c not in numeric_cols]
            
            # Optional: print just the numeric columns for debugging
            print(f"Numeric columns for {direction}:")
            print(group_df[numeric_cols])
            
            # Average numeric columns
            avg_numeric = group_df[numeric_cols].mean().to_frame().T

            # Copy representative string columns from the first row (for consistency)
            for col in non_numeric_cols:
                avg_numeric[col] = group_df.iloc[0][col]

            # Keep consistent order of columns
            avg_numeric = avg_numeric.reindex(columns=group_df.columns)

            # Add the averaged row to the result list
            result_rows.append(avg_numeric)


        avg_df = pd.concat(result_rows, ignore_index=True)

        outname = f"{proto}_{bw}_{proc}_avg.csv"
        outpath = os.path.join(best_dir, outname)
        avg_df.to_csv(outpath, index=False)

        print(f"[✓] {proto.upper()} averaged from {len(paths)} runs → {outname}")

    print("✅ Averaging complete (TCP/UDP, Upload+Download in same file).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default=DIR, help="Input directory")
    parser.add_argument("--dest", default=DEST, help="Output directory inside --dir")
    parser.add_argument("--filter", default=FILTER, help="Output directory inside --dir")

    args = parser.parse_args()

    # Override globals ONLY if provided
    if args.dir:
        DIR = args.dir
    if args.dest:
        DEST = args.dest
    if args.filter:
        FILTER = args.filter
        print(FILTER)
    main()