import * as fs from 'fs';
import * as path from 'path';
import { convertMarkdownToFinalHtml } from './conversionPipeline';

const mdPath = path.resolve(__dirname, '../test_custom_pandoc.md');
const md = fs.readFileSync(mdPath, 'utf8');
const debugBasePath = path.resolve(__dirname, '../webview_test_output');
const templatePath = path.resolve(__dirname, 'pandoc_webview_template.html');

(async () => {
  // Use canonical conversion pipeline
  let finalHtml: string;
  try {
    finalHtml = await convertMarkdownToFinalHtml(md, debugBasePath, templatePath, ['--mathjax']);
    console.log('Webview HTML output saved to webview_test_output.final.html');
  } catch (e: any) {
    console.error('FAIL: Conversion pipeline failed:', e);
    process.exit(1);
  }
  // Simple check: does the output look like a full HTML document?
  if (!finalHtml.trim().startsWith('<!DOCTYPE html>')) {
    console.error('FAIL: Output is not a full HTML document');
    process.exit(1);
  }
  console.log('PASS: Output is a full HTML document');

  // Additional test: simulate missing template file
  const missingTemplatePath = '/tmp/this_template_does_not_exist.html';
  let errorCaught = false;
  try {
    await convertMarkdownToFinalHtml(md, debugBasePath, missingTemplatePath, []);
    console.error('FAIL: Expected error for missing template, but none was thrown');
    process.exit(1);
  } catch (e: any) {
    if (e.message && e.message.includes('Could not find data file')) {
      console.log('PASS: Detected missing template error from Pandoc');
      errorCaught = true;
    } else {
      console.error('FAIL: Unexpected error for missing template:', e);
      process.exit(1);
    }
  }
  if (!errorCaught) {
    console.error('FAIL: Missing template error was not detected');
    process.exit(1);
  }
})(); 