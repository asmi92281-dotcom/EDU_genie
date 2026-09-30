import warnings

warnings.filterwarnings(
    "ignore",
    message=r"Using .*starlette\.testclient.*deprecated.*",
    category=Warning,
)
