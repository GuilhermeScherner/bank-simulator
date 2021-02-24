from odmantic import Model
from typing import Optional

class History(Model):
    topic: Optional[str]
    partition: Optional[str]
    offset: Optional[str]
    key: Optional[str]
    value: Optional[str]
    timestamp: Optional[str]
