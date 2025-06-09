import { runPandocOnStripped, macroStrip, Raw_Markdown, Stripped_Markdown, Pandoc_HTML_Output } from './pandocUtil';
import * as fs from 'fs';

const MATHJAX_V3_CONFIG = `<script>
window.MathJax = {
  tex: {
    inlineMath: [['\\(','\\)']],
    displayMath: [['\\[','\\]']],
    tags: 'ams'
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }
};
</script>\n<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>`;

export async function convertMarkdownToFinalHtml(md: Raw_Markdown, debugBasePath?: string, pandocArgs: string[] = [], logDir?: string, timestamp?: string, log?: (msg: string) => void): Promise<Pandoc_HTML_Output> {
  if (log) log('convertMarkdownToFinalHtml: called (NOT STALE)');
  // Save stripped markdown after macro stripping
  let strippedMd: Stripped_Markdown | undefined = undefined;
  if (log) log('convertMarkdownToFinalHtml: md (first 200 chars): ' + md.slice(0, 200));
  if (log) log('convertMarkdownToFinalHtml: pandocArgs: ' + JSON.stringify(pandocArgs)); 
  if (log) log('convertMarkdownToFinalHtml: debugBasePath: ' + debugBasePath);
  if (log) log('convertMarkdownToFinalHtml: logDir: ' + logDir);
  if (log) log('convertMarkdownToFinalHtml: timestamp: ' + timestamp);
  if (log) log('convertMarkdownToFinalHtml: log: ' + typeof log);

  // Use the new pipeline: convert md (Raw_Markdown) to stripped, then to HTML
  const stripped = await macroStrip(md);
  const html = await runPandocOnStripped(stripped, 'html', pandocArgs);
  // Inject MathJax config
  const injectedHtml = (html as string).replace(/<\/head>/i, `${MATHJAX_V3_CONFIG}\n</head>`) as Pandoc_HTML_Output;
  if (debugBasePath) {
    fs.writeFileSync(debugBasePath + '.final.html', injectedHtml, 'utf8');
  }
  if (log) log('convertMarkdownToFinalHtml: finished');
  return injectedHtml;
} 