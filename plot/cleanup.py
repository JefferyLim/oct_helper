import os
import pandas as pd
import re
import argparse

def parse_filename(filename):
    """
    Extract protocol, X, Y from filenames like:
    tcp_10G_5_random.csv
    Returns (protocol, x, y)
    """
    match = re.match(r"(tcp|udp)_([0-9]+G)_([0-9]+)_.*\.csv$", filename, re.IGNORECASE)
    if match:
        return match.group(1).lower(), match.group(2), match.group(3)
    return None


def is_bad_file(df):
    """
    A file is considered bad if *any* row has throughput_mbps == 0.
    """
    return (df["throughput_mbps"] == 0).any()

def main():
    # Discover run directories
    
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")   # one positional parameter
    args = parser.parse_args()

    DIR = args.dir
    os.makedirs(DIR + "/best", exist_ok=True)
    
    run_dirs = sorted(d for d in os.listdir(DIR) if d.startswith("run"))
    for filename in os.listdir(os.path.join(DIR, "best/")):
        if not filename.endswith(".csv"):
            continue

        parsed = parse_filename(filename)
        if not parsed:
            print(f"Skipping unrecognized format: {filename}")
            continue

        proto, x, y = parsed
        best_path = os.path.join(DIR + "best/", filename)
        df_best = pd.read_csv(best_path)

        if not is_bad_file(df_best):
            continue

        print(f"[!] Needs replacement: {filename}")

        replacement_df = None

        # Search in run directories for *pattern matched* alternatives
        for run in run_dirs:
            run_path = os.path.join(DIR, run)
            print(run_path)
            for candidate in os.listdir(run_path):
                if not candidate.endswith(".csv"):
                    continue

                p = parse_filename(candidate)
                if not p:
                    continue

                c_proto, c_x, c_y = p

                if (proto == c_proto) and (x == c_x) and (y == c_y):
                    candidate_path = os.path.join(run_path, candidate)
                    df_candidate = pd.read_csv(candidate_path)

                    if not is_bad_file(df_candidate):
                        replacement_df = df_candidate
                        print(f"  -> Using {candidate} from {run}")
                        break

            if replacement_df is not None:
                break

        if replacement_df is not None:
            replacement_df.to_csv(best_path, index=False)
        else:
            print(f"  !! No good replacement found for {filename}")
            
if __name__ == "__main__":
    main()
