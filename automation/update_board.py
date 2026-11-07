"""成绩看板统一刷新，避免多个PR同时写入时丢失其他学生的新成绩。"""
import json,os
from publish_result import refresh_board
students=json.loads(os.environ['CLASS_ROSTER_JSON'])
refresh_board(students)
