"""Tests for checkpoint path management and JSON persistence."""

import json
from pathlib import Path
import shutil
import tempfile

import pytest

from kaiwu.common import CheckpointManager


class SerializableState:
    """Minimal object that matches CheckpointManager.dump's protocol."""

    def __init__(self, value):
        self.value = value

    def to_json_dict(self):
        return {"value": self.value}


@pytest.fixture
def checkpoint_dir():
    # Use a workspace-local temp root to avoid restricted system temp locations.
    tmp_root = Path.cwd() / ".tmp_test_checkpoints"
    tmp_root.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(dir=tmp_root) as directory:
            yield Path(directory)
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)


def test_checkpoint_manager_returns_none_when_save_dir_is_unset(monkeypatch):
    state = SerializableState(1)
    monkeypatch.setattr(CheckpointManager, "save_dir", None)

    assert CheckpointManager.load(state) is None
    assert CheckpointManager.dump(state) is None


def test_checkpoint_manager_generates_stable_paths_per_object(
    checkpoint_dir, monkeypatch
):
    # Reset class-level bookkeeping so generated identities are deterministic.
    monkeypatch.setattr(CheckpointManager, "save_dir", str(checkpoint_dir))
    monkeypatch.setattr(CheckpointManager, "_class_name_counter", {})
    monkeypatch.setattr(CheckpointManager, "_dict_obj_identity", {})
    first = SerializableState(1)
    second = SerializableState(2)

    first_path = CheckpointManager.get_path(first)
    second_path = CheckpointManager.get_path(second)

    assert first_path.endswith("SerializableState_1_checkpoint.json")
    assert second_path.endswith("SerializableState_2_checkpoint.json")
    assert CheckpointManager.get_path(first) == first_path


def test_checkpoint_manager_dump_and_load_round_trip(checkpoint_dir, monkeypatch):
    # Reset class-level bookkeeping so load uses the same identity as dump.
    monkeypatch.setattr(CheckpointManager, "save_dir", str(checkpoint_dir))
    monkeypatch.setattr(CheckpointManager, "_class_name_counter", {})
    monkeypatch.setattr(CheckpointManager, "_dict_obj_identity", {})
    state = SerializableState(7)

    CheckpointManager.dump(state)

    checkpoint_path = Path(CheckpointManager.get_path(state))
    assert json.loads(checkpoint_path.read_text(encoding="utf8")) == {"value": 7}
    assert CheckpointManager.load(state) == {"value": 7}
