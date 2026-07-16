#!/usr/bin/env bash

# Forked from artemave/tmux_super_fingers (523dc9b).
# Single entry key (@mega-fingers-key). Inside fingers mode:
#   lowercase hint letter -> open (primary action)
#   shifted  hint letter -> copy (secondary action)
# See panes_renderer.py.

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

DEFAULT_FINGERS_KEY="f"

FINGERS_KEY=$(tmux show-option -gqv @mega-fingers-key)
FINGERS_KEY=${FINGERS_KEY:-$DEFAULT_FINGERS_KEY}

FINGERS_EXTEND=$(tmux show-option -gqv @mega-fingers-extend)

# Clean up stale state from an earlier fork version that bound a separate
# copy-first entry key. Safe no-ops if never set.
tmux unbind-key -T prefix C-S-f 2>/dev/null
tmux set-option -gu @mega-fingers-secondary-key 2>/dev/null

tmux bind "$FINGERS_KEY" new-window -e "FINGERS_EXTEND=$FINGERS_EXTEND" -n mega-fingers "$CURRENT_DIR/run.sh"
