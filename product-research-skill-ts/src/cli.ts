import { readFileSync } from "node:fs";
import { generateResearchReport } from "./skill.js";
import { ResearchInput } from "./types.js";

function usage(): string {
  return "Usage: node dist/cli.js <input.json>";
}

function parseInput(filePath: string): ResearchInput {
  const raw = readFileSync(filePath, "utf-8");
  return JSON.parse(raw) as ResearchInput;
}

function main(): void {
  const inputPath = process.argv[2];
  if (!inputPath) {
    console.error(usage());
    process.exit(1);
  }

  const input = parseInput(inputPath);
  const output = generateResearchReport(input);
  process.stdout.write(output + "\n");
}

main();
