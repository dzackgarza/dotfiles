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
  callback: (code: number, html: string, err: string, stripped?: string, pandocCmd?: string, pandocStdout?: string, pandocStderr?: string) => void,
  templatePath?: string,
  pandocArgs: string[] = [],
  logDir?: string,
  timestamp?: string,
  log?: (msg: string) => void
) {
  const logPath = logDir && timestamp ? require('path').join(logDir, `logs.log`) : path.resolve(__dirname, 'pandoc_debug.log');
  const writeLog = (msg: string) => {
    const entry = `[${new Date().toISOString()}] ${msg}\n`;
    fs.appendFileSync(logPath, entry);
    if (log) log(msg);
  };
  const pandocPath = '/usr/bin/pandoc';
  const inputFormat = 'markdown';
  const outputFormat = 'html5';
  const tmpDir = os.tmpdir();
  const mdPath = path.join(tmpDir, `pandoc_input_${process.pid}_${Date.now()}.md`);
  const outPath = path.join(tmpDir, `pandoc_output_${process.pid}_${Date.now()}.html`);
  fs.writeFileSync(mdPath, md, 'utf8');
  writeLog('Wrote input markdown to ' + mdPath);
  // Directly run Pandoc on the input markdown
  const args = ['-f', inputFormat, '-t', outputFormat, mdPath, '-o', outPath, '--standalone'];
  if (templatePath) {
    args.push(`--template=${templatePath}`);
  }
  if (pandocArgs && pandocArgs.length > 0) {
    args.push(...pandocArgs);
  }
  const pandocCmd = pandocPath + ' ' + args.join(' ');
  writeLog('Invoking: ' + pandocCmd);
  const pandoc = spawn(pandocPath, args);
  let err = '';
  let stdout = '';
  pandoc.stderr.on('data', (data) => { err += data.toString(); });
  pandoc.stdout.on('data', (data) => { stdout += data.toString(); });
  pandoc.on('close', (code: number | null) => {
    writeLog('Pandoc exited with code ' + code);
    if (err) writeLog('Pandoc stderr: ' + err);
    if (stdout) writeLog('Pandoc stdout: ' + stdout);
    let html = '';
    try {
      html = fs.readFileSync(outPath, 'utf8');
    } catch (e: any) {
      err += `\nFailed to read output file: ${e.stack || e}`;
    }
    try { fs.unlinkSync(mdPath); } catch {}
    try { fs.unlinkSync(outPath); } catch {}
    const exitCode = (typeof code === "number" ? code : 1);
    if (exitCode !== 0) {
      writeLog('Pandoc failed with code ' + exitCode + ': ' + err);
      callback(exitCode, html, err, undefined, pandocCmd, stdout, err);
      process.exit(1); // Crash hard if Pandoc fails
    } else {
      callback(exitCode, html, err, undefined, pandocCmd, stdout, err);
    }
  });
} 