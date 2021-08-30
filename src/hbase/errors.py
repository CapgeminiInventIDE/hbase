from uplink import response_handler


class ScannerExhausted(Exception):
    """Raised when the scanner is exhausted (Status Code: 204)"""


class ScannerInvalid(Exception):
    """Raised when the scannerID is invalid (Status Code: 404)"""


class ScannerCreationFailed(Exception):
    """Raised when the scanner has failed to be created (request headers.Location is None)"""


class NoDataFound(Exception):
    """Raised when there is no data to retrive (Status Code: 404)"""


class TableNotFound(Exception):
    """Raised when there is no table found (Status Code: 404)"""


@response_handler
def _raise_for_scanner(response):
    """Handles the errors raised by the stateful scanner"""
    if response.status_code == 204:
        raise ScannerExhausted()
    if response.status_code == 404:
        raise ScannerInvalid()
    return response


@response_handler
def _raise_for_data_not_found(response):
    """Handles the errors for data retrival"""
    if response.status_code == 404:
        raise NoDataFound()
    return response


@response_handler
def _raise_for_table_not_found(response):
    """Handles the errors raised for finding tables"""
    if response.status_code == 404:
        raise TableNotFound()
    return response
