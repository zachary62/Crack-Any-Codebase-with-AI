"""Ch9 flow: map a multi-service architecture in three passes.

BuildBundle overlays the four sources once. Inventory names every node and draws
the graph; TechStack and TraceRequest both reuse its numbered node list so all
three passes describe the same architecture (§9.3-9.5).
"""
from pocketflow import Flow
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import OverviewNode  # noqa: E402
from nodes import BuildBundle, Inventory, TechStack, TraceRequest, overview_spec  # noqa: E402


def create_architecture_flow() -> Flow:
    bundle = BuildBundle()
    inventory = Inventory()
    tech = TechStack()
    trace = TraceRequest()
    overview = OverviewNode(overview_spec)

    bundle >> inventory >> tech >> trace >> overview
    return Flow(start=bundle)
