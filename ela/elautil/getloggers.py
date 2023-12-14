import logging

# Get a list of all active logger names
active_logger_names = [logger.name for logger in logging.Logger.manager.loggerDict.values() if isinstance(logger, logging.Logger)]

print(active_logger_names)
