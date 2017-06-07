import os,logging
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER_ACCOUNT={
    'admin':'admin'
}
PROCESS_POOL_SIZE=5
#SERVER_CONF=""
SERVER_CONF="%s/conf/server_config.py" %BASE_DIR
GROUP_CONF="%s/conf/group_config.py" %BASE_DIR
LOG_FILE="%s/log/server.log" %BASE_DIR
LOG_FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL= logging.INFO
LOCAL_PATH="%s/download" %BASE_DIR