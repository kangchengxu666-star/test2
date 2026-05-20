# AI Agent 工作流规范

## Agent 是什么

Agent 是能够**自主规划、执行多步骤任务**的 AI。
区别于普通对话 AI，Agent 可以：
- 读写文件
- 执行终端命令
- 调用工具和 API
- 根据结果调整下一步行动

---

## 工作流模型

```
任务输入
   │
   ▼
┌─────────────────┐
│   理解 & 规划    │  ← 分析任务，拆解步骤
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   执行 & 观察    │  ← 调用工具，观察结果
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   验证 & 反思    │  ← 结果是否符合预期？
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   成功      失败
    │         │
    ▼         ▼
  输出      重新规划
```

---

## Claude Code 作为 Agent

### 启动方式
```bash
cd ~/your-project
claude                    # 交互模式
claude "完成 issue #5"    # 直接给任务
claude --bg "任务描述"    # 后台运行
```

### 任务描述模板
```
目标：[要实现什么]
背景：[相关上下文，比如哪个文件、哪个函数]
约束：[不能改什么、必须兼容什么]
验证：[怎么确认完成了，比如测试通过、输出什么结果]
```

### 示例
```
目标：为 router.py 添加 /health 端点
背景：参考现有的 /status 端点实现风格
约束：不修改现有端点，保持向后兼容
验证：uv run pytest tests/test_router.py -q 全部通过
```

---

## Codex 作为 Agent

### 启动方式
```bash
cd ~/your-project
codex                     # 交互模式
codex "重构这个函数"      # 直接给任务
```

### 适合场景
- 大型代码库的重构
- 跨文件的一致性修改
- 生成测试用例
- 代码解释和文档生成

---

## Claude Code vs Codex 分工建议

| 任务类型 | 推荐工具 |
|---------|---------|
| 新功能开发 | Claude Code |
| 代码重构 | Codex |
| 写测试 | Claude Code |
| 代码审查 | Claude Code（有 claude-review workflow）|
| 大规模文件修改 | Codex |
| 调试 bug | Claude Code |
| 生成文档 | 两者均可 |

---

## Agent 使用原则

### 1. 任务要具体
- ❌ "优化代码"
- ✅ "优化 main.py 里 process_data 函数的性能，目标是减少内存占用"

### 2. 给足上下文
- 告诉 Agent 项目用什么框架
- 说明代码风格要求（参考 CLAUDE.md）
- 提供相关文件路径

### 3. 验证结果
- Agent 完成后自己跑一遍测试
- 阅读改动的 diff，理解每处修改
- 不盲目信任 Agent 的输出

### 4. 迭代而非一次性
- 复杂任务拆成多个小任务
- 每步确认正确后再进行下一步
- 出错时告诉 Agent 哪里不对，让它修正

### 5. 保持人在回路
- Agent 是加速器，不是替代品
- 重要决策由你来做
- PR merge 前自己 review 一遍

---

## 常用 Agent 工作流

### 功能开发流
```bash
# 1. 创建分支
git checkout -b feature/xxx

# 2. 让 Claude Code 实现功能
claude "实现 xxx 功能，参考 CLAUDE.md 的规范"

# 3. 验证
uv run pytest -q
uvx ruff format . && uvx ruff check .

# 4. 提交 PR
git add . && git commit -m "feat: xxx"
git push origin feature/xxx
gh pr create
```

### Bug 修复流
```bash
# 1. 创建分支
git checkout -b fix/xxx

# 2. 让 Claude Code 定位和修复
claude "这个错误是什么原因：[粘贴报错信息]，帮我修复"

# 3. 验证修复
uv run pytest -q

# 4. 提交
git add . && git commit -m "fix: xxx"
git push && gh pr create
```

### 代码审查流
```bash
# 提 PR 后 GitHub Actions 自动触发 claude-review
# 也可以手动让 Claude Code 审查
claude "审查当前分支相对 main 的所有改动"
```

---

## 注意事项

- Agent 有时会过度修改，用 `git diff` 确认改动范围
- 不要让 Agent 接触 `.env` 和密钥文件
- 长任务用 `--bg` 后台模式，避免超时
- Agent 输出的代码要通过 CI 才算完成
