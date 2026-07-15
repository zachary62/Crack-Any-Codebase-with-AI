"""Ch7 flow: find the schema, then project it into four views.

FindSchema reads the schema file once. SchemaTour runs next because its ERD
names the ~20 core tables that TraceFlows and TableDeepDive reuse (§7.4).
MigrationActs is independent — it reads the migration folder, not the schema.
"""
import os
import sys

from pocketflow import Flow

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import OverviewNode  # noqa: E402
from nodes import FindSchema, SchemaTour, TraceFlows, TableDeepDive, MigrationActs, overview_spec  # noqa: E402


def create_schema_flow() -> Flow:
    find = FindSchema()
    tour = SchemaTour()
    flows = TraceFlows()
    deep = TableDeepDive()
    migrations = MigrationActs()
    overview = OverviewNode(overview_spec)

    find >> tour >> flows >> deep >> migrations >> overview
    return Flow(start=find)
