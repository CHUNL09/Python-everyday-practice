from module.db_ops import session
from module import db_ops
import datetime

def log_record(gateway_user,host_user_id,log_msg):
    date=datetime.datetime.now()
    log=db_ops.AuditLog(gateway_user_id=gateway_user,host_user_id=host_user_id,date=date,
                        log_msg=log_msg)
    session.add(log)
    session.commit()