# db_manager.py

import os
from pathlib import Path
import sqlite3
from time import time
from elautil import config, dataclasses as dc, logger

class DbUtil:

    @staticmethod
    def connect(database_file):
        connection = None
        try:
            connection = sqlite3.connect(database_file)
        except sqlite3.Error as e:
            connection = None
            print(f"Error connecting to the database: {e}")
        finally:
            return connection
    
    @staticmethod
    def disconnect(connection):
        try:
            if (connection):
                connection.close()
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
        finally:
            connection = None  
        return


class ELAAssessmentAuditDatabase:

    def __init__(self):
        dbname = config.ELA_ASSESSMENTAUDIT_LOCALDB_NAME
        dbdir = config.ELA_LOCALDB_DIR
        if (os.path.exists(dbdir) == False):
            Path(dbdir).mkdir(parents=True)

        self.database_file = os.path.join(dbdir, dbname)
        #logger.debug(f'Creating tables in database {dbname} | file {self.database_file}')
        self.createTable()

    def createTable(self):

        conn = self.connect()
        cursor = conn.cursor()

        ddl_table = """
            CREATE TABLE IF NOT EXISTS ela_audit_t (
            audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            school_code TEXT NOT NULL,
            pkg_id TEXT NOT NULL,
            time INTEGER NOT NULL,
            status INTEGER NOT NULL
        );
        """

        ddl_index = """
            CREATE INDEX IF NOT EXISTS idx_school_code ON ela_audit_t (school_code);
        """

        cursor.executescript(ddl_table)
        cursor.executescript(ddl_index)

        conn.commit()
        self.disconnect(conn)

    def connect(self):
        conn = DbUtil.connect(self.database_file)
        return conn
    
    def disconnect(self, conn):
        DbUtil.disconnect(conn)

    def audit(self,packageMetadata, status: dc.AuditItemStatus):
        audit_time = int(time() * 1000)
        self.insertAuditRecord(packageMetadata.schoolcode,packageMetadata.schoolpkgid,status.value,audit_time)
        return

    def insertAuditRecord(self,school_code,pkg_id, audit_status: dc.AuditItemStatus, audit_time):

        conn = self.connect()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO ela_audit_t (
            school_code, pkg_id, status, time
            ) VALUES (?, ?, ?, ?);
        """
        bind_param_values = (school_code,pkg_id,audit_status,audit_time)
        logger.debug(f'Executing audit log query {insert_query} with parameters {bind_param_values}')

        cursor.execute(insert_query,bind_param_values)

        conn.commit()
        self.disconnect(conn)

        return

class ELAAssessmentDatabase:

    def __init__(self,packageMetadata: dc.PackageMeta):

        dbdir = config.ELA_LOCALDB_DIR
        dbname = packageMetadata.schoolpkgid + '.db'
        if (os.path.exists(dbdir) == False):
            Path(dbdir).mkdir(parents=True)
        
        self.database_file = os.path.join(dbdir, dbname)
        #logger.debug(f'Creating tables in database {dbname} | file {self.database_file}')
        self.createTables()

    def connect(self):
        conn = DbUtil.connect(self.database_file)
        return conn
    
    def disconnect(self, conn):
        DbUtil.disconnect(conn)

    def createTables(self):

        conn = self.connect()
        cursor = conn.cursor()

        ddl_table = """
            CREATE TABLE IF NOT EXISTS ela_assessment_item_t (
            school_code TEXT NOT NULL,
            pkg_id TEXT NOT NULL,
            collected_time INTEGER NOT NULL,
            username TEXT NOT NULL,
            assignmentid TEXT NOT NULL,
            lessonid TEXT NOT NULL,
            attempt_time INTEGER NOT NULL,
            attempt_number INTEGER,
            transcribed_text TEXT NOT NULL,
            word_timings TEXT,
            annotated_text TEXT NOT NULL,
            grammar_analysis TEXT
            );
            """
            #PRIMARY KEY (school_code, username, assignmentid, lessonid, attempt_number)

        ddl_index = """
            CREATE INDEX IF NOT EXISTS idx_school_code ON ela_assessment_item_t (school_code);
        """

        cursor.executescript(ddl_table)
        cursor.executescript(ddl_index)

        conn.commit()
        self.disconnect(conn)

        return

    def save_assessment(self,assessment_item: dc.AssessmentItem):
        
        conn = self.connect()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO ela_assessment_item_t (
            school_code, pkg_id, collected_time, username, assignmentid,
            lessonid, attempt_time, attempt_number, transcribed_text,
            word_timings, annotated_text, grammar_analysis
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        bind_param_values = (assessment_item.schoolcode, assessment_item.pkg_id, 
                assessment_item.collectedtime,assessment_item.username, 
                assessment_item.assignmentid, assessment_item.lessonid,
                assessment_item.attempttime, assessment_item.attemptnumber, 
                assessment_item.asrresult.transcribed_text, assessment_item.asrresult.word_timings, 
                assessment_item.nlpresult.annotated_text, assessment_item.nlpresult.grammar_analysis
        )

        #logger.debug(f'Executing assessment item query {insert_query} with parameters {bind_param_values}')
        cursor.execute(insert_query, bind_param_values)

        conn.commit()
        self.disconnect(conn)

        return
    

    def itemExists(assessment_item):

        duplicate_check_query = """
            SELECT assessment_id, attempt_number, attempt_time FROM ela_assessment_item_t
            WHERE school_code = ? AND username = ? AND assignmentid = ? AND lessonid = ?;
        """

        cursor.execute(duplicate_check_query, (
            assessment_item.schoolcode, assessment_item.username, 
            assessment_item.assignmentid, assessment_item.lessonid
        ))

        assessment_record = cursor.fetchone()

        if assessment_record:
            logger.debug('Possible duplicate submission (re-processing?) detected. Checking')
            assessment_id, attempt_number, attempt_time = assessment_record
            if (attempt_time == assessment_item.attempt_time):
                logger.debug('Data duplicate (re-processing) confirmed. Discarding')
            else:
                logger.debug('Intentional duplicate submission (not re-processing) detected')
                if (attempt_time > assessment_record.attempt_time):
                    logger.debug('An older submission is already present in database. Discarding current submission')
                else:
                    logger.debug('Current submission is older than submission in database. Overwriting submission in database')
                    #TODO
                    #Delete from db. insert this one. Move this to a function and call from save_assessment

            return True

        return False