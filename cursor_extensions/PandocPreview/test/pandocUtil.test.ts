import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import {
  CONFIG_PATH,
  STRIP_MACROS_PATH,
  DEFAULT_TEMPLATE_PATH,
  TMP_DIR,
  loadPandocConfig,
  fileToRawMarkdown,
  fileToStrippedMarkdown,
  rawMarkdownToFile,
  strippedMarkdownToFile,
  macroStrip,
  runPandocOnStripped,
  rawMarkdownToStrippedMarkdownAndConvert,
  injectMathJaxConfig,
  Raw_Markdown,
  Stripped_Markdown,
  Pandoc_HTML_Output,
  Pandoc_Markdown_Output
} from '../src/pandocUtil';

describe('pandocUtil', () => {
  const config = loadPandocConfig();
  const testRawPath = config.pandoc.test_inputs.test_custom_pandoc;
  const testStrippedPath = config.pandoc.test_inputs.test_custom_pandoc_stripped;
  const testHtmlPath = config.pandoc.test_outputs.test_custom_pandoc_html;
  const testOutputMdPath = config.pandoc.test_outputs.stripmacros_test_output;

  describe('fileToRawMarkdown', () => {
    it('reads a file and returns Raw_Markdown', () => {
      const md = fileToRawMarkdown(testRawPath);
      expect(typeof md).toBe('string');
      expect(md.length).toBeGreaterThan(0);
    });
    it('throws if file does not exist', () => {
      expect(() => fileToRawMarkdown('/nonexistent.md')).toThrow();
    });
  });

  describe('fileToStrippedMarkdown', () => {
    it('reads a file and returns Stripped_Markdown', () => {
      const md = fileToStrippedMarkdown(testStrippedPath);
      expect(typeof md).toBe('string');
      expect(md.length).toBeGreaterThan(0);
    });
    it('throws if file does not exist', () => {
      expect(() => fileToStrippedMarkdown('/nonexistent.md')).toThrow();
    });
  });

  describe('rawMarkdownToFile', () => {
    it('writes Raw_Markdown to a file', () => {
      const tmp = path.join(TMP_DIR, 'raw_test.md');
      const md = fileToRawMarkdown(testRawPath);
      rawMarkdownToFile(md, tmp);
      expect(fs.existsSync(tmp)).toBe(true);
      const read = fs.readFileSync(tmp, 'utf8');
      expect(read).toBe(md);
      fs.unlinkSync(tmp);
    });
  });

  describe('strippedMarkdownToFile', () => {
    it('writes Stripped_Markdown to a file', () => {
      const tmp = path.join(TMP_DIR, 'stripped_test.md');
      const md = fileToStrippedMarkdown(testStrippedPath);
      strippedMarkdownToFile(md, tmp);
      expect(fs.existsSync(tmp)).toBe(true);
      const read = fs.readFileSync(tmp, 'utf8');
      expect(read).toBe(md);
      fs.unlinkSync(tmp);
    });
  });

  describe('macroStrip', () => {
    it('strips macros from Raw_Markdown', async () => {
      const md = fileToRawMarkdown(testRawPath);
      const stripped = await macroStrip(md);
      expect(typeof stripped).toBe('string');
      expect(stripped.length).toBeGreaterThan(0);
    });
    it('throws on non-string input', () => {
      // Synchronous error, not a rejected promise
      // @ts-expect-error
      expect(() => macroStrip(123)).toThrow('Input is not Raw_Markdown');
    });
    it('SEMANTIC: strips macros as expected', async () => {
      const input = '# Title\n\n:::{.remark}\nThis is a macro.\n:::\n' as Raw_Markdown;
      const expected = '# Title\n\n::: remark\nThis is a macro.\n:::\n';
      const stripped = await macroStrip(input);
      expect(stripped.replace(/\r/g, '')).toContain('::: remark');
      expect(stripped.replace(/\r/g, '')).not.toContain(':::{.remark}');
    });
    it('SEMANTIC: strips multiple macro environments', async () => {
      const input = '# Test\n\n:::{.theorem}\nThis is a theorem.\n:::\n\n:::{.proof}\nThis is a proof.\n:::\n' as Raw_Markdown;
      const stripped = await macroStrip(input);
      expect(stripped).toContain('::: theorem');
      expect(stripped).toContain('This is a theorem.');
      expect(stripped).toContain('::: proof');
      expect(stripped).toContain('This is a proof.');
      expect(stripped).not.toContain(':::{.theorem}');
      expect(stripped).not.toContain(':::{.proof}');
    });
    it('SEMANTIC: preserves math environments', async () => {
      const input = '# Math\n\n$E=mc^2$\n\n:::{.remark}\nLet $x$ be a variable.\n:::\n' as Raw_Markdown;
      const stripped = await macroStrip(input);
      expect(stripped).toContain('\\( E=mc^2 \\)');
      expect(stripped).toContain('Let \\( x \\) be a variable.');
      const html = await runPandocOnStripped(stripped as Stripped_Markdown, 'html');
      expect(html).toContain('E=mc^2');
      expect(html).toContain('Let');
      expect(html).toContain('math inline');
    });
    it('SEMANTIC: unknown environments are passed through', async () => {
      const input = '# Unknown\n\n:::{.foobar}\nThis is unknown.\n:::\n' as Raw_Markdown;
      const stripped = await macroStrip(input);
      expect(stripped).toContain('::: foobar');
      expect(stripped).toContain('This is unknown.');
      const html = await runPandocOnStripped(stripped as Stripped_Markdown, 'html');
      expect(html).toContain('This is unknown.');
      expect(html).toContain('foobar');
    });
    it('SEMANTIC: nested environments are handled', async () => {
      const input = '# Nested\n\n:::{.theorem}\nStatement\n\n:::{.proof}\nProof body\n:::\n\n:::\n' as Raw_Markdown;
      const stripped = await macroStrip(input);
      expect(stripped).toContain('::: theorem');
      expect(stripped).toContain('::: proof');
      expect(stripped).toContain('Proof body');
      expect(stripped).toContain('Statement');
      const html = await runPandocOnStripped(stripped as Stripped_Markdown, 'html');
      expect(html).toContain('Proof body');
      expect(html).toContain('Statement');
      expect(html).toContain('theorem');
      expect(html).toContain('proof');
    });
    it('SEMANTIC: file with no macros is unchanged and produces valid HTML', async () => {
      const input = '# No Macros\n\nJust text.\n\n- List\n- Items\n' as Raw_Markdown;
      const stripped = await macroStrip(input);
      expect(stripped).toContain('No Macros');
      expect(stripped).toContain('Just text.');
      expect(stripped).toMatch(/-\s+List/);
      expect(stripped).toMatch(/-\s+Items/);
      const html = await runPandocOnStripped(stripped as Stripped_Markdown, 'html');
      expect(html).toContain('No Macros');
      expect(html).toContain('Just text.');
      expect(html).toContain('<ul>');
      expect(html).toContain('<li>Items</li>');
    });
  });

  describe('runPandocOnStripped', () => {
    it('converts Stripped_Markdown to HTML', async () => {
      const md = fileToStrippedMarkdown(testStrippedPath);
      const html = await runPandocOnStripped(md, 'html');
      expect(typeof html).toBe('string');
      expect(String(html).trim().startsWith('<!DOCTYPE html>')).toBe(true);
    });
    it('converts Stripped_Markdown to Markdown', async () => {
      const md = fileToStrippedMarkdown(testStrippedPath);
      const out = await runPandocOnStripped(md, 'markdown');
      expect(typeof out).toBe('string');
      expect(String(out).length).toBeGreaterThan(0);
    });
    it('throws on non-string input', () => {
      // Synchronous error, not a rejected promise
      // @ts-expect-error
      expect(() => runPandocOnStripped(123, 'html')).toThrow('Input is not Stripped_Markdown');
    });
    it('SEMANTIC: converts stripped markdown to expected HTML', async () => {
      const stripped = '# Title\n\n::: remark\nThis is a macro.\n:::\n' as Stripped_Markdown;
      const html = await runPandocOnStripped(stripped, 'html');
      expect(typeof html).toBe('string');
      expect(html).toContain('<h1 id="title">Title</h1>');
      expect(html).toContain('<div class="remark">');
      expect(html).toContain('This is a macro.');
    });
  });

  describe('rawMarkdownToStrippedMarkdownAndConvert', () => {
    it('runs the full pipeline: macroStrip then runPandocOnStripped', async () => {
      const md = fileToRawMarkdown(testRawPath);
      const { output, stripped } = await rawMarkdownToStrippedMarkdownAndConvert(md, 'html');
      expect(typeof output).toBe('string');
      expect(typeof stripped).toBe('string');
      expect(String(output).trim().startsWith('<!DOCTYPE html>')).toBe(true);
    });
  });

  describe('injectMathJaxConfig', () => {
    it('injects MathJax config into Pandoc_HTML_Output', () => {
      const html = '<!DOCTYPE html><html><head></head><body></body></html>' as unknown as Pandoc_HTML_Output;
      const injected = injectMathJaxConfig(html);
      expect(typeof injected).toBe('string');
      expect(injected).toContain('MathJax');
      expect(injected).toContain('</head>');
    });
    it('throws on non-string input', () => {
      // @ts-expect-error
      expect(() => injectMathJaxConfig(123)).toThrow();
    });
  });
}); 