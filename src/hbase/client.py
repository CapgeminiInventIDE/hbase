import json
from typing import Dict, List, Optional

import requests
from uplink import (
    Body,
    Consumer,
    Path,
    Query,
    delete,
    get,
    headers,
    post,
    returns,
)

from .errors import (
    ScannerCreationFailed,
    _raise_for_data_not_found,
    _raise_for_scanner,
    _raise_for_table_not_found,
)
from .models import (
    CellSet,
    NameSpaces,
    StorageClusterStatus,
    StorageClusterVersion,
    TableInfo,
    TableList,
    TableSchema,
    Version,
)
from .utils import to_base64


class HBase(Consumer):
    """A Python Client for the HBase API.

    Build using the following references:
            [HBase REST API docs - 1.2](https://hbase.apache.org/1.2/apidocs/org/apache/hadoop/hbase/rest/package-summary.html)

    Notes:
        ```md
        Built to:
            Server='jetty/9.3.27.v20190418'
            Jersey=''
            OS='Linux 5.10.47-linuxkit amd64'
            REST='0.0.3'
            JVM='Oracle Corporation 1.8.0_302-25.302-b08'
            StorageClusterVersion='2.2.2'
        ```
    """

    ### GET ###

    @returns.json
    @headers({"Accept": "application/json"})
    @get("version")
    def get_software_version(self) -> Version:
        """Returns the software version"""

    @returns.json
    @headers({"Accept": "application/json"})
    @get("version/cluster")
    def get_storage_cluster_version(self) -> StorageClusterVersion:
        """Returns version information regarding the HBase cluster backing the Stargate instance."""

    @returns.json
    @headers({"Accept": "application/json"})
    @get("status/cluster")
    def get_storage_cluster_status(self) -> StorageClusterStatus:
        """Returns detailed status on the HBase cluster backing the Stargate instance."""

    @returns.json(NameSpaces)
    @headers({"Accept": "application/json"})
    @get("namespaces")
    def get_namespaces(self) -> NameSpaces:
        """Lists all namespaces"""

    @returns.json
    @headers({"Accept": "application/json"})
    @get("")
    def get_tables(self) -> TableList:
        """Retrieves the list of available tables"""

    @returns.json
    @headers({"Accept": "application/json"})
    @get("namespaces/{namespace}/tables")
    def get_tables_in_namespace(self, namespace: Path(type=str)) -> TableList:
        """Retrieves the list of available tables in the given namespace"""

    @_raise_for_table_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/schema")
    def get_schema(self, table: Path) -> TableSchema:
        """Retrieves the table schema."""

    @_raise_for_table_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/regions")
    def get_table_metadata(self, table: Path) -> TableInfo:
        """Retrieves table region metadata"""

    @_raise_for_data_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/{row_id}")
    def get_row(self, table: Path, row_id: Path, num_versions: Query("v") = None) -> CellSet:  # noqa: F821
        """Retrieves single row, or multiple rows using *"""

    @_raise_for_data_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/{row_id}/{column}")
    def get_cell(
        self, table: Path, row_id: Path, column: Path, num_versions: Query("v") = None  # noqa: F821
    ) -> CellSet:  # noqa: F821
        """Retrieves single cell, use column={column_name}:{qualifier} for qualifiers"""

    @_raise_for_data_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/{row_id}/{column}/{timestamp}")
    def get_cell_with_timestamp(
        self, table: Path, row_id: Path, column: Path, timestamp: Path, num_versions: Query("v") = None  # noqa: F821
    ) -> CellSet:
        """Retrieves single cell with the given timestamp, use column={column_name}:{qualifier} for qualifiers"""

    def get_row_with_multiple_columns(
        self,
        table: str,
        row_id: str,
        columns: List[str] = [],
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        num_versions: Optional[int] = None,
    ):
        """Retrieves one or more cells from a full row, or one or more 
        specified columns in the row, with optional filtering via timestamp, 
        and an optional restriction on the maximum number of versions to return."""

        return self.stateless_scanner(
            table,
            row_prefix=row_id,
            columns=columns,
            start_time=start_time,
            end_time=end_time,
            max_versions=num_versions,
        )

    @_raise_for_scanner
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/scanner/{scanner_id}")
    def get_next_scanner(self, table: Path, scanner_id: Path) -> CellSet:
        """Returns the values of the next cells found by the scanner, up to the configured batch amount."""

    @_raise_for_data_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/{row_prefix}*")
    def stateless_scanner(
        self,
        table: Path,
        row_prefix: Path = "",
        start_row: Query("startrow") = None,  # noqa: F821
        end_row: Query("endrow") = None,  # noqa: F821
        columns: Query("columns") = None,  # noqa: F821
        start_time: Query("starttime") = None,  # noqa: F821
        end_time: Query("endtime") = None,  # noqa: F821
        max_versions: Query("maxversions") = None,  # noqa: F821
        batch_size: Query("batchsize") = None,  # noqa: F821
        limit: Query("limit") = None,  # noqa: F821
    ) -> CellSet:
        """The current scanner API expects clients to restart scans if there is a REST server failure in the midst. The stateless does not store any state related to scan operation and all the parameters are specified as query parameters.

        Args:
            table (Path): [description]
            row_prefix (Path, optional): [description]. Defaults to "".
            start_row (Query, optional):  The start row for the scan. Defaults to None.
            end_row (Query, optional): The end row for the scan. Defaults to None.
            columns (Query, optional): The columns to scan. Defaults to None.
            start_time (Query, optional): To only retrieve columns within a specific range of version timestamps. Defaults to None.
            end_time (Query, optional): To only retrieve columns within a specific range of version timestamps. Defaults to None.
            max_versions (Query, optional): To limit the number of versions of each column to be returned. Defaults to None.
            batch_size (Query, optional): To limit the maximum number of values returned for each call to next().. Defaults to None.
            limit (Query, optional): The number of rows to return in the scan operation.. Defaults to None.

        Raises:
            ScannerCreationFailed: Raised when the scanner has failed to be created (request headers.Location is None)

        Returns:
            CellSet: The data retrieved from HBase

        Notes:
            More on start row, end row and limit parameters.

            - If start row, end row and limit not specified, then the whole table will be scanned.
            - If start row and limit (say N) is specified, then the scan operation will return N rows from the start row specified.
            - If only limit parameter is specified, then the scan operation will return N rows from the start of the table.
            - If limit and end row are specified, then the scan operation will return N rows from start of table till the end row. If the end row is reached before N rows ( say M and M < N ), then M rows will be returned to the user.
            - If start row, end row and limit (say N ) are specified and N < number of rows between start row and end row, then N rows from start row will be returned to the user. If N > (number of rows between start row and end row (say M), then M number of rows will be returned to the user.
        """

    ### POST ###

    @headers({"Accept": "application/json"})
    @post("namespaces/{namespace}")
    def create_namespace(self, namespace: Path) -> requests.models.Response:
        """Creates a namespace in HBase, this operation is idempotent

        Args:
            namespace (str): (Type: string) The name of the namespace you want to create

        Returns:
            requests.models.Response: The response for the user to handle and check the response code
        """

    @headers({"Accept": "text/xml", "Content-Type": "text/xml"})
    @post("{table}/scanner")
    def __create_scanner(self, table: Path, data: Body) -> requests.models.Response:
        """Allocates a new table scanner."""

    def create_scanner(
        self,
        table: str,
        start_row: Optional[str] = None,
        end_row: Optional[str] = None,
        columns: List[str] = [],
        batch_size: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> Optional[str]:
        """Creates a scanner and returns the scanner id"""
        add_if = lambda key, val: f'{key}="{val}" ' if val is not None else ""
        xml = f"""<Scanner {add_if("batch", batch_size)}{add_if("startRow", to_base64(start_row))}{add_if("endRow", to_base64(end_row))}{add_if("columns", to_base64(",".join(columns)))}{add_if("startTime", start_time)}{add_if("endTime", end_time)}/>"""
        resp = self.__create_scanner(table, xml).headers.get("Location")
        if resp is None:
            raise ScannerCreationFailed("Unable to create Scanner")
        return resp.split("/")[-1]

    @headers({"Accept": "application/json", "Content-Type": "application/json"})
    @post("{table}/XXX")  # XXX = <false-row-id>
    def __insert_row(self, table: Path, data: Body) -> requests.models.Response:
        """Stores cell data into the specified location."""
        # TODO: Look into the <false-row-id> - dont think we want to hardcode?

    def insert_row(self, table: str, row_id: str, column_data: Dict[str, str]) -> requests.models.Response:
        """Utility function for inserting a single row into a table"""
        return self.insert_rows(table, {row_id: column_data})

    def insert_rows(self, table: str, rows: Dict[str, Dict[str, str]]) -> requests.models.Response:
        """Utility function for inserting multiple rows into a table"""
        # TODO: Look into the column qualifier - dont think we want to hardcode?
        packet = {
            "Row": [
                {
                    "key": to_base64(row_id),
                    "Cell": [{"column": to_base64(f"{k}:e"), "$": to_base64(v)} for k, v in row.items()],
                }
                for row_id, row in rows.items()
            ]
        }

        return self.__insert_row(table, data=json.dumps(packet))

    @headers({"Accept": "text/xml", "Content-Type": "text/xml"})
    @post("{table}/schema")
    def __create_table(self, table: Path, schema: Body) -> requests.models.Response:
        """Creates the table by uploading the table schema."""

    def create_table(self, table: str, column_names: List[str]) -> requests.models.Response:
        """Utility function for creating a table - HBase REST API only accepts XML for this request"""
        xml_packet = f"""<?xml version="1.0" encoding="UTF-8"?><TableSchema name="{table}">{''.join(f'<ColumnSchema name="{col}" />' for col in column_names)}</TableSchema>"""
        return self.__create_table(table, xml_packet)

    ### DELETE ###

    @delete("{table}/schema")
    def delete_table(self, table: Path) -> requests.models.Response:
        """Deletes a table, if successful, returns HTTP 200 status."""

    @delete("namespaces/{namespace}")
    def delete_namespace(self, namespace: Path) -> requests.models.Response:
        """Deletes a table, if successful, returns HTTP 200 status."""

    @delete("{table}/{row_id}")
    def delete_row(self, table: Path, row_id: Path) -> requests.models.Response:
        """Deletes a entire row from the table, if successful, returns HTTP 200 status."""

    @delete("{table}/{row_id}/{column}")
    def delete_cell(self, table: Path, row_id: Path, column: Path) -> requests.models.Response:
        """Deletes a entire cell from the table, if successful, returns HTTP 200 status."""

    @delete("{table}/{row_id}/{column}/{timestamp}")
    def delete_cell_with_timestamp(
        self, table: Path, row_id: Path, column: Path, timestamp: Path
    ) -> requests.models.Response:
        """Deletes a entire cell with the given timestamp from the table, if successful, returns HTTP 200 status."""

    @delete("{table}/scanner/{scanner_id}")
    def delete_scanner(self, table: Path, scanner_id: Path) -> requests.models.Response:
        """Deletes resources associated with the scanner. 
        This is an optional action. Scanners will expire 
        after some globally configurable interval has elapsed 
        with no activity on the scanner.
        """
