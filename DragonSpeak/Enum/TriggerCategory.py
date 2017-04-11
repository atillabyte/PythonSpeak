from enum import IntEnum

class TriggerCategory(IntEnum):
    Undefined = -1
    Cause = 0,
    Condition = 1,
    Area = 3,
    Filter = 4,
    Effect = 5