import { runPandoc } from './pandocUtil';
import * as fs from 'fs';

export async function convertMarkdownToFinalHtml(md: string, debugBasePath?: string, templatePath?: string, pandocArgs: string[] = [], logDir?: string, timestamp?: string, log?: (msg: string) => void): Promise<string> {
  if (log) log('convertMarkdownToFinalHtml: called');
  // Save stripped markdown after macro stripping
  let strippedMd: string | undefined = undefined;
  const html: string = await new Promise((resolve, reject) => {
    runPandoc(md, (code: number, html: string, err: string, stripped?: string, pandocCmd?: string, pandocStdout?: string, pandocStderr?: string) => {
      if (log) {
        log('Pandoc command: ' + (pandocCmd || 'unknown'));
        log('Pandoc return code: ' + code);
        if (pandocStdout) log('Pandoc stdout: ' + pandocStdout);
        if (pandocStderr) log('Pandoc stderr: ' + pandocStderr);
      }
      if (stripped && logDir && timestamp) {
        const strippedPath = require('path').join(logDir, `stripped_${timestamp}.md`);
        fs.writeFileSync(strippedPath, stripped, 'utf8');
        if (log) log('Saved stripped markdown to ' + strippedPath);
      }
      if (code !== 0) {
        if (log) log('Pandoc failed with code ' + code + ': ' + err);
        reject(new Error('Pandoc failed with code ' + code + ': ' + err));
      } else {
        resolve(html);
      }
    }, templatePath, pandocArgs, logDir, timestamp, log);
  });
  if (debugBasePath) {
    fs.writeFileSync(debugBasePath + '.final.html', html, 'utf8');
  }
  if (log) log('convertMarkdownToFinalHtml: finished');
  return html;
} 