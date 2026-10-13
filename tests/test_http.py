# ruff: noqa: PLR2004
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
import requests
from freqsap.ebi import _get_variants
from freqsap.http import get_with_retry


def _response(status: int) -> requests.Response:
    r = requests.Response()
    r.status_code = status
    return r


def test_retries_transient_status():
    """A 503 followed by a 200 should yield the 200 response."""
    with patch("freqsap.http.requests.get", side_effect=[_response(503), _response(200)]) as get:
        r = get_with_retry("http://x", backoff=0)
    assert r.status_code == 200
    assert get.call_count == 2


def test_retries_connection_error():
    """Connection errors are retried."""
    with patch("freqsap.http.requests.get", side_effect=[requests.ConnectionError(), _response(200)]):
        assert get_with_retry("http://x", backoff=0).ok


def test_raises_when_retries_exhausted():
    """Persistent failures are raised rather than silently dropped."""
    with patch("freqsap.http.requests.get", side_effect=[_response(503)] * 3):
        with pytest.raises(requests.HTTPError):
            get_with_retry("http://x", retries=2, backoff=0)
    with patch("freqsap.http.requests.get", side_effect=requests.Timeout()):
        with pytest.raises(requests.Timeout):
            get_with_retry("http://x", retries=1, backoff=0)


def test_not_found_is_not_retried():
    """A 404 is returned immediately."""
    with patch("freqsap.http.requests.get", return_value=_response(404)) as get:
        assert get_with_retry("http://x", backoff=0).status_code == 404
    assert get.call_count == 1


def _feature(ref: str, begin: str) -> dict:
    return {"type": "VARIANT", "begin": begin, "xrefs": [{"name": "dbSNP", "id": ref}]}


def test_variants_are_deduplicated_and_sorted():
    """The variant list is independent of response order and duplicates."""
    a = {"features": [_feature("rs2", "20"), _feature("rs1", "10"), _feature("rs2", "20")]}
    b = {"features": [_feature("rs1", "10"), _feature("rs2", "20")]}
    assert list(_get_variants(a)) == list(_get_variants(b))
    assert [v.ref for v in _get_variants(a)] == ["rs1", "rs2"]


def test_main_reports_failed_variants(tmp_path, capsys):
    """The CLI exits non-zero and names variants whose retrieval failed."""
    from freqsap import __main__ as cli
    from freqsap.protein import Protein
    from freqsap.variation import Variation

    protein = Protein("P1", [Variation("rs1", 1), Variation("rs2", 2)])
    ebi = MagicMock()
    ebi.available.return_value = True
    ebi.get.return_value = protein
    db = MagicMock()
    db.available.return_value = True
    db.get.side_effect = requests.Timeout("boom")
    args = MagicMock(accession="P12345", timeout=1, regions="Global", output_file=str(tmp_path / "o"), delimiter="\t")
    with (
        patch.object(cli, "parse_args", return_value=args),
        patch.object(cli, "EBI", return_value=ebi),
        patch.object(cli, "DBSNP", return_value=db),
        pytest.raises(SystemExit) as e,
    ):
        cli.main()
    assert e.value.code == 1
    assert "rs1, rs2" in capsys.readouterr().err
