# This file makes the vid_vec_rep_clip directory a Python package
# It allows Python to find the vid_vec_rep_clip module when it's imported

# Import the main module to make its functions available when the package is imported
from .vid_vec_rep_clip import cleanup, initialize, run, state

# Export the public API
__all__ = ["initialize", "run", "cleanup", "state"]
