# AGENTS.md

## 项目概览

Python 项目，使用 uv 管理依赖，ruff 统一代码风格，pytest 做测试，gh 管理 PR 流程。

---

## 环境与命令

所有命令必须按以下方式运行，不得偏离：

```bash
uv sync                        # 同步依赖（每次开始前运行）
uv add <包名>                   # 添加新依赖
uv run python <文件>            # 运行脚本
uv run pytest -q               # 运行所有测试
uv run pytest tests/test_x.py  # 运行指定测试文件
uvx ruff format .              # 格式化代码
uvx ruff check .               # 检查语法问题
```

---

## 代码风格

- Python 3.12+
- 缩进：4 个空格
- 行宽：最长 88 字符
- 字符串：优先使用双引号
- 变量名：有意义的英文单词，不用 `a`、`tmp`、`data`
- 函数：单一职责，一个函数只做一件事
- 复杂逻辑必须加注释

### 示例风格

```python
# 好的
def calculate_user_score(user_id: int, multiplier: float = 1.0) -> float:
    """Calculate the score for a given user."""
    base_score = fetch_base_score(user_id)
    return base_score * multiplier

# 不好的
def calc(x, m=1.0):
    s = get(x)
    return s * m
```

---

## 测试规范

- 新功能必须有对应测试
- 测试文件放在 `tests/` 目录，命名为 `test_<模块名>.py`
- 每次提交前必须通过：`uv run pytest -q`
- 测试必须覆盖：正常路径、边界值、异常情况

```python
# 测试示例
def test_calculate_user_score_normal():
    assert calculate_user_score(1) == 100.0

def test_calculate_user_score_with_multiplier():
    assert calculate_user_score(1, 2.0) == 200.0

def test_calculate_user_score_invalid_user():
    with pytest.raises(ValueError):
        calculate_user_score(-1)
```

---

## Git 提交规范

提交信息格式：`type: 简短描述`

```
feat: 新功能
fix: 修复 bug
test: 添加或修改测试
refactor: 重构（不改功能）
docs: 文档更新
chore: 杂项（依赖更新等）
```

每个 commit 只做一件事，不要把多个不相关的改动混在一起。

---

## PR 规范

- 标题格式：`type: 简短描述`
- Body 必须包含：做了什么 / 为什么这么做 / 如何验证
- 关联 Issue：`Closes #N`
- 所有 CI 检查通过才能 merge
- 不在 `main` 分支直接开发

---

## 禁止事项

- 不提交 `.env` 文件或任何密钥、token
- 不用 `sudo` 安装 Python 包（用 uv）
- 不忽略 CI 失败强行 merge
- 不修改 `uv.lock`（由 uv 自动管理）
- 不删除已有测试
- 不在没有测试的情况下提交新功能

---

## 完成任务的标准

每次任务完成前，必须确认以下全部通过：

- [ ] `uv run pytest -q` 全绿
- [ ] `uvx ruff check .` 无报错
- [ ] `uvx ruff format --check .` 无差异
- [ ] 新逻辑已有对应测试覆盖
- [ ] 没有提交敏感文件
