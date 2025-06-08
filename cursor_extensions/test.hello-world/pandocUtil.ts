// @ts-ignore
/// <reference types="node" />
import { spawn } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';

declare const __dirname: string;

console.error('LOADED pandocUtil.ts');

export interface PandocOptions {
  pandocPath?: string;
  inputFormat?: string;
  outputFormat?: string;
  extraArgs?: string[];
}

export function runPandoc(
  md: string,
  callback: (code: number, html: string, err: string) => void,
  templatePath?: string,
  pandocArgs: string[] = []
) {
  const logPath = path.resolve(__dirname, 'pandoc_debug.log');
  const timestamp = new Date().toISOString();
  const pandocPath = '/usr/bin/pandoc';
  const inputFormat = 'markdown';
  const outputFormat = 'html5';
  // Write markdown to a temp file
  const tmpDir = os.tmpdir();
  const mdPath = path.join(tmpDir, `pandoc_input_${process.pid}_${Date.now()}.md`);
  const outPath = path.join(tmpDir, `pandoc_output_${process.pid}_${Date.now()}.html`);
  fs.writeFileSync(mdPath, md, 'utf8');
  const args = ['-f', inputFormat, '-t', outputFormat, mdPath, '-o', outPath, '--standalone'];
  if (templatePath) {
    args.push(`--template=${templatePath}`);
  }
  if (pandocArgs && pandocArgs.length > 0) {
    args.push(...pandocArgs);
  }
  fs.appendFileSync(logPath, `[${timestamp}] Invoking: ${pandocPath} ${args.join(' ')}\n`);
  const pandoc = spawn(pandocPath, args);
  let err = '';
  pandoc.stderr.on('data', (data) => { err += data.toString(); });
  pandoc.on('close', (code) => {
    fs.appendFileSync(logPath, `[${new Date().toISOString()}] Pandoc exited with code ${code}\n`);
    if (err) {
      fs.appendFileSync(logPath, `[${new Date().toISOString()}] Pandoc stderr: ${err}\n`);
    }
    let html = '';
    try {
      html = fs.readFileSync(outPath, 'utf8');
    } catch (e: any) {
      err += `\nFailed to read output file: ${e.stack || e}`;
    }
    // Clean up temp files
    try { fs.unlinkSync(mdPath); } catch {}
    try { fs.unlinkSync(outPath); } catch {}
    callback(code === null ? 1 : code, html, err);
  });
} 