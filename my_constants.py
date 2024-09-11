ISDEBUG=1

#--- Error codes
# _LEVELTONAME = {
#     CRITICAL: 'CRITICAL',
#     ERROR:    'ERROR',
#     WARNING:  'WARNING',
#     INFO:     'INFO',
#     DEBUG:    'DEBUG',
#     NOTSET:   'NOTSET',
# }

CONSOLE_LOG_LEVEL='ERROR'
LOGFILE_LOG_LEVEL='DEBUG'
LOG_DIR='logs'
LOG_FILE_NAME='log_file.log'
LOG_FILE_MAXBYTES=1000000
LOG_FILE_BACKUP_COUNT=10
# CONSOLE_ENTRY_FORMAT_STRING='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s'
CONSOLE_ENTRY_FORMAT_STRING='%(levelname)s :: %(name)s :: %(message)s'
# LOGFILE_ENTRY_FORMAT_STRING='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s'
# LOGFILE_ENTRY_FORMAT_STRING='%(asctime)s :: %(levelname)-8s :: %(name)s: :: %(filename)s:%(lineno)s | %(process)d >>> %(message)s'
# LOGFILE_ENTRY_FORMAT_STRING: '%(asctime)s :: %(levelname)-8s :: %(name)-12s :: %(message)s', 
# LOGFILE_ENTRY_FORMAT_STRING: '%(asctime)s :: %(levelname)-7s :: %(name)-15s :: %(message)s', 
LOGFILE_ENTRY_FORMAT_STRING='%(asctime)-24s :: %(levelname)-8s :: %(filename)-20s:%(lineno)-5s | %(process)d >>> %(message)s'

SUPPORTED_IN_FORMATS=[".jpg", ".jpeg", ".jfif", ".png", ".gif", ".webp", ".png", ".heif", ".heifs", ".heic"]
UNSUPPORTED_OUT_FORMATS=[".heif", ".heifs", ".heic"]

JPEG_QUALITY_IN_PERCENT=98
DEFAULT_JPEG_QUALITY_IN_PERCENT=-666
