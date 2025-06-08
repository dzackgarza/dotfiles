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
  const stripMacrosPath = path.resolve(__dirname, '../../bin/pandoc/pandoc_stripmacros.sh');
  const inputFormat = 'markdown';
  const outputFormat = 'html5';
  const tmpDir = os.tmpdir();
  const mdPath = path.join(tmpDir, `pandoc_input_${process.pid}_${Date.now()}.md`);
  const strippedMdPath = path.join(tmpDir, `pandoc_stripped_${process.pid}_${Date.now()}.md`);
  const outPath = path.join(tmpDir, `pandoc_output_${process.pid}_${Date.now()}.html`);
  fs.writeFileSync(mdPath, md, 'utf8');
  writeLog('Wrote input markdown to ' + mdPath);
  // 1. Run pandoc_stripmacros.sh on the input markdown
  writeLog('Invoking: ' + stripMacrosPath + ' < ' + mdPath);
  const stripProc = spawn(stripMacrosPath, [], { stdio: ['pipe', 'pipe', 'pipe'] });
  let stripErr = '';
  let stripOut = Buffer.alloc(0);
  stripProc.stderr.on('data', (data) => { stripErr += data.toString(); });
  stripProc.stdout.on('data', (data) => { stripOut = Buffer.concat([stripOut, data]); });
  stripProc.on('close', (stripCode: number | null) => {
    const exitCode = (typeof stripCode === "number" ? stripCode : 1);
    if (exitCode !== 0) {
      writeLog('pandoc_stripmacros.sh exited with code ' + exitCode);
      if (stripErr) writeLog('pandoc_stripmacros.sh stderr: ' + stripErr);
      try { fs.unlinkSync(mdPath); } catch {}
      callback(exitCode, '', `pandoc_stripmacros.sh failed: ${stripErr}`);
      return;
    }
    fs.writeFileSync(strippedMdPath, stripOut);
    if (logDir && timestamp) {
      const strippedPath = path.join(logDir, `stripped_${timestamp}.md`);
      fs.writeFileSync(strippedPath, stripOut, 'utf8');
      writeLog('Saved stripped markdown to ' + strippedPath);
    }
    const strippedText = stripOut.toString('utf8');
    writeLog('[DEBUG] Stripped markdown before Pandoc:\n' + strippedText);
    // 2. Run Pandoc as before, but on the stripped markdown
    const args = ['-f', inputFormat, '-t', outputFormat, strippedMdPath, '-o', outPath, '--standalone'];
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
      try { fs.unlinkSync(strippedMdPath); } catch {}
      try { fs.unlinkSync(outPath); } catch {}
      const exitCode = (typeof code === "number" ? code : 1);
      if (exitCode !== 0) {
        writeLog('Pandoc failed with code ' + exitCode + ': ' + err);
        callback(exitCode, html, err, strippedText, pandocCmd, stdout, err);
        process.exit(1); // Crash hard if Pandoc fails
      } else {
        callback(exitCode, html, err, strippedText, pandocCmd, stdout, err);
      }
    });
  });
  const mdStream = fs.createReadStream(mdPath);
  mdStream.pipe(stripProc.stdin);
} 