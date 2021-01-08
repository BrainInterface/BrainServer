from typing import Any, List, Union


class ActionService:

    @classmethod
    def get_actions(cls, request_id: int) -> Union[float, List[Any]]:
        pass

    @classmethod
    def request_actions(cls, observations: List[Any]) -> int:
        pass
