"""Public tests for pay_authz_01 (valid signature creates invoice; invalid raises)."""

import pytest

from payments import storage, verify

SECRET = "whsec_test_public"


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_valid_signature_creates_invoice():
    sig = verify.expected_signature("e1", 1000, SECRET)
    invoice = verify.process_signed_webhook("e1", 1000, sig, SECRET)
    assert invoice.event_id == "e1"
    assert invoice.amount == 1000
    assert storage.count_for_event("e1") == 1


def test_invalid_signature_raises_and_creates_no_invoice():
    with pytest.raises(PermissionError):
        verify.process_signed_webhook("e1", 1000, "deadbeef", SECRET)
    assert storage.count_for_event("e1") == 0
