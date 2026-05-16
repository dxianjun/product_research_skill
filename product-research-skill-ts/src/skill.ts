import { ResearchInput } from "./types.js";

function lines(items: string[]): string {
  if (items.length === 0) {
    return "- (none)";
  }
  return items.map((item) => `- ${item}`).join("\n");
}

function findingsLines(
  findings: ResearchInput["findings"]
): string {
  if (findings.length === 0) {
    return "- (none)";
  }
  return findings
    .map((f) => `- [${f.confidence.toUpperCase()}] ${f.statement}`)
    .join("\n");
}

function optionsLines(options: ResearchInput["options"]): string {
  if (options.length === 0) {
    return "- (none)";
  }
  return options
    .map(
      (opt, idx) =>
        `${idx + 1}. ${opt.name}\n   - Pros: ${opt.pros.join("; ") || "(none)"}\n   - Cons: ${opt.cons.join("; ") || "(none)"}`
    )
    .join("\n");
}

export function generateResearchReport(input: ResearchInput): string {
  return [
    "## 1. Research Question",
    input.productQuestion,
    "",
    "## 2. Key Findings",
    findingsLines(input.findings),
    "",
    "## 3. Scope",
    `- Market: ${input.marketScope.join(", ") || "(none)"}`,
    `- Users: ${input.userScope.join(", ") || "(none)"}`,
    `- Competitors: ${input.competitorScope.join(", ") || "(none)"}`,
    `- Constraints: ${input.constraints.join(", ") || "(none)"}`,
    "",
    "## 4. Options and Tradeoffs",
    optionsLines(input.options),
    "",
    "## 5. Recommendation",
    input.recommendation || "(none)",
    "",
    "## 6. Risks and Unknowns",
    lines(input.risks),
    "",
    "## 7. Next Experiments",
    lines(input.nextExperiments)
  ].join("\n");
}
