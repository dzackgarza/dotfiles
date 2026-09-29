import sys

import numpy as np


def render_npy(filepath, start_line=1, end_line=1000):
    try:
        arr = np.load(filepath)
    except Exception as e:
        print(f"Error loading .npy file: {e}")
        return

    lines = ["=== NumPy Array Info ==="]
    lines.append(f"Shape: {arr.shape}")
    lines.append(f"Data type: {arr.dtype}")
    lines.append(f"Size: {arr.size} elements")
    lines.append(f"Memory usage: {arr.nbytes} bytes")
    lines.append("")
    if arr.ndim <= 2 and arr.size <= 1000 or arr.size <= 20:
        lines.append("=== Array Contents ===")
        lines.extend(str(arr).splitlines())
    else:
        lines.append("=== Sample Data ===")
        lines.append(f"First few elements: {arr.flat[:10]}")

    sliced = lines[max(0, start_line - 1) : end_line]
    print("\n".join(sliced))


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        fp = sys.argv[1]
        s = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
        e = int(sys.argv[3]) if len(sys.argv) >= 4 else 1000
        render_npy(fp, s, e)
