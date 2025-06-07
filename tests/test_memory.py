# tests/test_memory.py
from memory_manager import load_memory, save_memory

def test_save_and_load_memory(tmp_path):
    test_file = tmp_path / "test.json"
    context = "Namamu Vintec.\n"
    history = [{"user": "halo", "Vintec": "hai"}]

    save_memory(context, history, filename=str(test_file))
    loaded_context, loaded_history = load_memory(filename=str(test_file))

    assert loaded_context == context
    assert loaded_history == history
