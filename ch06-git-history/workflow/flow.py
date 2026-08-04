"""Ch6 flow: crawl the git log once, then read it at three zoom levels.

FetchHistory does the one git crawl and hands every later node the same commit
list (§6.2: one `git log`, then slice it, never re-query). NameEras surveys the
whole history; ProfileEras and Graveyard dig into what it found.
"""
from pocketflow import Flow
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import OverviewNode  # noqa: E402
from nodes import FetchHistory, NameEras, ProfileEras, Graveyard, overview_spec  # noqa: E402


def create_history_flow() -> Flow:
    fetch = FetchHistory()
    eras = NameEras()
    profile = ProfileEras()
    graves = Graveyard()
    overview = OverviewNode(overview_spec)

    fetch >> eras >> profile >> graves >> overview
    return Flow(start=fetch)
