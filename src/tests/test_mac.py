from optimized_mac.mac import OptimizedMAC


def test_optimized_mac():
    key = b'test_key'
    message = b'test_message'
    mac = OptimizedMAC(key)

    generated = mac.generate(message)
    assert mac.verify(message, generated), "MAC verification failed."
