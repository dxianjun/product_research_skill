import test from "node:test";
import assert from "node:assert/strict";
import { generateResearchReport } from "../skill.js";

test("generate report should include required sections", () => {
  const report = generateResearchReport({
    productQuestion: "How should we monitor competitor strategy for Amazon batteries?",
    marketScope: ["Amazon US", "Batteries"],
    userScope: ["Category manager", "Ops analyst"],
    competitorScope: ["BrandA", "BrandB"],
    constraints: ["Daily refresh", "Low ops overhead"],
    findings: [
      { confidence: "fact", statement: "BrandA increased coupon frequency in 2 weeks." },
      { confidence: "assumption", statement: "BrandB may be testing aggressive launch pricing." }
    ],
    options: [
      {
        name: "Alert-first monitoring",
        pros: ["Fast reaction"],
        cons: ["Can be noisy"]
      }
    ],
    recommendation: "Use alert-first for P1/P2 events and weekly trend reports for strategy updates.",
    risks: ["Data source interruptions"],
    nextExperiments: ["A/B threshold on coupon-change alerts"]
  });

  assert.match(report, /## 1\. Research Question/);
  assert.match(report, /## 2\. Key Findings/);
  assert.match(report, /## 4\. Options and Tradeoffs/);
  assert.match(report, /## 7\. Next Experiments/);
  assert.match(report, /\[FACT\]/);
  assert.match(report, /\[ASSUMPTION\]/);
});
