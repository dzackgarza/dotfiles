import { spawn } from 'child_process';

const scriptPath = '/home/dzack/dotfiles/bin/pandoc/pandoc_stripmacros.sh';
const input = 'abd $\\ZZ$ asdwe\n';

console.log('Input:');
console.log(input);

const proc = spawn(scriptPath, [], { stdio: ['pipe', 'pipe', 'inherit'] });

let output = '';
proc.stdout.on('data', (data) => {
  output += data.toString();
});

proc.on('close', (code) => {
  console.log('Exit code:', code);
  console.log('Output:');
  console.log(output);
  if (!output.includes('{\\mathbf{Z}}')) {
    console.error('TEST FAILED: Macro replacement did not occur');
    process.exit(1);
  } else {
    console.log('TEST PASSED: Macro replacement occurred');
  }
});

proc.stdin.write(input);
proc.stdin.end(); 