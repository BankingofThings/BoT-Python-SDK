from bot_python_sdk.key_generator import KeyGenerator


def test_generate_uuid():
    uuid = KeyGenerator().generate_uuid()
    assert isinstance(s, str)
