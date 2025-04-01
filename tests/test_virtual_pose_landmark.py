import pytest
from types import SimpleNamespace

from custom_landmarks import VirtualPoseLandmark  # Substitua pelo caminho real, ex: custom_landmarks.virtual_pose_landmark

@pytest.fixture
def custom_vpl():
    vpl = VirtualPoseLandmark()
    # Limpa os dados e define um item de teste manualmente
    vpl.clear()
    vpl._reverse.clear()
    vpl["DUMMY"] = 99
    vpl._reverse[99] = "DUMMY"
    setattr(vpl, "DUMMY", 99)
    return vpl

# Cria todas as variações de teste
def test_add_success(custom_vpl):
    custom_vpl.add("NECK", 33)
    assert custom_vpl["NECK"] == 33
    assert custom_vpl._reverse[33] == "NECK"
    assert custom_vpl.NECK == 33

def test_add_invalid_name_type(custom_vpl):
    with pytest.raises(ValueError, match="must be a valid identifier string"):
        custom_vpl.add(123, 10)

def test_add_invalid_name_identifier(custom_vpl):
    with pytest.raises(ValueError, match="must be a valid identifier string"):
        custom_vpl.add("123INVALID", 10)

def test_add_duplicate_name(custom_vpl):
    custom_vpl.add("NECK", 33)
    with pytest.raises(ValueError, match="already defined"):
        custom_vpl.add("NECK", 34)

def test_add_duplicate_index(custom_vpl):
    custom_vpl.add("NECK", 33)
    with pytest.raises(ValueError, match="Index 33 is already used"):
        custom_vpl.add("THORAX", 33)

def test_getitem_with_string_key(custom_vpl):
    assert custom_vpl["DUMMY"] == 99

def test_getitem_with_integer_key(custom_vpl):
    assert custom_vpl[99] == "DUMMY"

def test_contains_string_key(custom_vpl):
    assert "DUMMY" in custom_vpl

def test_contains_integer_key(custom_vpl):
    assert 99 in custom_vpl

def test_getitem_invalid_string_raises(custom_vpl):
    with pytest.raises(KeyError):
        _ = custom_vpl["UNKNOWN"]

def test_getitem_invalid_integer_raises(custom_vpl):
    with pytest.raises(KeyError):
        _ = custom_vpl[123456]

def test_getattr_valid(custom_vpl):
    assert getattr(custom_vpl, "DUMMY") == 99

def test_getattr_invalid_raises(custom_vpl):
    with pytest.raises(AttributeError):
        _ = custom_vpl.NOT_EXISTS

def test_virtual_pose_landmark_repr():
    vpl = VirtualPoseLandmark()
    result = repr(vpl)

    assert isinstance(result, str)
    assert result.startswith("<VirtualPoseLandmark {")
    assert "NOSE" in result 