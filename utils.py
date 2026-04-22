import logging

logger = logging.getLogger(__name__)


def calculate_internal_metric(a, b):
    try:
        if b == 0:
            raise ValueError("Division by zero is not allowed")

        return a / b

    except Exception as e:
        logger.error(f"Error calculating metric: {e}")
        return None  # safe fallback
