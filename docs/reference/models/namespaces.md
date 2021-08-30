# HBase - Models

::: hbase.models.namespaces
    selection:
        filters:
            - "!^_"  # exclude all members starting with_
            - "!^Config"  # exclude Config Pydantic
    rendering:
        show_if_no_docstring: true
