import sys
import warnings
from pathlib import Path

warnings.filterwarnings(
    "ignore",
    message=r"Using .*starlette\.testclient.*deprecated.*",
    category=Warning,
)

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
