import { runPandoc } from './pandocUtil';
import * as fs from 'fs';

export async function convertMarkdownToFinalHtml(md: string, debugBasePath?: string, templatePath?: string, pandocArgs: string[] = []): Promise<string> {
  // Step 1: Pandoc (standalone)
  const html: string = await new Promise((resolve, reject) => {
    runPandoc(md, (code: number, html: string, err: string) => {
      if (code !== 0) {
        reject(new Error(`Pandoc failed with code ${code}: ${err}`));
      } else {
        resolve(html);
      }
    }, templatePath, pandocArgs);
  });
  if (debugBasePath) {
    fs.writeFileSync(debugBasePath + '.final.html', html, 'utf8');
  }
  return html;
} 