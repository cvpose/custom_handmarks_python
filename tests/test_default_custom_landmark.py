import numpy as np
from custom_landmarks.default_custom_landmark import DefaultCustomLandmark
from custom_landmarks.landmark_ref import LandmarkRef


def test_default_custom_landmark_points(fake_landmarks):
    lm = DefaultCustomLandmark(fake_landmarks)

    assert isinstance(lm.LEFT_RIB, LandmarkRef)
    assert isinstance(tuple(lm.LEFT_RIB), tuple)

    assert isinstance(lm.MIDDLE_HIP, LandmarkRef)
    assert isinstance(tuple(lm.MIDDLE_HIP), tuple)

    assert isinstance(lm.RIGHT_RIB, LandmarkRef)
    assert isinstance(tuple(lm.RIGHT_RIB), tuple)

    assert isinstance(lm.MIDDLE_HIP, LandmarkRef)
    assert isinstance(tuple(lm.MIDDLE_HIP), tuple)

    assert isinstance(lm.MIDDLE_SHOULDER, LandmarkRef)
    assert isinstance(tuple(lm.MIDDLE_SHOULDER), tuple)

    assert isinstance(lm.THORAX, LandmarkRef)
    assert isinstance(tuple(lm.THORAX), tuple)

    # Check that the values make sense
    left_hip = fake_landmarks[lm._plm.LEFT_HIP.value]
    left_shoulder = fake_landmarks[lm._plm.LEFT_SHOULDER.value]

    expected_lrib = (
        np.array([left_hip.x, left_hip.y, left_hip.z])
        + np.array([left_shoulder.x, left_shoulder.y, left_shoulder.z])
    ) / 2

    # Força conversão segura para array numérico
    actual_lrib = np.array(tuple(lm.LEFT_RIB))

    assert np.allclose(actual_lrib, expected_lrib)


def test_custom_landmark_index_values(fake_landmarks):
    lm = DefaultCustomLandmark(fake_landmarks)

    assert isinstance(lm.LEFT_RIB.value, int)
    assert lm.LEFT_RIB.value == 33  # First virtual point
    assert lm.THORAX.value == 38  # Last of the 6 custom points
    assert len(lm) == 39  # 33 original + 6 custom
