import * as fs from 'fs';
import * as path from 'path';
import { convertMarkdownToFinalHtml } from '../src/conversionPipeline';
import * as os from 'os';
import * as yaml from 'js-yaml';
import { fileToRawMarkdown, fileToStrippedMarkdown, macroStrip, runPandocOnStripped, Raw_Markdown, Stripped_Markdown, Pandoc_HTML_Output } from '../src/pandocUtil';

const configPath = path.resolve(__dirname, '../pandoc_global.yaml');
const config = yaml.load(fs.readFileSync(configPath, 'utf8')) as any;
const mdPath = config.pandoc.test_inputs.test_custom_pandoc;
const strippedPath = config.pandoc.test_inputs.test_custom_pandoc_stripped;
const outputHtmlPath = config.pandoc.test_outputs.test_custom_pandoc_html;
const outputMdPath = config.pandoc.test_outputs.stripmacros_test_output;
const debugBasePath = path.resolve(__dirname, '../webview_test_output');
const templatePath = config.pandoc.template;
const tmpDir = os.tmpdir();
const inputPath = path.join(tmpDir, 'pandoc_input_debug.md');
const strippedTmpPath = path.join(tmpDir, 'pandoc_stripped_debug.md');

const md = fs.readFileSync(mdPath, 'utf8') as Raw_Markdown;

const pandocArgs = [
  ...(config.pandoc.args || [])
];

console.error('[DEBUG] Template path:', templatePath);
console.error('[DEBUG] Markdown input path:', mdPath);
console.error('[DEBUG] Markdown input (first 500 chars):', md.slice(0, 500));

(async () => { 
  // Use canonical conversion pipeline
  let finalHtml: Pandoc_HTML_Output;
  try {
    console.error('[DEBUG] Calling convertMarkdownToFinalHtml...');
    finalHtml = await convertMarkdownToFinalHtml(md, debugBasePath, [], undefined, undefined, console.error);
    console.error('[DEBUG] Final HTML for Cursor webview (first 500 chars):', finalHtml.slice(0, 500));
  } catch (e: any) {
    console.error('[DEBUG] Error during convertMarkdownToFinalHtml:', e);
    throw e;
  }

  // Show the text after pandoc_stripmacros
  try {
    const stripped = fs.readFileSync(strippedPath, 'utf8');
    console.error('[DEBUG] Text after pandoc_stripmacros (first 500 chars):', stripped.slice(0, 500));
  } catch (e: any) {
    console.error('[DEBUG] Could not read stripped markdown:', e);
  }

  // Show the text after the pandoc command (markdown)
  try {
    const outMd = fs.readFileSync(outputMdPath, 'utf8');
    console.error('[DEBUG] Text after pandoc command (markdown, first 500 chars):', outMd.slice(0, 500));
  } catch (e: any) {
    console.error('[DEBUG] Could not read output markdown:', e);
  }

  // Show the text after the pandoc command (HTML, if available)
  try {
    const outHtml = fs.readFileSync(outputHtmlPath, 'utf8');
    console.error('[DEBUG] Text after pandoc command (HTML, first 500 chars):', outHtml.slice(0, 500));
  } catch (e: any) {
    console.error('[DEBUG] Could not read output HTML:', e);
  }

  // Simple check: does the output look like a full HTML document?
  if (!finalHtml.trim().startsWith('<!DOCTYPE html>')) {
    console.error('FAIL: Output is not a full HTML document');
    process.exit(1);
  } else {
    console.error('PASS: Output is a full HTML document');
  }

  // Additional test: simulate missing template file
  const missingTemplatePath = '/tmp/this_template_does_not_exist.html';
  try {
    await convertMarkdownToFinalHtml(md, debugBasePath, [], missingTemplatePath, undefined, console.error);
    console.error('WARN: No error was thrown for missing template. This may be expected if Pandoc does not error on missing template.');
  } catch (e: any) {
    if (e.message && e.message.includes('Could not find data file')) {
      console.error('PASS: Detected missing template error from Pandoc');
    } else {
      console.error('WARN: Unexpected error for missing template:', e);
    }
  }

  fs.writeFileSync(outputHtmlPath, finalHtml, 'utf8');

  // Test 1: macroStrip
  console.error('--- TEST 1: macroStrip ---');
  const rawMd = fileToRawMarkdown(mdPath);
  try {
    const stripped = await macroStrip(rawMd);
    console.error('[TEST 1] Stripped markdown (first 500 chars):', stripped.slice(0, 500));
  } catch (e) {
    console.error('[TEST 1] Error:', e);
  }

  // Test 2: runPandocOnStripped
  console.error('--- TEST 2: runPandocOnStripped ---');
  const strippedMd = fileToStrippedMarkdown(strippedPath);
  try {
    const html = await runPandocOnStripped(strippedMd, 'html');
    console.error('[TEST 2] HTML output (first 500 chars):', (html as string).slice(0, 500));
  } catch (e) {
    console.error('[TEST 2] Error:', e);
  }
})(); 