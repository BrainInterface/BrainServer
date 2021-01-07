from typing import Any, List


class ActionService:
    def __init__(self, obs: list) -> None:
        self._obs = obs

    def get_actions(self) -> List[Any]:
        pass
