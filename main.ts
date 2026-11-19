// News-image entry for make.fun (Node 22, standard library only).
// Writes the entry image to the output directory: the file the judge sees
// is entry.png, copied byte for byte from this repository. The program does
// no network access and no drawing at run time; the image was rendered
// beforehand by render.py in this repository, so every run writes the same
// bytes.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const OUTPUT_NAME = "entry.png";

function outputDir(): string {
  const fromEnv = process.env.MAKEFUN_OUTPUT_DIR;
  return fromEnv && fromEnv.length > 0 ? fromEnv : "/output";
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, OUTPUT_NAME);
  if (!existsSync(source)) {
    throw new Error(`missing ${OUTPUT_NAME} next to main.ts`);
  }
  const bytes = readFileSync(source);
  const dir = outputDir();
  mkdirSync(dir, { recursive: true });
  const target = join(dir, OUTPUT_NAME);
  writeFileSync(target, bytes);
  console.log(`wrote ${target} (${bytes.length} bytes)`);
}

main();
