#!/usr/bin/env bash
set -euo pipefail

# Captive-portal login page captured from the browser redirect.
LOGIN_URL="${LOGIN_URL:-http://172.16.254.250/cgi-bin/login?cmd=login&mac=e0:2e:0b:08:fb:24&ip=10.1.203.109&essid=NCTS%2DVISITOR&apname=f4%3A2e%3A7f%3Ac4%3Ae9%3A60&apgroup=default&url=http%3A%2F%2Fconnectivitycheck%2Egstatic%2Ecom%2Fgenerate%5F204}"

# Provide credentials via env vars or hardcode here.
USERNAME="${USERNAME:-}"
PASSWORD="${PASSWORD:-}"

if [[ -z "$USERNAME" || -z "$PASSWORD" ]]; then
  echo "Set USERNAME and PASSWORD env vars (or edit this file) before running." >&2
  exit 1
fi

python3 - "$LOGIN_URL" "$USERNAME" "$PASSWORD" <<'PY'
import sys
import re
import urllib.parse
import urllib.request
import http.cookiejar
import html.parser

login_url, user, pwd = sys.argv[1:4]

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Fetch the login page so we can grab the form, hidden fields, and cookies.
resp = opener.open(login_url)
html = resp.read().decode("utf-8", "ignore")
base_url = resp.geturl()


class FormFinder(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_form = False
        self.form_attrs = {}
        self.inputs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == "form" and not self.in_form:
            self.in_form = True
            self.form_attrs = attrs
        if self.in_form and tag.lower() == "input":
            self.inputs.append(attrs)

    def handle_endtag(self, tag):
        if tag.lower() == "form" and self.in_form:
            self.in_form = False


parser = FormFinder()
parser.feed(html)
inputs = parser.inputs

if not inputs:
    print("Login form not found; no inputs detected.", file=sys.stderr)
    sys.exit(2)


def pick_user_field():
    for attr in inputs:
        name = attr.get("name") or ""
        if re.search(r"user|email|login", name, re.I):
            return name
    for attr in inputs:
        if attr.get("type", "text").lower() in ("text", "email") and attr.get("name"):
            return attr["name"]
    return None


def pick_pass_field():
    for attr in inputs:
        if attr.get("type", "").lower() == "password" and attr.get("name"):
            return attr["name"]
    for attr in inputs:
        name = attr.get("name") or ""
        if re.search(r"pass", name, re.I):
            return name
    return None


user_field = pick_user_field()
pass_field = pick_pass_field()

if not user_field or not pass_field:
    print("Could not identify username/password fields; found names:", [i.get("name") for i in inputs], file=sys.stderr)
    sys.exit(3)

payload = {}
for attr in inputs:
    name = attr.get("name")
    if not name:
        continue
    itype = (attr.get("type") or "").lower()
    if name == user_field:
        payload[name] = user
    elif name == pass_field:
        payload[name] = pwd
    elif itype == "submit":
        payload[name] = attr.get("value", "Login")
    else:
        payload[name] = attr.get("value", "")

action = parser.form_attrs.get("action", "") if parser.form_attrs else ""
method = parser.form_attrs.get("method", "POST").upper() if parser.form_attrs else "POST"
target = urllib.parse.urljoin(base_url, action) if action else base_url

encoded = urllib.parse.urlencode(payload)

if method == "GET":
    sep = "&" if urllib.parse.urlparse(target).query else "?"
    target = f"{target}{sep}{encoded}"
    req = urllib.request.Request(target)
else:
    req = urllib.request.Request(target, data=encoded.encode())
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

with opener.open(req) as resp2:
    sys.stdout.write(f"{resp2.status} {resp2.reason}\n")
    sys.stdout.write(f"Posted to: {resp2.geturl()}\n")
    sys.stdout.buffer.write(resp2.read(4000))
PY
