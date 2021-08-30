# HBase - Models

::: hbase.models.cell_set
    selection:
        filters:
            - "!^_"  # exclude all members starting with _
            - "!^Config"  # exclude Config Pydantic
    rendering:
        show_if_no_docstring: true
