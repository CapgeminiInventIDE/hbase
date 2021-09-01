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
        """Returns the software version

        Returns:
            Version: Version information about HBase
        """

    @returns.json
    @headers({"Accept": "application/json"})
    @get("version/cluster")
    def get_storage_cluster_version(self) -> StorageClusterVersion:
        """Returns version information regarding the HBase cluster backing the Stargate instance.

        Returns:
            StorageClusterVersion: Version information regarding the HBase cluster backing the Stargate instance
        """

    @returns.json
    @headers({"Accept": "application/json"})
    @get("status/cluster")
    def get_storage_cluster_status(self) -> StorageClusterStatus:
        """Returns detailed status on the HBase cluster backing the Stargate instance.

        Returns:
            StorageClusterStatus: Detailed status on the HBase cluster backing the Stargate instance.
        """

    @returns.json(NameSpaces)
    @headers({"Accept": "application/json"})
    @get("namespaces")
    def get_namespaces(self) -> NameSpaces:
        """Lists all namespaces

        Returns:
            NameSpaces: All of the namespaces for the HBase instance
        """

    @returns.json
    @headers({"Accept": "application/json"})
    @get("")
    def get_tables(self) -> TableList:
        """Retrieves the list of available tables

        Returns:
            TableList: The list of available tables
        """

    @returns.json
    @headers({"Accept": "application/json"})
    @get("namespaces/{namespace}/tables")
    def get_tables_in_namespace(self, namespace: Path(type=str)) -> TableList:
        """Retrieves the list of available tables in the given namespace

        Args:
            namespace (str): The given namespace.

        Returns:
            TableList: The list of available tables in the given namespace
        """

    @_raise_for_table_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/schema")
    def get_schema(self, table: Path(type=str)) -> TableSchema:
        """Retrieves the table schema.

        Args:
            table (str): The table for which schema you want to get

        Raises:
            TableNotFound: When the table is not found on HBase

        Returns:
            TableSchema: The table schema
        """

    @_raise_for_table_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/regions")
    def get_table_metadata(self, table: Path(type=str)) -> TableInfo:
        """Retrieves table region metadata

        Args:
            table (str): The table for which metadata you want to get

        Raises:
            TableNotFound: When the table is not found on HBase

        Returns:
            TableInfo: The table region metadata
        """

    @_raise_for_data_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/{row_id}")
    def get_row(
        self, table: Path(type=str), row_id: Path(type=str), num_versions: Query("v", type=int) = None  # noqa: F821
    ) -> CellSet:  # noqa: F821
        """Retrieves single row, or multiple rows using *

        Args:
            table (str): The table for which you want to get the data from
            row_id (str): The row ID for which you want to get the data from. Use * for multiple rows.
            num_versions (int, optional): The number of versions to return. Defaults to None.

        Raises:
            NoDataFound: If no data is found for the given table and row_id 

        Returns:
            CellSet: The data from the requested HBase Cell/s
        """

    @_raise_for_data_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/{row_id}/{column}")
    def get_cell(
        self,
        table: Path(type=str),  # noqa: F821
        row_id: Path(type=str),  # noqa: F821
        column: Path(type=str),  # noqa: F821
        num_versions: Query("v", type=int) = None,  # noqa: F821
    ) -> CellSet:  # noqa: F821
        """Retrieves single cell, use column={column_name}:{qualifier} for qualifiers

        Args:
            table (str): The table for which you want to get the data from
            row_id (str): The row ID for which you want to get the data from. Use * for multiple rows.
            column (str): The column name you want to get data from
            num_versions (int, optional): The number of versions to return. Defaults to None.

        Raises:
            NoDataFound: If no data is found for the given table, row_id and column

        Returns:
            CellSet: The data from the requested HBase Cell/s
        """

    @_raise_for_data_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/{row_id}/{column}/{timestamp}")
    def get_cell_with_timestamp(
        self,
        table: Path(type=str),  # noqa: F821
        row_id: Path(type=str),  # noqa: F821
        column: Path(type=str),  # noqa: F821
        timestamp: Path(type=int),  # noqa: F821
        num_versions: Query("v", type=int) = None,  # noqa: F821
    ) -> CellSet:
        """Retrieves single cell with the given timestamp, use column={column_name}:{qualifier} for qualifiers

        Args:
            table (str): The table for which you want to get the data from
            row_id (str): The row ID for which you want to get the data from. Use * for multiple rows.
            column (str): The column name you want to get data from
            timestamp (int): The given timestamp to filter by
            num_versions (int, optional): The number of versions to return. Defaults to None.

        Raises:
            NoDataFound: If no data is found for the given table, row_id and column

        Returns:
            CellSet: The data from the requested HBase Cell/s
        """

    def get_row_with_multiple_columns(
        self,
        table: str,
        row_id: str,
        columns: List[str] = [],
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        num_versions: Optional[int] = None,
    ) -> CellSet:
        """Retrieves one or more cells from a full row, or one or more 
        specified columns in the row, with optional filtering via timestamp, 
        and an optional restriction on the maximum number of versions to return.

        Args:
            table (str): The table for which you want to get the data from
            row_id (str): The row ID for which you want to get the data from. Use * for multiple rows.
            columns (List[str], optional): The column name you want to get data from. Defaults to [].
            start_time (Optional[int], optional): The given start timestamp to filter by. Defaults to None.
            end_time (Optional[int], optional): The given end timestamp to filter by. Defaults to None.
            num_versions (Optional[int], optional): The number of versions to return. Defaults to None.

        Raises:
            NoDataFound: If no data is found for the given table, row_id and filters

        Returns:
            CellSet: The data from the requested HBase Cell/s
        """

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
    def get_next_scanner(self, table: Path(type=str), scanner_id: Path(type=str)) -> CellSet:
        """Returns the values of the next cells found by the scanner, up to the configured batch amount.

        Args:
            table (str): The table for which you want to get the data from
            scanner_id (str): The scanner id gathered from HBase.create_scanner()

        Raises:
            ScannerCreationFailed: If the scanner fails

        Returns:
            CellSet: The next round of data from the requested HBase Cell/s using the scanner
        """

    @_raise_for_data_not_found
    @returns.json
    @headers({"Accept": "application/json"})
    @get("{table}/{row_prefix}")
    def stateless_scanner(
        self,
        table: Path(type=str),
        row_prefix: Path(type=str) = "*",
        start_row: Query("startrow", type=str) = None,  # noqa: F821
        end_row: Query("endrow", type=str) = None,  # noqa: F821
        columns: Query("columns", type=List[str]) = None,  # noqa: F821
        start_time: Query("starttime", type=int) = None,  # noqa: F821
        end_time: Query("endtime", type=int) = None,  # noqa: F821
        max_versions: Query("maxversions", type=int) = None,  # noqa: F821
        batch_size: Query("batchsize", type=int) = None,  # noqa: F821
        limit: Query("limit", type=int) = None,  # noqa: F821
    ) -> CellSet:
        """The current scanner API expects clients to restart scans if there is a REST server failure in the midst. The stateless does not store any state related to scan operation and all the parameters are specified as query parameters.

        Args:
            table (str): The table for which you want to get the data from
            row_prefix (str, optional): The row ID for which you want to get the data from. Use * for multiple rows.. Defaults to all rows (*).
            start_row (str, optional):  The start row for the scan. Defaults to None.
            end_row (str, optional): The end row for the scan. Defaults to None.
            columns (List[str], optional): The columns to scan. Defaults to None.
            start_time (int, optional): To only retrieve columns within a specific range of version timestamps. Defaults to None.
            end_time (int, optional): To only retrieve columns within a specific range of version timestamps. Defaults to None.
            max_versions (int, optional): To limit the number of versions of each column to be returned. Defaults to None.
            batch_size (int, optional): To limit the maximum number of values returned for each call to next().. Defaults to None.
            limit (int, optional): The number of rows to return in the scan operation.. Defaults to None.

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
    def create_namespace(self, namespace: Path(type=str)) -> requests.models.Response:
        """Creates a namespace in HBase, this operation is idempotent

        Args:
            namespace (str): (Type: string) The name of the namespace you want to create

        Returns:
            requests.models.Response: The response for the user to handle and check the response code
        """

    @headers({"Accept": "text/xml", "Content-Type": "text/xml"})
    @post("{table}/scanner")
    def __create_scanner(self, table: Path(type=str), data: Body) -> requests.models.Response:
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
    ) -> str:
        """Creates a scanner and returns the scanner id

        Args:
            table (str): The table for which you want to get the data from
            row_prefix (str, optional): The row ID for which you want to get the data from. Use * for multiple rows.. Defaults to "".
            start_row (str, optional):  The start row for the scan. Defaults to None.
            end_row (str, optional): The end row for the scan. Defaults to None.
            columns (List[str], optional): The columns to scan. Defaults to None.
            batch_size (int, optional): To limit the maximum number of values returned for each call to next().. Defaults to None.
            start_time (int, optional): To only retrieve columns within a specific range of version timestamps. Defaults to None.
            end_time (int, optional): To only retrieve columns within a specific range of version timestamps. Defaults to None.

        Raises:
            ScannerCreationFailed: Raised when the scanner has failed to be created (request headers.Location is None)

        Returns:
            str: The scanner ID

        Notes:
            More on start row, end row and limit parameters.

            - If start row, end row and limit not specified, then the whole table will be scanned.
            - If start row and limit (say N) is specified, then the scan operation will return N rows from the start row specified.
            - If only limit parameter is specified, then the scan operation will return N rows from the start of the table.
            - If limit and end row are specified, then the scan operation will return N rows from start of table till the end row. If the end row is reached before N rows ( say M and M < N ), then M rows will be returned to the user.
            - If start row, end row and limit (say N ) are specified and N < number of rows between start row and end row, then N rows from start row will be returned to the user. If N > (number of rows between start row and end row (say M), then M number of rows will be returned to the user.
        """
        add_if = lambda key, val: f'{key}="{val}" ' if val is not None else ""
        xml = f"""<Scanner {add_if("batch", batch_size)}{add_if("startRow", to_base64(start_row))}{add_if("endRow", to_base64(end_row))}{add_if("columns", to_base64(",".join(columns)))}{add_if("startTime", start_time)}{add_if("endTime", end_time)}/>"""
        resp = self.__create_scanner(table, xml).headers.get("Location")
        if resp is None:
            raise ScannerCreationFailed("Unable to create Scanner")
        return resp.split("/")[-1]

    @headers({"Accept": "application/json", "Content-Type": "application/json"})
    @post("{table}/XXX")  # XXX = <false-row-id>
    def __insert_row(self, table: Path(type=str), data: Body) -> requests.models.Response:
        """Stores cell data into the specified location."""
        # TODO: Look into the <false-row-id> - dont think we want to hardcode?

    def insert_row(self, table: str, row_id: str, column_data: Dict[str, str]) -> requests.models.Response:
        """Utility function for inserting a single row into a table

        Args:
            table (str): The table for which you want to get the data from
            row_id (str): The row ID for which you want to get the data from. Use * for multiple rows.
            column_data (Dict[str, str]): The data for the row you wish to insert into the table

        Returns:
            requests.models.Response: The HTTP response from inserting the row for the user to check
        """
        return self.insert_rows(table, {row_id: column_data})

    def insert_rows(self, table: str, rows: Dict[str, Dict[str, str]]) -> requests.models.Response:
        """Utility function for inserting multiple rows into a table

        Args:
            table (str): The table for which you want to get the data from
            rows (Dict[str, Dict[str, str]]): The data for the row you wish to insert into the table, the keys should be the row id's

        Returns:
            requests.models.Response: The HTTP response from inserting the rows for the user to check
        """
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
    def __create_table(self, table: Path(type=str), schema: Body) -> requests.models.Response:
        """Creates the table by uploading the table schema."""

    def create_table(self, table: str, column_names: List[str]) -> requests.models.Response:
        """Utility function for creating a table - HBase REST API only accepts XML for this request

        Args:
            table (str): The name of the table you wish to create
            column_names (List[str]): The list of the table column names

        Returns:
            requests.models.Response: The HTTP response from creating the table for the user to check
        """
        xml_packet = f"""<?xml version="1.0" encoding="UTF-8"?><TableSchema name="{table}">{''.join(f'<ColumnSchema name="{col}" />' for col in column_names)}</TableSchema>"""
        return self.__create_table(table, xml_packet)

    ### DELETE ###

    @delete("{table}/schema")
    def delete_table(self, table: Path(type=str)) -> requests.models.Response:
        """Deletes a table, if successful, returns HTTP 200 status.

        Args:
            table (str): The name of the table you wish to delete.

        Returns:
            requests.models.Response: The HTTP response from deleting the table for the user to check
        """

    @delete("namespaces/{namespace}")
    def delete_namespace(self, namespace: Path(type=str)) -> requests.models.Response:
        """Deletes a table, if successful, returns HTTP 200 status.

        Args:
            namespace (str): The name of the namespace you wish to delete.

        Returns:
            requests.models.Response: The HTTP response from deleting the namespace for the user to check
        """

    @delete("{table}/{row_id}")
    def delete_row(self, table: Path(type=str), row_id: Path(type=str)) -> requests.models.Response:
        """Deletes a entire row from the table, if successful, returns HTTP 200 status.

        Args:
            table (str): The name of the table from which the row belongs that you wish to delete.
            row_id (str): The name of the row_id that you wish to delete.

        Returns:
            requests.models.Response: The HTTP response from deleting the row for the user to check
        """

    @delete("{table}/{row_id}/{column}")
    def delete_cell(
        self, table: Path(type=str), row_id: Path(type=str), column: Path(type=str)
    ) -> requests.models.Response:
        """Deletes a entire cell from the table, if successful, returns HTTP 200 status.

        Args:
            table (str): The name of the table from which the cell belongs that you wish to delete.
            row_id (str): The name of the row_id from which the cell belongs that you wish to delete.
            column (str): The name of the column from which the cell belongs that you wish to delete.

        Returns:
            requests.models.Response: The HTTP response from deleting the cell for the user to check
        """

    @delete("{table}/{row_id}/{column}/{timestamp}")
    def delete_cell_with_timestamp(
        self, table: Path(type=str), row_id: Path(type=str), column: Path(type=str), timestamp: Path(type=int)
    ) -> requests.models.Response:
        """Deletes a entire cell with the given timestamp from the table, if successful, returns HTTP 200 status.

        Args:
            table (str): The name of the table from which the cell belongs that you wish to delete.
            row_id (str): The name of the row_id from which the cell belongs that you wish to delete.
            column (str): The name of the column from which the cell belongs that you wish to delete.
            timestamp (int): The timestamp from which the cell belongs that you wish to delete.

        Returns:
            requests.models.Response: The HTTP response from deleting the cell for the user to check
        """

    @delete("{table}/scanner/{scanner_id}")
    def delete_scanner(self, table: Path(type=str), scanner_id: Path(type=str)) -> requests.models.Response:
        """Deletes resources associated with the scanner. 
        Note: 
            This is an optional action. 
            Scanners will expire after some globally configurable interval has 
            elapsed with no activity on the scanner.

        Args:
            table (str): The table name that the scanner is attached to.
            scanner_id (str): The scanner id gathered from HBase.create_scanner().

        Returns:
            requests.models.Response: The HTTP response from deleting the scanner for the user to check
        """
