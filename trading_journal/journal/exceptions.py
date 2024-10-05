from trading_journal.core.exceptions import CoreError
from trading_journal.journal import messages


class PositionAlreadyExistsError(CoreError):
    error_message = messages.POSITION_ALREADY_EXISTS


class PositionNotClosedError(CoreError):
    error_message = messages.POSITION_NOT_CLOSED


class TemporalDisturbanceError(CoreError):
    error_message = messages.TEMPORAL_DISTURBANCE
