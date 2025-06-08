// @ts-ignore
/// <reference types="node" />
import { spawn } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

declare const __dirname: string;

export function runPandoc(md: string, callback: (code: number, html: string, err: string) => void) {
  const logPath = path.resolve(__dirname, 'pandoc_debug.log');
  const timestamp = new Date().toISOString();
  fs.appendFileSync(logPath, `[${timestamp}] Invoking: pandoc -f markdown -t html\n`);
  const pandoc = spawn('pandoc', ['-f', 'markdown', '-t', 'html']);
  let html = '';
  let err = '';
  pandoc.stdout.on('data', (data) => { html += data.toString(); });
  pandoc.stderr.on('data', (data) => { err += data.toString(); });
  pandoc.on('close', (code) => {
    fs.appendFileSync(logPath, `[${new Date().toISOString()}] Pandoc exited with code ${code}\n`);
    if (err) {
      fs.appendFileSync(logPath, `[${new Date().toISOString()}] Pandoc stderr: ${err}\n`);
    }
    callback(code === null ? 1 : code, html, err);
  });
  pandoc.stdin.write(md);
  pandoc.stdin.end();
} 