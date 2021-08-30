## Installation

```bash
pip install hbase
```

## Usage

Build an instance to interact with the webservice.

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
