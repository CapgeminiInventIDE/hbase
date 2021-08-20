import pytest

from ..hbase.utils import to_base64, from_base64


@pytest.mark.parametrize("s,e", [("aGVsbG8=", "hello"), ("MTIzNDU=", "12345"), ("", ""),])
def test_from_base64(s, e):
    assert from_base64(s) == e


@pytest.mark.parametrize("s,e", [("hello", "aGVsbG8="), ("12345", "MTIzNDU="), ("", ""),])
def test_to_base64(s, e):
    assert to_base64(s) == e
