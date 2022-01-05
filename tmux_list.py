#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import json
import libtmux
import sys

from typing import Dict, List, Union, Optional



class TmuxList:
    def __init__(self):
        self.server = libtmux.Server()

    def list_sessions(self, filter_name: Optional[str]=None) -> Dict[str, Union[str, List, Dict]]:
        result = []

        sessions = self.server.list_sessions()
        for session in sessions:
            session_id = session.get("session_id")
            session_name = session.get("session_name")

            if filter_name and not re.match(r".*%s.*" % filter_name, session_name):
                continue

            result.append(
                    {
                        "title": session_name,
                        "subtitle": f"Session {session_name}",
                        "arg": ["session",session_id, session_name],
                        "autocomplete": "",
                        "icon": {
                            "path": "icons/session.ico"
                            }
                        }
                    )
        return result

    def list_windows(self, filter_name: Optional[str]=None) -> Dict[str, Union[str, List, Dict]]:
        result = []

        sessions = self.server.list_sessions()
        for session in sessions:
            session_id = session.get("session_id")
            session_name = session.get("session_name")
            windows = session.list_windows()
            for window in windows:
                window_name = window.get("window_name")
                window_id = window.get("window_id")
                window_index = window.get("window_index")

                if filter_name and not re.match(r".*%s.*" % filter_name, window_name):
                    continue

                result.append(
                        {
                            "title": window_name,
                            "subtitle": f"Window {window_index}:{window_name} in session {session_name}",
                            "arg": ["window", f"{session_id}-{window_id}", window_name],
                            "autocomplete": "",
                            "icon": {
                                "path": "icons/window.ico"
                                }
                            }
                        )
        return result


    def print(self, *args):
        items = []
        for arg in args:
            items.extend(arg)

        print(json.dumps({ "items": items }))



if __name__ == "__main__":
    tmux_list = TmuxList()

    params = sys.argv[1:]
    if not params:
        list_session_result = tmux_list.list_sessions()
        list_window_result = tmux_list.list_windows()
        tmux_list.print(list_session_result, list_window_result)
    else:
        if params[0] == "s":
            list_session_result = tmux_list.list_sessions()
            tmux_list.print(list_session_result)
        elif params[0] == "w":
            list_window_result = tmux_list.list_windows()
            tmux_list.print(list_window_result)
        else:
            filter_name = params[0]
            list_session_result = tmux_list.list_sessions(filter_name)
            list_window_result = tmux_list.list_windows(filter_name)
            tmux_list.print(list_session_result, list_window_result)

