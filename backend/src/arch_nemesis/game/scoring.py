def clamp_delta(value: int, low: int = -10, high: int = 10) -> int:
    return max(low, min(high, value))
