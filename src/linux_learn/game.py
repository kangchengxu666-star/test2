"""WSL 基础命令闯关游戏。"""

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

SANDBOX = Path("/tmp/wsl-learn")

BANNER = """
╔══════════════════════════════════════════════════╗
║          WSL 基础命令闯关练习                    ║
║                                                  ║
║  每关都有一个目标，在沙盒目录里完成它。          ║
║  hint  → 查看提示                               ║
║  skip  → 跳过当前关卡                           ║
║  quit  → 退出游戏                               ║
╚══════════════════════════════════════════════════╝
"""

CATEGORIES = {
    "导航": "🧭",
    "文件操作": "📁",
    "查看内容": "📄",
    "搜索": "🔍",
    "组合技": "⚡",
}


@dataclass
class Challenge:
    id: int
    category: str
    title: str
    goal: str
    hint: str
    setup: list[str]
    # (cmd_typed, stdout, returncode, sandbox_cwd) -> bool
    check: Callable[[str, str, int, Path], bool]
    explain: str


def _run(cmd: str, cwd: Path) -> tuple[str, str, int]:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=str(cwd))
    return r.stdout, r.stderr, r.returncode


def _setup(ch: Challenge) -> Path:
    cwd = SANDBOX / f"ch{ch.id:02d}"
    if cwd.exists():
        shutil.rmtree(cwd)
    cwd.mkdir(parents=True)
    for cmd in ch.setup:
        _run(cmd, cwd)
    return cwd


CHALLENGES: list[Challenge] = [
    # ── 导航 ─────────────────────────────────────────────────────────
    Challenge(
        id=1,
        category="导航",
        title="查看当前路径",
        goal="显示你当前所在的完整目录路径",
        hint="pwd",
        setup=[],
        check=lambda cmd, out, rc, cwd: "pwd" in cmd and rc == 0 and str(cwd) in out,
        explain="pwd = Print Working Directory，随时可以用它确认自己在哪里。",
    ),
    Challenge(
        id=2,
        category="导航",
        title="列出文件",
        goal="列出当前目录里的所有文件（里面有 apple.txt、banana.txt、cherry.txt）",
        hint="ls",
        setup=["touch apple.txt banana.txt cherry.txt"],
        check=lambda cmd, out, rc, cwd: rc == 0 and "apple.txt" in out,
        explain="ls = list，最常用的命令之一，快速查看目录内容。",
    ),
    Challenge(
        id=3,
        category="导航",
        title="列出隐藏文件",
        goal="列出所有文件，包括以 . 开头的隐藏文件，并显示详细信息",
        hint="ls -la",
        setup=["touch visible.txt .hidden_config"],
        check=lambda cmd, out, rc, cwd: rc == 0 and ".hidden_config" in out,
        explain="ls -la：-l = 详细格式（权限/大小/时间），-a = 显示隐藏文件（all）。",
    ),
    Challenge(
        id=4,
        category="导航",
        title="进入目录",
        goal="进入已有的 workspace 目录",
        hint="cd workspace",
        setup=["mkdir workspace"],
        check=lambda cmd, out, rc, cwd: bool(re.match(r"cd\s+workspace", cmd.strip())),
        explain="cd = Change Directory。cd .. 返回上一层，cd ~ 回到家目录，cd - 回到上次目录。",
    ),
    # ── 文件操作 ─────────────────────────────────────────────────────
    Challenge(
        id=5,
        category="文件操作",
        title="创建目录",
        goal="创建一个名为 projects 的新目录",
        hint="mkdir projects",
        setup=[],
        check=lambda cmd, out, rc, cwd: (cwd / "projects").is_dir(),
        explain="mkdir = Make Directory。mkdir -p a/b/c 可以一次创建多层嵌套目录。",
    ),
    Challenge(
        id=6,
        category="文件操作",
        title="创建空文件",
        goal="创建一个名为 notes.txt 的空文件",
        hint="touch notes.txt",
        setup=[],
        check=lambda cmd, out, rc, cwd: (cwd / "notes.txt").exists(),
        explain="touch 用于创建空文件，也可更新已有文件的访问/修改时间戳。",
    ),
    Challenge(
        id=7,
        category="文件操作",
        title="写入文件",
        goal='把文字 "Hello WSL" 写入 hello.txt 文件',
        hint="echo 'Hello WSL' > hello.txt",
        setup=[],
        check=lambda cmd, out, rc, cwd: (
            (cwd / "hello.txt").exists()
            and "Hello WSL" in (cwd / "hello.txt").read_text()
        ),
        explain="> 是重定向符，把命令输出写入文件（会覆盖）。>> 是追加，不会覆盖已有内容。",
    ),
    Challenge(
        id=8,
        category="文件操作",
        title="复制文件",
        goal="把 original.txt 复制一份，命名为 backup.txt",
        hint="cp original.txt backup.txt",
        setup=["echo 'important data' > original.txt"],
        check=lambda cmd, out, rc, cwd: (
            (cwd / "backup.txt").exists() and (cwd / "original.txt").exists()
        ),
        explain="cp = copy。cp -r src/ dst/ 复制整个目录（r = recursive）。",
    ),
    Challenge(
        id=9,
        category="文件操作",
        title="重命名文件",
        goal="把 old_name.txt 重命名为 new_name.txt",
        hint="mv old_name.txt new_name.txt",
        setup=["touch old_name.txt"],
        check=lambda cmd, out, rc, cwd: (
            (cwd / "new_name.txt").exists() and not (cwd / "old_name.txt").exists()
        ),
        explain="mv = move，既可移动文件到其他目录，也可用来重命名。",
    ),
    Challenge(
        id=10,
        category="文件操作",
        title="删除文件",
        goal="删除 trash.txt 文件",
        hint="rm trash.txt",
        setup=["touch trash.txt"],
        check=lambda cmd, out, rc, cwd: not (cwd / "trash.txt").exists(),
        explain="rm = remove。⚠ Linux 没有回收站，rm 删了就没了！rm -r 删目录。",
    ),
    # ── 查看内容 ─────────────────────────────────────────────────────
    Challenge(
        id=11,
        category="查看内容",
        title="查看文件内容",
        goal="查看 message.txt 的全部内容",
        hint="cat message.txt",
        setup=["echo 'WSL bridges Windows and Linux!' > message.txt"],
        check=lambda cmd, out, rc, cwd: rc == 0 and "WSL" in out,
        explain="cat = concatenate，最简单的查看文件命令。内容多时用 less 翻页更方便。",
    ),
    Challenge(
        id=12,
        category="查看内容",
        title="查看文件前几行",
        goal="只查看 big.txt 的前 3 行（文件共 20 行）",
        hint="head -n 3 big.txt",
        setup=['for i in $(seq 1 20); do echo "line $i" >> big.txt; done'],
        check=lambda cmd, out, rc, cwd: (
            rc == 0 and "head" in cmd and "line 1" in out and "line 4" not in out
        ),
        explain="head 看开头，tail 看末尾。tail -f 可实时追踪不断增长的日志文件。",
    ),
    # ── 搜索 ─────────────────────────────────────────────────────────
    Challenge(
        id=13,
        category="搜索",
        title="搜索文件内容",
        goal="在 server.log 里找出包含 ERROR 的所有行",
        hint="grep ERROR server.log",
        setup=[
            "echo 'INFO: server started' > server.log",
            "echo 'ERROR: connection refused' >> server.log",
            "echo 'INFO: request received' >> server.log",
            "echo 'ERROR: timeout exceeded' >> server.log",
        ],
        check=lambda cmd, out, rc, cwd: rc == 0 and "ERROR" in out,
        explain="grep 是强大的文本搜索工具。grep -i 忽略大小写，grep -n 显示行号，grep -r 递归搜索目录。",
    ),
    Challenge(
        id=14,
        category="搜索",
        title="查找文件",
        goal="在当前目录（含子目录）下找到名为 config.json 的文件",
        hint="find . -name config.json",
        setup=["mkdir -p app/settings", "touch app/settings/config.json"],
        check=lambda cmd, out, rc, cwd: rc == 0 and "config.json" in out,
        explain="find . 从当前目录开始搜索。-name '*.txt' 支持通配符，-type f 只找文件，-type d 只找目录。",
    ),
    # ── 组合技 ─────────────────────────────────────────────────────
    Challenge(
        id=15,
        category="组合技",
        title="管道：统计行数",
        goal="用管道（|）统计 names.txt 里有几个名字（每行一个）",
        hint="cat names.txt | wc -l",
        setup=["printf 'Alice\\nBob\\nCharlie\\nDave\\nEve\\n' > names.txt"],
        check=lambda cmd, out, rc, cwd: rc == 0 and "|" in cmd and "5" in out,
        explain="| 是管道，把左边命令的输出直接传给右边命令处理。wc -l 统计行数。这是 Linux 命令行最强大的特性之一！",
    ),
]


