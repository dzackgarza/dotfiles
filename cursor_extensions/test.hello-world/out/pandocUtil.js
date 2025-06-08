"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.runPandoc = runPandoc;
// @ts-ignore
/// <reference types="node" />
var child_process_1 = require("child_process");
var path = require("path");
var fs = require("fs");
function runPandoc(md, callback) {
    var logPath = path.resolve(__dirname, 'pandoc_debug.log');
    var timestamp = new Date().toISOString();
    fs.appendFileSync(logPath, "[".concat(timestamp, "] Invoking: pandoc -f gfm -t html\n"));
    var pandoc = (0, child_process_1.spawn)('pandoc', ['-f', 'gfm', '-t', 'html']);
    var html = '';
    var err = '';
    pandoc.stdout.on('data', function (data) { html += data.toString(); });
    pandoc.stderr.on('data', function (data) { err += data.toString(); });
    pandoc.on('close', function (code) {
        fs.appendFileSync(logPath, "[".concat(new Date().toISOString(), "] Pandoc exited with code ").concat(code, "\n"));
        if (err) {
            fs.appendFileSync(logPath, "[".concat(new Date().toISOString(), "] Pandoc stderr: ").concat(err, "\n"));
        }
        callback(code === null ? 1 : code, html, err);
    });
    pandoc.stdin.write(md);
    pandoc.stdin.end();
}
