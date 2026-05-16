---
name: product-research-skill-ts
description: TypeScript implementation of product research skill, used to output structured research reports for competitor analysis, market monitoring, and sentiment tracking.
version: 0.1.0
language: zh-CN
author: dxianjun
tags:
  - product-research
  - typescript
  - amazon
---

# Product Research Skill TS

## Purpose

Generate a structured product research report from input JSON.

## Output Sections

1. Research Question
2. Key Findings
3. Scope
4. Options and Tradeoffs
5. Recommendation
6. Risks and Unknowns
7. Next Experiments

## Run

```bash
npm install
npm run build
node dist/cli.js examples/sample-input.json
```
