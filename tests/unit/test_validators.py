"""
Unit tests for input, audio, and image validation utilities.
"""

import pytest
import io
import numpy as np
from PIL import Image

from src.validators.input_validators import (
    validate_username,
    validate_password,
    validate_subject_inputs,
    sanitize_string
)
from src.validators.audio_validators import validate_audio_payload
from src.validators.image_validators import validate_and_prepare_image

class TestInputValidators:
    def test_validate_username_valid(self):
        valid, msg = validate_username("prof_smith")
        assert valid is True
        assert msg == ""

    def test_validate_username_invalid_chars(self):
        valid, msg = validate_username("prof@smith!")
        assert valid is False
        assert "only contain" in msg

    def test_validate_username_too_short(self):
        valid, msg = validate_username("ab")
        assert valid is False
        assert "between 3 and 30" in msg

    def test_validate_username_empty(self):
        valid, msg = validate_username("")
        assert valid is False
        assert "required" in msg

    def test_validate_password_strong(self):
        valid, msg = validate_password("SecurePass123")
        assert valid is True
        assert msg == ""

    def test_validate_password_too_short(self):
        valid, msg = validate_password("Short1")
        assert valid is False
        assert "at least 8" in msg

    def test_validate_password_missing_number(self):
        valid, msg = validate_password("NoNumberPass")
        assert valid is False
        assert "number" in msg

    def test_validate_password_missing_uppercase(self):
        valid, msg = validate_password("lowercase123")
        assert valid is False
        assert "uppercase" in msg

    def test_validate_subject_inputs_valid(self):
        valid, msg = validate_subject_inputs("CS101", "Computer Science", "Sec A")
        assert valid is True

    def test_validate_subject_inputs_missing_code(self):
        valid, msg = validate_subject_inputs("", "Computer Science", "Sec A")
        assert valid is False
        assert "code is required" in msg

    def test_validate_subject_inputs_invalid_code(self):
        valid, msg = validate_subject_inputs("CS 101!", "Computer Science", "Sec A")
        assert valid is False

    def test_sanitize_string(self):
        assert sanitize_string("  hello world  ") == "hello world"
        assert sanitize_string(None) == ""

class TestAudioValidators:
    def test_empty_audio_payload(self):
        valid, err, dur = validate_audio_payload(b"")
        assert valid is False
        assert "empty" in err.lower()
        assert dur is None

    def test_none_audio_payload(self):
        valid, err, dur = validate_audio_payload(None)
        assert valid is False
        assert "no audio data" in err.lower()

    def test_oversized_audio_payload(self):
        huge_bytes = b"0" * (11 * 1024 * 1024)
        valid, err, dur = validate_audio_payload(huge_bytes)
        assert valid is False
        assert "exceeds maximum" in err

class TestImageValidators:
    def test_none_image(self):
        valid, err, arr = validate_and_prepare_image(None)
        assert valid is False
        assert arr is None

    def test_tiny_image(self):
        tiny = Image.new("RGB", (10, 10))
        valid, err, arr = validate_and_prepare_image(tiny)
        assert valid is False
        assert "too low" in err

    def test_valid_image(self):
        img = Image.new("RGB", (200, 200), color=(100, 150, 200))
        valid, err, arr = validate_and_prepare_image(img)
        assert valid is True
        assert arr is not None
        assert arr.shape == (200, 200, 3)

    def test_oversized_image_downscaled(self):
        # 3000 x 2000 image should be scaled to max 1920
        large_img = Image.new("RGB", (3000, 2000), color="white")
        valid, err, arr = validate_and_prepare_image(large_img)
        assert valid is True
        assert max(arr.shape[0], arr.shape[1]) <= 1920
