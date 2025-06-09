import { fileToRawMarkdown, fileToStrippedMarkdown, Raw_Markdown, Stripped_Markdown, Pandoc_HTML_Output } from '../src/pandocUtil';
import * as fs from 'fs';
import * as yaml from 'js-yaml';
import * as path from 'path';

const configPath = path.resolve(__dirname, '../pandoc_global.yaml');
const config = yaml.load(fs.readFileSync(configPath, 'utf8')) as any;
const mdPath = config.pandoc.test_inputs.test_custom_pandoc;
const strippedPath = config.pandoc.test_inputs.test_custom_pandoc_stripped;
const htmlPath = config.pandoc.test_outputs.test_custom_pandoc_html;
const stripmacrosOutputPath = config.pandoc.test_outputs.stripmacros_test_output;
const templatePath = config.pandoc.template;

// Test A: Run only the macro-stripping shell script on the markdown file. Confirm output.
async function testA() {
  console.error('--- TEST A: Macro-stripping shell script ---');
  const { execSync } = require('child_process');
  execSync(`/home/dzack/.pandoc/bin/pandoc_stripmacros.sh < ${mdPath} > ${strippedPath}`);
  const stripped: Stripped_Markdown = fs.readFileSync(strippedPath, 'utf8') as Stripped_Markdown;
  console.error('[TEST A] Stripped markdown (first 500 chars):', stripped.slice(0, 500));
}

// Test B: Run Pandoc directly on the stripped markdown file using the exact command from the Makefile
async function testB() {
  console.error('--- TEST B: Pandoc direct shell command ---');
  const { execSync } = require('child_process');
  const config = yaml.load(fs.readFileSync(configPath, 'utf8')) as any;
  const pandocPath = config.pandoc.path;
  const from = config.pandoc.from;
  const to = config.pandoc.to;
  const template = config.pandoc.template;
  const args = config.pandoc.args ? config.pandoc.args.join(' ') : '';
  const cmd = `${pandocPath} --from=${from} --to=${to} --template=${template} ${args} < ${strippedPath} > test_custom_pandoc.html`;
  console.error('[TEST B] Running:', cmd);
  try {
    execSync(cmd, { stdio: 'inherit' });
    const html = fs.readFileSync('test_custom_pandoc.html', 'utf8') as Pandoc_HTML_Output;
    console.error('[TEST B] HTML output (first 500 chars):', html.slice(0, 500));
  } catch (e) {
    console.error('[TEST B] Error:', e);
  }
}

// Test C: Programmatically invoke Pandoc (via Node/TS) on the stripped markdown file
async function testC() {
  console.error('--- TEST C: Programmatic Pandoc on stripped markdown ---');
  const { spawnSync } = require('child_process');
  const config = yaml.load(fs.readFileSync(configPath, 'utf8')) as any;
  const pandocPath = config.pandoc.path;
  const from = config.pandoc.from;
  const to = config.pandoc.to;
  const template = config.pandoc.template;
  const args = config.pandoc.args ? config.pandoc.args : [];
  const cmdArgs = [`--from=${from}`, `--to=${to}`, `--template=${template}`, ...args];
  console.error('[TEST C] Running:', pandocPath, ...cmdArgs, '<', strippedPath);
  const input = fs.readFileSync(strippedPath, 'utf8');
  const proc = spawnSync(pandocPath, cmdArgs, { input, encoding: 'utf8' });
  if (proc.error) {
    console.error('[TEST C] Error:', proc.error);
  } else {
    console.error('[TEST C] stdout (first 500 chars):', (proc.stdout || '').slice(0, 500));
    console.error('[TEST C] stderr:', proc.stderr);
  }
}

// Test D: Programmatically invoke Pandoc on a minimal markdown file, with and without --template
async function testD() {
  console.error('--- TEST D: Minimal markdown, with/without --template ---');
  const { spawnSync } = require('child_process');
  const config = yaml.load(fs.readFileSync(configPath, 'utf8')) as any;
  const pandocPath = config.pandoc.path;
  const from = config.pandoc.from;
  const to = config.pandoc.to;
  const template = config.pandoc.template;
  const minimalMd: Raw_Markdown = '# Hello\n\nThis is a test.' as Raw_Markdown;
  // With template
  let args = [`--from=${from}`, `--to=${to}`, `--template=${template}`];
  console.error('[TEST D] With template:', pandocPath, ...args);
  let proc = spawnSync(pandocPath, args, { input: minimalMd, encoding: 'utf8' });
  if (proc.error) {
    console.error('[TEST D] With template error:', proc.error);
  } else {
    console.error('[TEST D] With template stdout (first 500 chars):', (proc.stdout || '').slice(0, 500));
    console.error('[TEST D] With template stderr:', proc.stderr);
  }
  // Without template
  args = [`--from=${from}`, `--to=${to}`];
  console.error('[TEST D] Without template:', pandocPath, ...args);
  proc = spawnSync(pandocPath, args, { input: minimalMd, encoding: 'utf8' });
  if (proc.error) {
    console.error('[TEST D] Without template error:', proc.error);
  } else {
    console.error('[TEST D] Without template stdout (first 500 chars):', (proc.stdout || '').slice(0, 500));
    console.error('[TEST D] Without template stderr:', proc.stderr);
  }
}

// Test E: Print YAML config and resolved template path
function testE() {
  console.error('--- TEST E: YAML config and resolved template path ---');
  const config = yaml.load(fs.readFileSync(configPath, 'utf8')) as any;
  console.error('[TEST E] YAML config:', JSON.stringify(config, null, 2));
  let templatePathResolved = config.pandoc.template;
  if (templatePathResolved && !path.isAbsolute(templatePathResolved)) {
    templatePathResolved = path.resolve(__dirname, templatePathResolved);
  }
  console.error('[TEST E] Resolved template path:', templatePathResolved);
}

(async () => {
  await testA();
  await testB();
  await testC();
  await testD();
  testE();
})(); 