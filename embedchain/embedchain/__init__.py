import importlib.metadata



from embedchain.app import App  # noqa: F401
from embedchain.client import Client  # noqa: F401
from embedchain.pipeline import Pipeline  # noqa: F401

# Setup the user directory if doesn't exist already
Client.setup()
