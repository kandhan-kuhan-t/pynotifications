import logging.handlers
import os.path

# logging.dis
logging._srcfile = None
logging.logThreads = 0
logging.logProcesses = 0

FILE_DIR = '/var/log/pyNotifications'
DEFAULT_FILE_MODE = 'a'
BACKUP_COUNT = 10
MAX_BYTES = 1000000


default_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(default_formatter)

# debug_file_handler = logging.handlers.RotatingFileHandler(
#     filename=os.path.join(FILE_DIR, 'debug.log'), mode=DEFAULT_FILE_MODE, backupCount=BACKUP_COUNT, maxBytes=MAX_BYTES
# )
info_file_handler = logging.handlers.RotatingFileHandler(
    filename=os.path.join(FILE_DIR, 'info.log'), mode=DEFAULT_FILE_MODE, backupCount=BACKUP_COUNT, maxBytes=MAX_BYTES
)
exception_file_handler = logging.handlers.RotatingFileHandler(
    filename=os.path.join(FILE_DIR, 'exception.log'), mode=DEFAULT_FILE_MODE, backupCount=BACKUP_COUNT, maxBytes=MAX_BYTES
)


# debug_file_handler.setLevel(logging.DEBUG)
info_file_handler.setLevel(logging.INFO)
exception_file_handler.setLevel(logging.ERROR)

# debug_file_handler.setFormatter(default_formatter)
info_file_handler.setFormatter(default_formatter)
console_handler.setFormatter(default_formatter)

local = logging.getLogger('local')
local.addHandler(console_handler)
local.setLevel(logging.DEBUG)

app = logging.getLogger('app')
app.addHandler(info_file_handler)
app.addHandler(exception_file_handler)

mode = 'local'
