# Claude Code Guidelines (Karpathy-Inspired)

## 核心哲学

> "The best code is the code that doesn't need to be written." — 能用简单方案解决的问题，不要过度设计。

Claude Code 是你的结对编程伙伴，不是自动化机器。你负责方向和判断，它负责执行和加速。

---

## 工作原则

### 1. 先理解，再动手
- 拿到任务先读懂现有代码，不要急着写
- 用 `find`、`grep`、`cat` 探索项目结构
- 不确定的地方先问，不要猜

### 2. 小步快跑
- 每次改动尽量小而聚焦，一个 commit 只做一件事
- 改完立刻跑测试，不要积累大量未验证的改动
- 宁可多提几个小 PR，不要一个巨型 PR

### 3. 测试驱动
- 新功能必须有对应测试
- 跑测试命令：`uv run pytest -q`
- 格式检查：`uvx ruff format . && uvx ruff check .`
- 所有检查通过才能提交

### 4. 不要过度设计
- 先让代码跑起来，再考虑优化
- 避免提前抽象，等真正需要复用时再重构
- YAGNI 原则：You Aren't Gonna Need It

### 5. 保持代码可读
- 变量名要有意义，不用 `a`、`tmp`、`data` 这种
- 函数单一职责，一个函数只做一件事
- 复杂逻辑必须加注释

---

## 项目规范

### Python 环境
```bash
uv sync                  # 同步依赖
uv add <包名>            # 添加依赖
uv run python <文件>     # 运行脚本
uvx ruff format .        # 格式化代码
uvx ruff check .         # 语法检查
```

### Git 提交规范
```
feat: 新功能
fix: 修复 bug
test: 添加或修改测试
refactor: 重构（不改功能）
docs: 文档更新
chore: 杂项（依赖更新等）
```

### PR 规范
- 标题格式：`type: 简短描述`
- Body 包含：做了什么、为什么这么做、如何测试
- 所有 CI 检查通过才能 merge
- 关联对应的 Issue：`Closes #N`

---

## Claude Code 使用技巧

### 给任务加上下文
```
# 好的方式
"在 src/auth.py 的 login 函数里，
添加对空密码的校验，参考现有的 validate_email 函数风格"

# 不好的方式
"添加密码校验"
```

### 让 Claude 先解释再执行
```
"先解释你打算怎么改，我确认后再动手"
```

### 遇到 bug 时
```
"这个错误是什么原因，有哪几种可能的解法，各有什么优缺点"
```

### 代码审查
```
"审查这段代码，找出潜在问题和改进点"
```

---

## 禁止事项

- 不直接在 `main` 分支上开发
- 不提交未通过测试的代码
- 不提交 `.env` 文件或任何密钥
- 不用 `sudo` 安装 Python 包（用 uv）
- 不忽略 CI 失败强行 merge

---

## 每次开发前的 checklist

- [ ] 拉取最新代码：`git pull origin main`
- [ ] 创建新分支：`git checkout -b feature/xxx`
- [ ] 同步依赖：`uv sync`
- [ ] 开发完跑测试：`uv run pytest -q`
- [ ] 格式化代码：`uvx ruff format .`
- [ ] 提交并推送：`git add . && git commit -m "..." && git push`
- [ ] 创建 PR：`gh pr create`
