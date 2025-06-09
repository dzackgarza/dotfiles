"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const child_process_1 = require("child_process");
const scriptPath = '/home/dzack/dotfiles/bin/pandoc/pandoc_stripmacros.sh';
const input = 'abd $\\ZZ$ asdwe\n';
console.error('[DEBUG] Script path:', scriptPath);
console.error('[DEBUG] Input:', input);
const proc = (0, child_process_1.spawn)(scriptPath, [], { stdio: ['pipe', 'pipe', 'inherit'] });
let output = '';
proc.stdout.on('data', (data) => {
    output += data.toString();
    console.error('[DEBUG] Received stdout chunk:', data.toString());
});
proc.on('close', (code) => {
    console.error('[DEBUG] Process closed with exit code:', code);
    console.error('[DEBUG] Output:');
    console.error(output);
    if (!output.includes('{\\mathbf{Z}}')) {
        console.error('TEST FAILED: Macro replacement did not occur');
        process.exit(1);
    }
    else {
        console.error('TEST PASSED: Macro replacement occurred');
    }
});
console.error('[DEBUG] Writing input to stdin...');
proc.stdin.write(input);
console.error('[DEBUG] Closing stdin...');
proc.stdin.end();