def main() -> None:
    SANDBOX.mkdir(exist_ok=True)
    print(BANNER)

    total = len(CHALLENGES)
    score = 0

    for i, ch in enumerate(CHALLENGES):
        cwd = _setup(ch)
        icon = CATEGORIES.get(ch.category, "•")

        print(f"\n{'─' * 52}")
        print(f"  关卡 {i + 1:02d}/{total}  {icon} {ch.category}  ·  {ch.title}")
        print(f"  目标：{ch.goal}")
        print(f"  沙盒：{cwd}")
        print()

        attempts = 0
        passed = False

        while not passed:
            try:
                cmd = input("  $ ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n已退出")
                return

            if not cmd:
                continue

            if cmd == "quit":
                print(f"\n已退出。当前得分：{score}/{i}")
                return

            if cmd == "hint":
                print(f"  提示：{ch.hint}")
                continue

            if cmd == "skip":
                print("  已跳过")
                break

            stdout, stderr, rc = _run(cmd, cwd)

            if stdout:
                # indent output for readability
                for line in stdout.splitlines():
                    print(f"  {line}")
            if stderr:
                for line in stderr.splitlines():
                    print(f"  {line}")

            if ch.check(cmd, stdout, rc, cwd):
                score += 1
                passed = True
                print(f"\n  ✓ 完成！{ch.explain}")
            else:
                attempts += 1
                if attempts >= 2:
                    print("  （输入 hint 查看提示，skip 跳过本关）")

    print(f"\n{'═' * 52}")
    print(f"  全部完成！最终得分：{score}/{total}")
    if score == total:
        print("  满分！你已掌握 WSL 基础命令，太棒了！")
    elif score >= total * 0.8:
        print("  很棒！多练练剩余的命令，就能完全掌握。")
    else:
        print("  继续加油！可以重新运行再练一遍。")
    print()
