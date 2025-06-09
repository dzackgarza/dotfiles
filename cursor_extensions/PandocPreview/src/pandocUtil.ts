// @ts-ignore
/// <reference types="node" />
import { spawn, spawnSync } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';
import * as yaml from 'js-yaml';

declare const __dirname: string;

console.error('LOADED pandocUtil.ts');

// ---- CONSTANTS ----
export const CONFIG_PATH = path.resolve(__dirname, 'pandoc_global.yaml');
export const STRIP_MACROS_PATH = '/home/dzack/.pandoc/bin/pandoc_stripmacros.sh';
export const DEFAULT_TEMPLATE_PATH = path.resolve(__dirname, '../templates/pandoc_webview_template.html');
export const TMP_DIR = os.tmpdir();

// Load config from YAML
export function loadPandocConfig() {
  if (!fs.existsSync(CONFIG_PATH)) throw new Error('Config file not found: ' + CONFIG_PATH);
  return yaml.load(fs.readFileSync(CONFIG_PATH, 'utf8')) as any;
}

// ---- TYPE SYSTEM ----
export type Brand<K, T> = K & { __brand: T };
export type Raw_Markdown = Brand<string, "Raw_Markdown">;
export type Stripped_Markdown = Brand<string, "Stripped_Markdown">;
export type Pandoc_HTML_Output = Brand<string, "Pandoc_HTML_Output">;
export type Pandoc_Markdown_Output = Brand<string, "Pandoc_Markdown_Output">;

// ---- FILE UTILITIES ----
/**
 * PURE
 * FILE -> RAW_MARKDOWN
 */
export function fileToRawMarkdown(file: string): Raw_Markdown {
  if (!fs.existsSync(file)) throw new Error('File not found: ' + file);
  return fs.readFileSync(file, 'utf8') as Raw_Markdown;
}
/**
 * PURE
 * FILE -> STRIPPED_MARKDOWN
 */
export function fileToStrippedMarkdown(file: string): Stripped_Markdown {
  if (!fs.existsSync(file)) throw new Error('File not found: ' + file);
  return fs.readFileSync(file, 'utf8') as Stripped_Markdown;
}
/**
 * SIDE-EFFECTING (writes to disk)
 * RAW_MARKDOWN -> FILE
 */
export function rawMarkdownToFile(md: Raw_Markdown, file: string) {
  if (typeof md !== 'string') throw new Error('Not a Raw_Markdown string');
  fs.writeFileSync(file, md, 'utf8');
}
/**
 * SIDE-EFFECTING (writes to disk)
 * STRIPPED_MARKDOWN -> FILE
 */
export function strippedMarkdownToFile(md: Stripped_Markdown, file: string) {
  if (typeof md !== 'string') throw new Error('Not a Stripped_Markdown string');
  fs.writeFileSync(file, md, 'utf8');
}

// ---- MACRO STRIPPING ----
/**
 * SIDE-EFFECTING (spawns process)
 * RAW_MARKDOWN -> STRIPPED_MARKDOWN
 */
export function macroStrip(md: Raw_Markdown): Promise<Stripped_Markdown> {
  if (typeof md !== 'string') throw new Error('Input is not Raw_Markdown');
  return new Promise((resolve, reject) => {
    const proc = spawn(STRIP_MACROS_PATH, [], { stdio: ['pipe', 'pipe', 'pipe'] });
    let out = '';
    let err = '';
    proc.stdout.on('data', (data) => { out += data.toString(); });
    proc.stderr.on('data', (data) => { err += data.toString(); });
    proc.on('close', (code) => {
      if (code === 0) resolve(out as Stripped_Markdown);
      else reject(new Error('macroStrip failed: ' + err));
    });
    proc.stdin.write(md);
    proc.stdin.end();
  });
}

// ---- PANDOC CONVERSION ----
/**
 * SIDE-EFFECTING (spawns process)
 * STRIPPED_MARKDOWN -> (PANDOC_HTML_OUTPUT | PANDOC_MARKDOWN_OUTPUT)
 */
export function runPandocOnStripped(
  md: Stripped_Markdown,
  to: 'html' | 'markdown',
  extraArgs: string[] = [],
  templatePath?: string
): Promise<Pandoc_HTML_Output | Pandoc_Markdown_Output> {
  if (typeof md !== 'string') throw new Error('Input is not Stripped_Markdown');
  const config = loadPandocConfig();
  const pandocPath = config.pandoc.path;
  const from = config.pandoc.from;
  const args = [
    '--from=' + from,
    '--to=' + to,
    ...(templatePath ? ['--template=' + templatePath] : []),
    ...(config.pandoc.args || []),
    ...extraArgs
  ];
  return new Promise((resolve, reject) => {
    const proc = spawn(pandocPath, args, { stdio: ['pipe', 'pipe', 'pipe'] });
    let out = '';
    let err = '';
    proc.stdout.on('data', (data) => { out += data.toString(); });
    proc.stderr.on('data', (data) => { err += data.toString(); });
    proc.on('close', (code) => {
      if (code === 0) {
        if (to === 'html') resolve(out as Pandoc_HTML_Output);
        else resolve(out as Pandoc_Markdown_Output);
      } else {
        reject(new Error('runPandocOnStripped failed: ' + err));
      }
    });
    proc.stdin.write(md);
    proc.stdin.end();
  });
}

// =============================
// PIPELINE / COMPOSED FUNCTIONS
// =============================

/**
 * SIDE-EFFECTING (spawns process)
 * RAW_MARKDOWN -> { output: PANDOC_HTML_OUTPUT | PANDOC_MARKDOWN_OUTPUT, stripped: STRIPPED_MARKDOWN }
 * Pipeline: macroStrip -> runPandocOnStripped
 */
export async function rawMarkdownToStrippedMarkdownAndConvert(
  md: Raw_Markdown,
  to: 'html' | 'markdown',
  extraArgs: string[] = [],
  templatePath?: string
): Promise<{ output: Pandoc_HTML_Output | Pandoc_Markdown_Output, stripped: Stripped_Markdown }> {
  if (typeof md !== 'string') throw new Error('Input is not Raw_Markdown');
  const stripped = await macroStrip(md);
  const output = await runPandocOnStripped(stripped, to, extraArgs, templatePath);
  return { output, stripped };
}

// ---- TESTABLE PIECES ----
// Export all above for individual testing

// ---- INJECT MATHJAX ----
/**
 * PURE
 * PANDOC_HTML_OUTPUT -> PANDOC_HTML_OUTPUT
 */
export function injectMathJaxConfig(html: Pandoc_HTML_Output): Pandoc_HTML_Output {
  if (typeof html !== 'string') throw new Error('Input is not Pandoc_HTML_Output');
  const MATHJAX_V3_CONFIG = `<script>\nwindow.MathJax = {\n  tex: {\n    inlineMath: [['\\(','\\)']],\n    displayMath: [['\\[','\\]']],\n    tags: 'ams'\n  },\n  options: {\n    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']\n  }\n};\n</script>\n<script src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\"></script>`;
  return html.replace(/<\/head>/i, `${MATHJAX_V3_CONFIG}\n</head>`) as Pandoc_HTML_Output;
}

export interface PandocOptions {
  pandocPath?: string;
  inputFormat?: string;
  outputFormat?: string;
  extraArgs?: string[];
} 