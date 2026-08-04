"""Ch10 flow: read a backend as its six layers.

BuildBundle crawls the source into the six layers once; Pipeline, LayerCode, and
Trace are three independent reads of that same bundle — the map, the custom
code, and one request in motion (§10.3-10.5).
"""
from pocketflow import Flow
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import OverviewNode  # noqa: E402
from nodes import BuildBundle, Pipeline, LayerCode, Trace, overview_spec  # noqa: E402


def create_backend_flow() -> Flow:
    bundle = BuildBundle()
    pipeline = Pipeline()
    layercode = LayerCode()
    trace = Trace()
    overview = OverviewNode(overview_spec)

    bundle >> pipeline >> layercode >> trace >> overview
    return Flow(start=bundle)
