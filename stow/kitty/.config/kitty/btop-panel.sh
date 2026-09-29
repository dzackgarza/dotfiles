#!/bin/bash
# Launch btop as a kitty panel using examples from the official documentation

# As a transparent desktop background (from the documentation)
kitten panel --edge=background -o background_opacity=0.2 -o background=black btop

# Other options you can try:
# kitten panel --edge=top --lines=10 btop
# kitten panel --edge=bottom --lines=10 btop
# kitten panel --edge=left --lines=30 btop
# kitten panel --edge=right --lines=30 btop

# With remote control enabled:
# kitten panel -o allow_remote_control=socket-only --lines=10 --listen-on=unix:/tmp/btop-panel btop