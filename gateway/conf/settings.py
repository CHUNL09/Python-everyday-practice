import os
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB={
    'connector':'mysql+pymysql://root:aircool@127.0.0.1:3306/gateway',
    'max_session':5
}

PROCESS_POOL_SIZE=5
#SERVER_CONF=""
SERVER_CONF="%s/conf/server_config.py" %BASE_DIR
GROUP_CONF="%s/conf/group_config.py" %BASE_DIR
LOCAL_PATH="%s/download" %BASE_DIR
DATA_SOURCE="%s/data_source" %BASE_DIR