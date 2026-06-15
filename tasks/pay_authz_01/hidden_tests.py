"""Hidden tests for pay_authz_01: tampering, wrong secret, replay, and bad-signature semantics."""

import pytest

from payments import storage, verify

SECRET = "whsec_test_hidden"


@pytest.fixture(autouse=True)
def _reset():
    storage.reset()
    yield
    storage.reset()


def test_amount_tampering_raises_and_creates_no_invoice():
    # Signature is computed for amount 1000 but the call claims amount 9999.
    sig = verify.expected_signature("e1", 1000, SECRET)
    with pytest.raises(PermissionError):
        verify.process_signed_webhook("e1", 9999, sig, SECRET)
    assert storage.count_for_event("e1") == 0


def test_wrong_secret_raises_and_creates_no_invoice():
    sig = verify.expected_signature("e1", 1000, "the_wrong_secret")
    with pytest.raises(PermissionError):
        verify.process_signed_webhook("e1", 1000, sig, SECRET)
    assert storage.count_for_event("e1") == 0


def test_valid_signature_replay_is_idempotent():
    sig = verify.expected_signature("e1", 1000, SECRET)
    first = verify.process_signed_webhook("e1", 1000, sig, SECRET)
    second = verify.process_signed_webhook("e1", 1000, sig, SECRET)
    assert second is first
    assert storage.count_for_event("e1") == 1


def test_verify_signature_returns_false_for_bad_signature():
    # A bad signature yields False, not an exception.
    result = verify.verify_signature("e1", 1000, "not_a_real_signature", SECRET)
    assert result is False


def test_verify_signature_returns_true_for_good_signature():
    sig = verify.expected_signature("e1", 1000, SECRET)
    assert verify.verify_signature("e1", 1000, sig, SECRET) is True
