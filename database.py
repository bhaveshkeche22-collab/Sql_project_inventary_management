

    
import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.environ["gateway01.ap-northeast-1.prod.aws.tidbcloud.com"],
        user=os.environ["46oCbGv85sjBpSm.root"],
        password=os.environ["fZzRhQdTgYPeOko9"],
        database=os.environ["sys"],
        port=int(os.environ.get("DB_PORT", "4000")),
        ssl_disabled=False
    )
