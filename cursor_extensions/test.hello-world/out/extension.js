const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const { runPandoc } = require('./pandocUtil.js');

function activate(context) {
  let disposable = vscode.commands.registerCommand('hello-world.sayHello', function () {
    vscode.window.showInformationMessage('Hello from Hello World extension!');
  });
  context.subscriptions.push(disposable);

  // Minimal Pandoc-based Markdown webview
  let webviewDisposable = vscode.commands.registerCommand('hello-world.showMarkdownWebview', function () {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'markdown') {
      vscode.window.showErrorMessage('Please open a Markdown file to preview.');
      return;
    }
    const panel = vscode.window.createWebviewPanel(
      'markdownWebview',
      'Markdown Webview',
      vscode.ViewColumn.Beside,
      {}
    );
    const md = editor.document.getText();
    const logPath = path.resolve(__dirname, 'pandoc_debug.log');
    // Log startup message
    fs.appendFileSync(logPath, `\n[${new Date().toISOString()}] Starting Pandoc invocation\n`);
    try {
      // Use Pandoc without the Lua filter
      const pandoc = spawn('/usr/bin/pandoc', ['-f', 'gfm', '-t', 'html']);
      let html = '';
      let err = '';
      pandoc.stdout.on('data', (data) => { html += data.toString(); });
      pandoc.stderr.on('data', (data) => { err += data.toString(); });
      pandoc.on('close', (code) => {
        fs.appendFileSync(logPath, `[${new Date().toISOString()}] Pandoc exited with code ${code}\n`);
        if (err) {
          fs.appendFileSync(logPath, `[${new Date().toISOString()}] Pandoc stderr: ${err}\n`);
        }
        if (code !== 0) {
          fs.appendFileSync(logPath, `[${new Date().toISOString()}] Pandoc failed.\n`);
          let logTail = '';
          try {
            const logContent = fs.readFileSync(logPath, 'utf8').split('\n');
            logTail = logContent.slice(-20).join('\n');
          } catch (e) {
            logTail = 'Could not read pandoc_debug.log: ' + (e.stack || e);
          }
          panel.webview.html = `<pre>Pandoc failed with code ${code}\n\n--- pandoc_debug.log (last 20 lines) ---\n${logTail}</pre>`;
        } else {
          panel.webview.html = html;
        }
      });
      pandoc.stdin.write(md);
      pandoc.stdin.end();
      return;
    } catch (e) {
      fs.appendFileSync(logPath, `[${new Date().toISOString()}] Exception: ${e.stack || e}\n`);
    }
  });
  context.subscriptions.push(webviewDisposable);
}
exports.activate = activate;

function deactivate() {}
exports.deactivate = deactivate;

if (require.main === module) {
  // Standalone test runner for Pandoc invocation
  const fs = require('fs');
  const path = require('path');
  const mdPath = path.resolve(__dirname, '../../test_checkboxes.md');
  const md = fs.readFileSync(mdPath, 'utf8');
  runPandoc(md, (code, html, err) => {
    if (code === 0) {
      console.log(html);
    } else {
      console.error(`Pandoc failed with code ${code}`);
      if (err) console.error(err);
    }
  });
} 