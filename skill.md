---
name: product-research-skill
description: 面向跨境电商（重点 Amazon）的产品研究技能。用于持续追踪竞品策略、产品变化、营销动态和舆情，并输出可执行的分析结论与下一步实验建议。
version: 1.0.0
language: zh-CN
author: dxianjun
tags:
  - product-research
  - competitor-analysis
  - market-monitoring
  - amazon
---

# Product Research Skill（小龙虾安装版）

## 技能目标

将输入问题转化为结构化研究输出，覆盖：
1. 竞品分析
2. 市场监控
3. 舆情洞察
4. 策略建议与验证计划

## 适用场景

- 用户要求做产品调研、竞品对比、市场扫描
- 用户要评估机会点、风险点、策略动作
- 用户要形成可用于业务评审/复盘的报告

## 工作流

1. 用一句话重述研究问题（Research Question）。
2. 明确范围（Scope）：
   - 市场范围（站点/类目/价格带）
   - 用户范围（目标人群/购买动机）
   - 竞品范围（核心竞品/腰部竞品）
   - 约束条件（时效、成本、数据可得性）
3. 汇总证据并区分：
   - `FACT`：有明确数据或来源支撑
   - `ASSUMPTION`：待验证判断
4. 输出可选方案并给出权衡（tradeoff）：
   - 优势（Pros）
   - 劣势（Cons）
5. 给出推荐方案（Recommendation）：
   - 为什么选它
   - 适用前提
   - 不适用边界
6. 输出风险与未知项（Risks and Unknowns）。
7. 输出下一步实验（Next Experiments）：
   - 可执行
   - 可验证
   - 有时间窗口

## 输出格式（必须遵守）

按以下结构输出：

1. Research Question  
2. Key Findings  
3. Scope  
4. Options and Tradeoffs  
5. Recommendation  
6. Risks and Unknowns  
7. Next Experiments

## 质量规则

- 优先使用一手来源或高可信来源。
- 不确定信息必须标记为 `ASSUMPTION`。
- 结论必须可执行、可验证，避免空泛建议。
- 输出中至少给出 2 条可落地实验建议。
