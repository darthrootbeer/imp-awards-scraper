#!/usr/bin/env python3
"""
Digest tracking utilities for IMP Awards email digest workflow.

Stores identifiers for posters that have already been processed or emailed
so subsequent runs only target new additions.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Iterable, List, Set


class DigestTracker:
    """Persists state about which poster IDs have been handled."""

    def __init__(self, state_file: str = "digest_state.json", history_limit: int = 500) -> None:
        self.state_file = state_file
        self.history_limit = history_limit
        self.state = {
            "sent_ids": [],       # type: List[str]
            "ignored_ids": [],    # type: List[str]
            "last_run": None
        }
        self._load()

    # --------------------------------------------------------------------- #
    # Persistence helpers
    # --------------------------------------------------------------------- #

    def _load(self) -> None:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    if isinstance(data, dict):
                        self.state.update({
                            "sent_ids": data.get("sent_ids", []),
                            "ignored_ids": data.get("ignored_ids", []),
                            "last_run": data.get("last_run")
                        })
            except Exception:
                # Corrupt or unreadable file; start fresh but keep backup.
                backup_path = f"{self.state_file}.bak"
                try:
                    os.rename(self.state_file, backup_path)
                except OSError:
                    pass

    def save(self) -> None:
        tmp_path = f"{self.state_file}.tmp"
        self.state["last_run"] = datetime.utcnow().isoformat()
        with open(tmp_path, "w", encoding="utf-8") as fh:
            json.dump(self.state, fh, indent=2)
        os.replace(tmp_path, self.state_file)

    # --------------------------------------------------------------------- #
    # State queries
    # --------------------------------------------------------------------- #

    def get_known_ids(self) -> Set[str]:
        """Return IDs that have already been handled (sent or ignored)."""
        return set(self.state["sent_ids"]) | set(self.state["ignored_ids"])

    def get_last_sent_ids(self) -> List[str]:
        """Return the ordered list of IDs included in the last successful digest."""
        return list(self.state["sent_ids"])

    # --------------------------------------------------------------------- #
    # State updates
    # --------------------------------------------------------------------- #

    def record_sent(self, ids: Iterable[str]) -> None:
        """Record poster IDs that were emailed successfully."""
        for poster_id in reversed(list(ids)):
            self._remove_if_present(poster_id)
            self.state["sent_ids"].insert(0, poster_id)
        self._trim_history()

    def record_ignored(self, ids: Iterable[str]) -> None:
        """Record poster IDs that were processed but not emailed."""
        for poster_id in reversed(list(ids)):
            if poster_id in self.state["sent_ids"]:
                continue
            self._remove_from_list(poster_id, self.state["ignored_ids"])
            self.state["ignored_ids"].insert(0, poster_id)
        self._trim_history()

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #

    def _remove_if_present(self, poster_id: str) -> None:
        self._remove_from_list(poster_id, self.state["sent_ids"])
        self._remove_from_list(poster_id, self.state["ignored_ids"])

    @staticmethod
    def _remove_from_list(poster_id: str, target: List[str]) -> None:
        try:
            target.remove(poster_id)
        except ValueError:
            pass

    def _trim_history(self) -> None:
        if len(self.state["sent_ids"]) > self.history_limit:
            del self.state["sent_ids"][self.history_limit :]
        if len(self.state["ignored_ids"]) > self.history_limit:
            del self.state["ignored_ids"][self.history_limit :]
