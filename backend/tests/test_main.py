from main import is_prime


def test_is_prime():
    assert is_prime(7)
    assert not is_prime(8)
