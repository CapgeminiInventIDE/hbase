<h1 align="center">
   <strong>hbase</strong>
</h1>

<p align="center">
    <a href="https://codecov.io/gh/CapgeminiInventIDE/hbase" target="_blank">
        <img src="https://img.shields.io/codecov/c/github/CapgeminiInventIDE/hbase?color=%2334D058" alt="Coverage">
    </a>
    <a href="https://CapgeminiInventIDE.github.io/hbase" target="_blank">
        <img src="https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat" alt="Docs">
    </a>
    <a href="https://pypi.org/project/hbase/" target="_blank">
        <img src="https://img.shields.io/pypi/v/hbase.svg" alt="PyPI Latest Release">
    </a>
    <br /><a href="https://github.com/CapgeminiInventIDE/hbase/blob/main/LICENSE" target="_blank">
        <img src="https://img.shields.io/github/license/CapgeminiInventIDE/hbase.svg" alt="License">
    </a>
    <a href="https://github.com/psf/black" target="_blank">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
    </a>
</p>

Hbase REST API client built using uplink

## Main Features

- A transparent and user friendly HBase REST API client
- Easy to extend by subclassing and utilizing uplink's Consumer class
- A great alternative to HBase Thrift client

## Installation

```console
$ pip install hbase

---> 100%
```

## Usage

Build an instance to interact with the web service, check out the [HBase client reference](reference/client.md) for a full list of available methods.

```python
from hbase import HBase

hbase = HBase(base_url="http://localhost:8000")
```

Then, executing an HTTP request is as simply as invoking a method.

```python
# Get all rows using the wildcard, or supply exact row_id for single row
hbase.get_row(table="example_table", row_id="*")
```

The returned object is a friendly Pydantic model which will automatically decode the response from base64:

```python
CellSet(
    Row=[
        Row(
            key="decoded_key", 
            Cell=[
                Cell(
                    column="decoded_column", 
                    timestamp=39082034, 
                    value="decoded_value"
                ), 
                ...
            ]
        ), 
    ...]
)
```

Similarly you can perform other CRUD operations on HBase, such as inserting a row, note that the data will automatically be encoded into base64 for you free of charge!

```python
hbase.insert_rows(
    test_table_name, 
    rows={
        "row-1": {
            "col1": "dat1", 
            "col2": "dat2"
        }, 
        "row-2": {
            "col1": "dat1", 
            "col2": "dat2"
        }
    }
)
hbase.insert_row(
    test_table_name, 
    row_id="row-3", 
    column_data={
        "col1": "dat1", 
        "col2": "dat2"
    }
)
```

For sending non-blocking requests, HBase uses Uplink, which comes with support for aiohttp and twisted.

## Credits

- [Uplink](https://github.com/prkumar/uplink) - A Declarative HTTP Client for Python
- [HBase REST API documentation](https://hbase.apache.org/1.2/apidocs/org/apache/hadoop/hbase/rest/package-summary.html) - Used to help build out the package

## License

- [Mozilla Public License Version](/LICENSE)
