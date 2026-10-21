// Actions & Tags script action: send the selected items' PDFs to the Kindle.
//
// Runs inside Zotero with `item`, `items`, `collection`, `require`, `triggerType`
// in scope (see windingwind/zotero-actions-tags, src/utils/actions.ts). Installed
// into the running Zotero with:
//
//   zotero-action-install --name "Send to Kindle" --shortcut accel,shift,k \
//       zotero/actions/send-to-kindle.js
//
// Delivery is `bin/kindle-send`, which must already be logged in. Failures land in
// ~/.local/state/kindle-send/sends.log; Zotero only shows the exit status.
//
// The plugin dispatches a menu or shortcut trigger twice: once with `items` set to
// the whole selection, then once per item with `items` empty. Only the first
// dispatch does work here, so each selected PDF is sent once.
const KINDLE_SEND = "/home/dzack/dotfiles/bin/kindle-send";

if (!items || !items.length) {
  return;
}
const sent = [];
const skipped = [];
for (const it of items) {
  let attachment = null;
  if (it.isAttachment()) {
    attachment = it;
  } else if (it.isRegularItem()) {
    attachment = await it.getBestAttachment();
  }
  if (!attachment || !attachment.isPDFAttachment()) {
    skipped.push(it.getField("title"));
    continue;
  }
  const path = await attachment.getFilePathAsync();
  if (!path) {
    skipped.push(it.getField("title"));
    continue;
  }
  const parent = attachment.parentItem || attachment;
  const title = parent.getField("title") || attachment.getField("title");
  const author = parent.isRegularItem() ? parent.firstCreator : "";
  await Zotero.Utilities.Internal.exec(KINDLE_SEND, [
    "send", "--title", title, "--author", author, path,
  ]);
  sent.push(title);
}
let message = `Sent to Kindle: ${sent.length}`;
if (skipped.length) {
  message += `; no PDF: ${skipped.join("; ")}`;
}
return message;
