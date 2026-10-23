# Rack SSH connection ownership

Reserve the SSH host name `rack` for interactive access from bahamut. OpenSSH owns
one shared transport and its reverse forward. Background services use their own
host names, such as `rack-searxng`, with `HostName rack` and `User dzack`.

Replace the workstation's existing `Host rack` forwarding block with the following.
Place it before broad `Host *` defaults: OpenSSH uses the first value for scalar
options. Keep exactly one RemoteForward declaration for this endpoint.

```sshconfig
Host rack
    User dzack
    ControlMaster auto
    ControlPath /run/user/1000/rack-interactive-%C
    ControlPersist 1s
    RemoteForward 127.0.0.1:2222 127.0.0.1:22222
    ExitOnForwardFailure yes
    ServerAliveInterval 15
    ServerAliveCountMax 3
```

Configure Kitty's `~/.config/kitty/ssh.conf`:

```text
hostname rack dzack@rack
share_connections no
```

This makes OpenSSH configuration govern sharing across Kitty windows and terminal
instances. Each shell attaches to the shared master. The master shuts down after
one second without client sessions. That explicit grace period is the lifecycle
boundary; this is not instantaneous revocation. A broken network connection also
requires failure detection rather than immediate teardown.

The local `reverse-sshd.service` listens on loopback port 22222. Rack agents use
their dedicated key to reach it through rack loopback port 2222. Its forwarding
permission is limited to the workstation's Zotero API at `127.0.0.1:23119`.

## Acceptance checks

Check `ssh -G rack` for the exact master, socket, persistence, and forwarding
options. Check the effective background service profile for absence of that
reverse forward. Open separate rack shells, close the first, then close the last.
The reverse endpoint must survive the first close and disappear after the last
session and the grace period. Repeat with an active rack-to-workstation connection.
Verify Zotero's `/version` response from rack while connected.

## Installation boundary

The workstation SSH configuration and Kitty settings must both be installed before
this design is active. A host configuration edit requires access to
`~/.ssh/config`; the agent's safety hook currently rejects access to that file.

## Reference

[OpenSSH ssh_config](https://man.openbsd.org/ssh_config) defines ControlMaster,
ControlPath, ControlPersist, and RemoteForward.
[Kitty SSH](https://sw.kovidgoyal.net/kitty/kittens/ssh/) defines share_connections.
