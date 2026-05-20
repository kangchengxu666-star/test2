"""Tests for linux_learn game challenges."""

from src.linux_learn.game import CHALLENGES, _run, _setup


def run_challenge(ch_id: int, cmd: str):
    ch = next(c for c in CHALLENGES if c.id == ch_id)
    cwd = _setup(ch)
    stdout, stderr, rc = _run(cmd, cwd)
    passed = ch.check(cmd, stdout, rc, cwd)
    return passed, stdout, cwd


def test_ch01_pwd():
    passed, _, _ = run_challenge(1, "pwd")
    assert passed


def test_ch02_ls():
    passed, out, _ = run_challenge(2, "ls")
    assert passed
    assert "apple.txt" in out


def test_ch03_ls_la():
    passed, out, _ = run_challenge(3, "ls -la")
    assert passed
    assert ".hidden_config" in out


def test_ch04_cd():
    passed, _, _ = run_challenge(4, "cd workspace")
    assert passed


def test_ch05_mkdir():
    passed, _, cwd = run_challenge(5, "mkdir projects")
    assert passed
    assert (cwd / "projects").is_dir()


def test_ch06_touch():
    passed, _, cwd = run_challenge(6, "touch notes.txt")
    assert passed
    assert (cwd / "notes.txt").exists()


def test_ch07_echo_redirect():
    passed, _, cwd = run_challenge(7, "echo 'Hello WSL' > hello.txt")
    assert passed
    assert "Hello WSL" in (cwd / "hello.txt").read_text()


def test_ch08_cp():
    passed, _, cwd = run_challenge(8, "cp original.txt backup.txt")
    assert passed
    assert (cwd / "backup.txt").exists()
    assert (cwd / "original.txt").exists()


def test_ch09_mv():
    passed, _, cwd = run_challenge(9, "mv old_name.txt new_name.txt")
    assert passed
    assert (cwd / "new_name.txt").exists()
    assert not (cwd / "old_name.txt").exists()


def test_ch10_rm():
    passed, _, cwd = run_challenge(10, "rm trash.txt")
    assert passed
    assert not (cwd / "trash.txt").exists()


def test_ch11_cat():
    passed, out, _ = run_challenge(11, "cat message.txt")
    assert passed
    assert "WSL" in out


def test_ch12_head():
    passed, out, _ = run_challenge(12, "head -n 3 big.txt")
    assert passed
    assert "line 1" in out
    assert "line 4" not in out


def test_ch13_grep():
    passed, out, _ = run_challenge(13, "grep ERROR server.log")
    assert passed
    assert "ERROR" in out


def test_ch14_find():
    passed, out, _ = run_challenge(14, "find . -name config.json")
    assert passed
    assert "config.json" in out


def test_ch15_pipe_wc():
    passed, out, _ = run_challenge(15, "cat names.txt | wc -l")
    assert passed
    assert "5" in out
