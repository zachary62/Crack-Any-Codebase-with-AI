"""Ch8 flow: read an API surface at three levels of zoom.

FindRoutes collects the surface files once. ApiMenu groups them into features;
TraceActions reuses those feature groups to trace user gestures; EndpointSequence
picks the most illustrative endpoint from the menu, reads its handler, and draws
a sequence diagram (§8.3-8.5).
"""
from pocketflow import Flow
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import OverviewNode  # noqa: E402
from nodes import FindRoutes, ApiMenu, TraceActions, EndpointSequence, overview_spec  # noqa: E402


def create_interface_flow() -> Flow:
    find = FindRoutes()
    menu = ApiMenu()
    trace = TraceActions()
    seq = EndpointSequence()
    overview = OverviewNode(overview_spec)

    find >> menu >> trace >> seq >> overview
    return Flow(start=find)
