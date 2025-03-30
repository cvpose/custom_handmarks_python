from custom_landmarks.virtual_enum import VirtualEnumRef

def test_virtual_enum_ref_int():
    ref = VirtualEnumRef(42)
    assert int(ref) == 42

def test_virtual_enum_ref_repr():
    ref = VirtualEnumRef(7)
    assert repr(ref) == "<VirtualLandmark value=7>"