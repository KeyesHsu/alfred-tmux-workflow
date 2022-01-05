#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import sys
import libtmux

from typing import Tuple



class TmuxType:
    WINDOW = "window"
    SESSION = "session"


class TmuxOpen:
    def __init__(self):
        self.server = libtmux.Server()

    def open(self, tmux_type: TmuxType, tmux_id: str, tmux_name: str):
        if tmux_type == TmuxType.SESSION:
            session  = self.server.get_by_id(tmux_id)
            if not session:
                return

            session.switch_client()

        elif tmux_type == TmuxType.WINDOW:
            session_id, window_id = tmux_id.split("-")
            session  = self.server.get_by_id(session_id)
            window = session.get_by_id(window_id)

            window.select_window()

        else:
            pass


if __name__ == "__main__":
    tmux_open = TmuxOpen()

    params = sys.argv[1:]
    if params:
        tmux_open.open(*params)
    else:
        print("Missing parameters", file=sys.stderr)
