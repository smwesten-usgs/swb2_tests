"""
D8 flow routing implementation matching SWB2's routing__D8.F90.

SWB2 D8 codes (same as ArcGIS):
    32  64  128
    16   0    1
     8   4    2

Cells are processed upstream→downstream. Each cell's runoff + rejected_net_infiltration
is added to its downstream target's runon. The outlet cell (code 0 or off-grid target)
accumulates to runoff_outside.
"""
import numpy as np
from collections import deque

# D8 direction codes → (row_offset, col_offset)
# Row increases southward (row 1 = north), col increases eastward
D8_OFFSETS = {
    1:   (0, 1),    # East
    2:   (1, 1),    # Southeast
    4:   (1, 0),    # South
    8:   (1, -1),   # Southwest
    16:  (0, -1),   # West
    32:  (-1, -1),  # Northwest
    64:  (-1, 0),   # North
    128: (-1, 1),   # Northeast
}


def read_asc_grid(filepath):
    """Read an Arc ASCII grid, return header dict and 2D numpy array."""
    header = {}
    with open(filepath) as f:
        for _ in range(6):
            parts = f.readline().split()
            header[parts[0].lower()] = float(parts[1]) if '.' in parts[1] else int(parts[1])
    data = np.loadtxt(filepath, skiprows=6, dtype=int)
    return header, data


def get_target(row, col, flow_dir, nrows, ncols):
    """Return (target_row, target_col) or None if outlet/off-grid."""
    if flow_dir not in D8_OFFSETS:
        return None
    dr, dc = D8_OFFSETS[flow_dir]
    tr, tc = row + dr, col + dc
    if 0 <= tr < nrows and 0 <= tc < ncols:
        return (tr, tc)
    return None


def compute_sort_order(flow_dir_grid):
    """
    Compute upstream→downstream processing order via topological sort (Kahn's algorithm).
    Returns list of (row, col) tuples in processing order.
    """
    nrows, ncols = flow_dir_grid.shape
    # Count incoming edges for each cell
    in_degree = np.zeros((nrows, ncols), dtype=int)

    for r in range(nrows):
        for c in range(ncols):
            target = get_target(r, c, flow_dir_grid[r, c], nrows, ncols)
            if target is not None:
                in_degree[target] += 1

    # Start with cells that have no upstream contributors
    queue = deque()
    for r in range(nrows):
        for c in range(ncols):
            if in_degree[r, c] == 0:
                queue.append((r, c))

    order = []
    while queue:
        r, c = queue.popleft()
        order.append((r, c))
        target = get_target(r, c, flow_dir_grid[r, c], nrows, ncols)
        if target is not None:
            in_degree[target] -= 1
            if in_degree[target] == 0:
                queue.append(target)

    return order


def route_one_day(flow_dir_grid, runoff_grid, rejected_infil_grid=None):
    """
    Perform D8 routing for a single day.

    Args:
        flow_dir_grid: 2D array of D8 flow direction codes
        runoff_grid: 2D array of runoff values (inches) for each cell
        rejected_infil_grid: 2D array of rejected net infiltration (optional, defaults to 0)

    Returns:
        runon: 2D array of accumulated runon at each cell
        runoff_outside: 2D array of water leaving the grid at each cell
    """
    nrows, ncols = flow_dir_grid.shape
    runon = np.zeros((nrows, ncols), dtype=float)
    runoff_outside = np.zeros((nrows, ncols), dtype=float)

    if rejected_infil_grid is None:
        rejected_infil_grid = np.zeros((nrows, ncols), dtype=float)

    order = compute_sort_order(flow_dir_grid)

    for r, c in order:
        outflow = runoff_grid[r, c] + rejected_infil_grid[r, c]
        target = get_target(r, c, flow_dir_grid[r, c], nrows, ncols)
        if target is not None:
            runon[target] += outflow
        else:
            runoff_outside[r, c] += outflow

    return runon, runoff_outside
