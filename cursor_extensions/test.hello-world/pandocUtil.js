"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.runPandoc = runPandoc;
// @ts-ignore
/// <reference types="node" />
var child_process_1 = require("child_process");
var path = require("path");
var fs = require("fs");
var os = require("os");
console.error('LOADED pandocUtil.ts');
function runPandoc(md, callback, templatePath, pandocArgs) {
    if (pandocArgs === void 0) { pandocArgs = []; }
    var logPath = path.resolve(__dirname, 'pandoc_debug.log');
    var timestamp = new Date().toISOString();
    var pandocPath = '/usr/bin/pandoc';
    var stripMacrosPath = path.resolve(__dirname, '../../bin/pandoc/pandoc_stripmacros.sh');
    var inputFormat = 'markdown';
    var outputFormat = 'html5';
    var tmpDir = os.tmpdir();
    var mdPath = path.join(tmpDir, "pandoc_input_".concat(process.pid, "_").concat(Date.now(), ".md"));
    var strippedMdPath = path.join(tmpDir, "pandoc_stripped_".concat(process.pid, "_").concat(Date.now(), ".md"));
    var outPath = path.join(tmpDir, "pandoc_output_".concat(process.pid, "_").concat(Date.now(), ".html"));
    fs.writeFileSync(mdPath, md, 'utf8');
    // 1. Run pandoc_stripmacros.sh on the input markdown
    fs.appendFileSync(logPath, "[".concat(timestamp, "] Invoking: ").concat(stripMacrosPath, " < ").concat(mdPath, "\n"));
    var stripProc = (0, child_process_1.spawn)(stripMacrosPath, [], { stdio: ['pipe', 'pipe', 'pipe'] });
    var stripErr = '';
    var stripOut = Buffer.alloc(0);
    stripProc.stderr.on('data', function (data) { stripErr += data.toString(); });
    stripProc.stdout.on('data', function (data) { stripOut = Buffer.concat([stripOut, data]); });
    stripProc.on('close', function (stripCode) {
        var exitCode = (typeof stripCode === "number" ? stripCode : 1);
        if (exitCode !== 0) {
            fs.appendFileSync(logPath, "[".concat(new Date().toISOString(), "] pandoc_stripmacros.sh exited with code ").concat(exitCode, "\n"));
            if (stripErr) {
                fs.appendFileSync(logPath, "[".concat(new Date().toISOString(), "] pandoc_stripmacros.sh stderr: ").concat(stripErr, "\n"));
            }
            // Clean up temp file
            try {
                fs.unlinkSync(mdPath);
            }
            catch (_a) { }
            callback(exitCode, '', "pandoc_stripmacros.sh failed: ".concat(stripErr));
            return;
        }
        // Write the filtered markdown to a temp file
        fs.writeFileSync(strippedMdPath, stripOut);
        // 2. Run Pandoc as before, but on the stripped markdown
        var args = ['-f', inputFormat, '-t', outputFormat, strippedMdPath, '-o', outPath, '--standalone'];
        if (templatePath) {
            args.push("--template=".concat(templatePath));
        }
        if (pandocArgs && pandocArgs.length > 0) {
            args.push.apply(args, pandocArgs);
        }
        fs.appendFileSync(logPath, "[".concat(new Date().toISOString(), "] Invoking: ").concat(pandocPath, " ").concat(args.join(' '), "\n"));
        var pandoc = (0, child_process_1.spawn)(pandocPath, args);
        var err = '';
        pandoc.stderr.on('data', function (data) { err += data.toString(); });
        pandoc.on('close', function (code) {
            fs.appendFileSync(logPath, "[".concat(new Date().toISOString(), "] Pandoc exited with code ").concat(code, "\n"));
            if (err) {
                fs.appendFileSync(logPath, "[".concat(new Date().toISOString(), "] Pandoc stderr: ").concat(err, "\n"));
            }
            var html = '';
            try {
                html = fs.readFileSync(outPath, 'utf8');
            }
            catch (e) {
                err += "\nFailed to read output file: ".concat(e.stack || e);
            }
            // Clean up temp files
            try {
                fs.unlinkSync(mdPath);
            }
            catch (_a) { }
            try {
                fs.unlinkSync(strippedMdPath);
            }
            catch (_b) { }
            try {
                fs.unlinkSync(outPath);
            }
            catch (_c) { }
            var exitCode = (typeof code === "number" ? code : 1);
            callback(exitCode, html, err);
        });
    });
    // Pipe the input markdown to the stripmacros process
    var mdStream = fs.createReadStream(mdPath);
    mdStream.pipe(stripProc.stdin);
}
