import { runPandoc } from './pandocUtil';

const md = '# Hello World\n\nThis is a test.';

runPandoc(md, (code, html, err) => {
  console.log('Pandoc exit code:', code);
  console.log('HTML output:', html.slice(0, 200));
  if (err) console.error('Pandoc stderr:', err);
}, undefined, []); 