from typing import TypedDict, List

class AutoGraphState(TypedDict, total=False):
    pdf_path: str
    output_path: str
    messages: List[dict]
    topics: List[str]
    current_topic_index: int
    current_session_index: int
    current_episode_index: int
