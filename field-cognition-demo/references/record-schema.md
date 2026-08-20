# `/后台记录` 记录契约

## 查询方式

- `/后台记录`：默认显示当前会话最近 5 条事件；只有 1 条时直接展开详情。
- `/后台记录 CAL-0001`：显示指定事件。
- `/后台记录 当前画板`：只显示与当前已选画板同名或同 ID 的事件。

从当前会话先前回复中的 `FIELD_COGNITION_EVENT` HTML 注释读取事件。不要调用不存在的数据库。如果注释不可见但存在前台回执，重建最小记录并标记 `record_integrity: partial`。

## 规范事件 JSON

每个事件至少包含：

```json
{
  "schema_version": "0.1",
  "event_id": "CAL-0001",
  "persistence": "session-only",
  "record_integrity": "complete",
  "created_at": null,
  "actor": {
    "erp": null,
    "display_name": null
  },
  "context": {
    "file_name": null,
    "request_name": null,
    "frame_id": null,
    "frame_name": null
  },
  "rule_chain": {
    "id": "RC-CHILD-001",
    "version": "0.1",
    "title": "换购子品保留与资格恢复"
  },
  "question": "取消勾选主品后，已经保存的换购子品，其换购价和结算资格分别如何变化？",
  "raw_response": "用户原始回答",
  "source_refs": ["SRC-CHILD-001"],
  "claim_changes": [
    {
      "claim_id": "EX-CHILD-004",
      "operation": "update",
      "before": {
        "statement": "主品取消勾选后，子品换购价是否继续有效",
        "status": "unknown"
      },
      "after": {
        "statement": "仅在用户明确回答后填写",
        "status": "local-candidate",
        "scope": "current-request"
      },
      "support": "user-calibration"
    }
  ],
  "unresolved": [],
  "conflicts": [],
  "inference_notes": [],
  "promotion": {
    "result": "not-promoted",
    "reason": "一次局部校准不能晋升为场域事实"
  }
}
```

没有真实时间或 ERP 时保留 `null`，不能伪造。没有主张变化时，`claim_changes` 使用空数组。

## 后台列表视图

```markdown
### 后台记录 · 会话级演示

> 尚未连接正式后台；以下记录来自当前对话。

| 事件 | 画板 | 规则链 | 结果 | 模型影响 |
| --- | --- | --- | --- | --- |
| CAL-0001 | ... | ... | 已拆分 2 条候选主张 | 未晋升 |
```

## 事件详情视图

详情必须让项目负责人快速回答“人说了什么、系统学成了什么、还有什么不知道”：

```markdown
### CAL-0001 · 校准事件

**上下文**
- 文件：...
- 画板：...
- 操作者：未提供
- 记录状态：会话级演示

**前台当时询问**
> ...

**用户原始回答**
> ...

**系统转译与主张差异**
| 主张 | 校准前 | 校准后 | 范围 |
| --- | --- | --- | --- |
| EX-... | unknown | ... | 当前需求 |

**仍待确认**
- ...

**推断与冲突**
- 没有则明确写“无”；有则逐条说明，不能隐藏。

**模型结果**
- 局部候选认知；未晋升为场域规则。
```

不要展示整个知识图谱。用户要求“原始记录”时，才额外展示规范事件 JSON。

## 晋升规则

后台只能显示晋升结果，不能因为次数自动晋升。至少需要同时具备明确适用范围、更高权威证据或多次独立复用、没有未解决冲突，才可能由后续正式系统评估。本演示技能始终输出 `not-promoted`。
