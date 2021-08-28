import os

import pytest

from ..hbase import *
from ..hbase.models.cell_set import *
from ..hbase.models.namespaces import *
from ..hbase.models.storage_cluster_status import *
from ..hbase.models.table_info import *
from ..hbase.models.table_list import *
from ..hbase.models.table_schema import *
from ..hbase.models.version import *

if os.environ.get("INTEGRATION_TEST") is not None:

    test_table_name = "unit_test"
    hbase = HBase("http://hbase:8080")
    hbase.delete_table(test_table_name)

    def test_software_version():
        assert hbase.get_software_version() == Version(
            Server="jetty/9.3.27.v20190418",
            Jersey="",
            OS="Linux 5.10.47-linuxkit amd64",
            REST="0.0.3",
            JVM="Oracle Corporation 1.8.0_302-25.302-b08",
        )

    def test_storage_cluster_version():
        assert hbase.get_storage_cluster_version() == StorageClusterVersion(Version="2.2.2")

    def test_storage_cluster_status():
        # Testing doesnt raise error
        assert hbase.get_storage_cluster_status()

    def test_get_namespaces():
        assert hbase.get_namespaces() == NameSpaces(Namespace=["default", "hbase"])

    def test_get_tables():
        assert hbase.get_tables() == TableList(table=[])

    def test_get_tables_in_namespace():
        assert hbase.get_tables_in_namespace("default") == TableList(table=[])
        assert hbase.get_tables_in_namespace("hbase") == TableList(
            table=[TableListItem(name="meta"), TableListItem(name="namespace")]
        )

    def test_create_table_lifecycle():
        try:
            hbase.get_schema("bob")
            assert False
        except TableNotFound:
            pass
        assert hbase.get_tables() == TableList(table=[])
        hbase.create_table(test_table_name, ["col1", "col2"])
        schema = hbase.get_schema(test_table_name)
        assert schema.name == test_table_name
        assert {c.name for c in schema.ColumnSchema} == set(["col1", "col2"])
        assert hbase.get_tables() == TableList(table=[TableListItem(name=test_table_name)])
        hbase.delete_table(test_table_name)
        assert hbase.get_tables() == TableList(table=[])

    def test_row_lifecycle():
        hbase.delete_table(test_table_name)
        try:
            hbase.get_row(test_table_name, "*")
            assert False
        except NoDataFound:
            pass
        hbase.create_table(test_table_name, ["col1", "col2"])
        hbase.insert_rows(
            test_table_name, {"row-1": {"col1": "dat1", "col2": "dat2"}, "row-2": {"col1": "dat1", "col2": "dat2"}}
        )
        hbase.insert_row(test_table_name, "row-3", {"col1": "dat1", "col2": "dat2"})
        data = hbase.get_row(test_table_name, "*")
        assert data.Row[0].key == "row-1"
        assert set([data.Row[0].Cell[1].column, data.Row[0].Cell[0].column]) == set(["col1:e", "col2:e"])
        assert set([data.Row[0].Cell[1].value, data.Row[0].Cell[0].value]) == set(["dat1", "dat2"])

        assert data.Row[1].key == "row-2"
        assert set([data.Row[1].Cell[1].column, data.Row[0].Cell[0].column]) == set(["col1:e", "col2:e"])
        assert set([data.Row[1].Cell[1].value, data.Row[0].Cell[0].value]) == set(["dat1", "dat2"])

        assert data.Row[2].key == "row-3"
        assert set([data.Row[2].Cell[1].column, data.Row[0].Cell[0].column]) == set(["col1:e", "col2:e"])
        assert set([data.Row[2].Cell[1].value, data.Row[0].Cell[0].value]) == set(["dat1", "dat2"])

        data = hbase.get_row_with_multiple_columns(test_table_name, "row-3", columns=["col1", "col2"])
        assert data.Row[0].key == "row-3"
        assert set([data.Row[0].Cell[1].column, data.Row[0].Cell[0].column]) == set(["col1:e", "col2:e"])
        assert set([data.Row[0].Cell[1].value, data.Row[0].Cell[0].value]) == set(["dat1", "dat2"])

        r1 = hbase.get_row_with_multiple_columns(test_table_name, "row-*", columns=["col1", "col2"])
        r2 = hbase.get_row(test_table_name, "*")
        assert r1 == r2

        hbase.delete_table(test_table_name)

    def test_cell_lifecycle():
        hbase.delete_table(test_table_name)
        hbase.create_table(test_table_name, ["col1", "col2"])
        hbase.insert_rows(
            test_table_name, {"row-1": {"col1": "dat1", "col2": "dat2"}, "row-2": {"col1": "dat1", "col2": "dat2"}}
        )
        data = hbase.get_cell(test_table_name, "*", "col1")
        assert data.Row[0].key == "row-1"
        assert data.Row[0].Cell[0].column == "col1:e"
        assert data.Row[0].Cell[0].value == "dat1"

        assert data.Row[1].key == "row-2"
        assert data.Row[1].Cell[0].column == "col1:e"
        assert data.Row[1].Cell[0].value == "dat1"

        hbase.delete_table(test_table_name)

    def test_stateless_scanner_lifecycle():
        hbase.delete_table(test_table_name)
        hbase.create_table(test_table_name, ["col1", "col2"])
        hbase.insert_rows(
            test_table_name, {"row-1": {"col1": "dat1", "col2": "dat2"}, "row-2": {"col1": "dat1", "col2": "dat2"}}
        )
        data = hbase.stateless_scanner(test_table_name, "*", batch_size=2)
        assert data.Row[0].key == "row-1"
        assert set([data.Row[0].Cell[1].column, data.Row[0].Cell[0].column]) == set(["col1:e", "col2:e"])
        assert set([data.Row[0].Cell[1].value, data.Row[0].Cell[0].value]) == set(["dat1", "dat2"])

        assert data.Row[1].key == "row-2"
        assert set([data.Row[1].Cell[1].column, data.Row[0].Cell[0].column]) == set(["col1:e", "col2:e"])
        assert set([data.Row[1].Cell[1].value, data.Row[0].Cell[0].value]) == set(["dat1", "dat2"])

        hbase.delete_table(test_table_name)

    def test_scanner_lifecycle():
        hbase.delete_table(test_table_name)
        hbase.create_table(test_table_name, ["col1", "col2"])
        hbase.insert_rows(
            test_table_name, {"row-1": {"col1": "dat1", "col2": "dat2"}, "row-2": {"col1": "dat1", "col2": "dat2"}}
        )
        try:
            hbase.get_next_scanner(test_table_name, "bob")
            assert False
        except ScannerInvalid:
            pass
        scanner_id = hbase.create_scanner(test_table_name, batch_size=2)  # Batch size includes columns
        data = hbase.get_next_scanner(test_table_name, scanner_id)

        rows = ["row-2", "row-1"]
        rows.remove(data.Row[0].key)
        assert set([data.Row[0].Cell[1].column, data.Row[0].Cell[0].column]) == set(["col1:e", "col2:e"])
        assert set([data.Row[0].Cell[1].value, data.Row[0].Cell[0].value]) == set(["dat1", "dat2"])

        data = hbase.get_next_scanner(test_table_name, scanner_id)
        rows.remove(data.Row[0].key)
        assert set([data.Row[0].Cell[1].column, data.Row[0].Cell[0].column]) == set(["col1:e", "col2:e"])
        assert set([data.Row[0].Cell[1].value, data.Row[0].Cell[0].value]) == set(["dat1", "dat2"])

        assert rows == []
        try:
            data = hbase.get_next_scanner(test_table_name, scanner_id)
            assert False
        except ScannerExhausted:
            pass

        assert hbase.delete_scanner(test_table_name, scanner_id).status_code == 200

        # Wildcard table scanner should fail
        try:
            scanner_id = hbase.create_scanner("*")
            assert False
        except ScannerCreationFailed:
            pass

        hbase.delete_table(test_table_name)
