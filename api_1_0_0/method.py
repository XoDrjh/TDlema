from flask import abort
import logging
from . import db
from bson import ObjectId
import datetime

def GetOpenid():
    pass#获取Openid

def CheckSeat(dyn_course_id, row, col, classroom, camps):
    return True#检查座位是否在合法数据范围内

def CheckTime(dyn_course_id, time):
    dyndoc = db.GetDynamicCourseInfo(dyn_course_id=dyn_course_id)
    if time <= dyndoc['_class_time']:
        return 1
    else:
        return 2

def ConversionTime():
    now = datetime.datetime.now()
    t = datetime.time(now.hour, now.minute, now.second)
    if datetime.time(7, 30, 0) <= t < datetime.time(9, 45, 0):
        return datetime.datetime(now.year, now.month, now.day, 8, 0, 0)
    elif datetime.time(9, 45, 0) <= t < datetime.time(12, 0, 0):
        return datetime.datetime(now.year, now.month, now.day, 10, 15, 0)
    elif datetime.time(13, 30, 0) <= t < datetime.time(15, 45, 0):
        return datetime.datetime(now.year, now.month, now.day, 14, 0, 0)
    elif datetime.time(15, 45, 0) <= t < datetime.time(18, 0, 0):
        return datetime.datetime(now.year, now.month, now.day, 16, 15, 0)
    elif datetime.time(18, 15, 0) <= t < datetime.time(20, 30, 0):
        return datetime.datetime(now.year, now.month, now.day, 18, 45, 0)

def GetStudentInfo(openid):
    if openid is None:
        return 2, None, None, None
    else:
        openid = str(openid)
        studentdoc = db.GetUser(openid)
        if studentdoc is None:
            return 1, None, None, None
        else:
            return 0, studentdoc['_id'], studentdoc['_name'], studentdoc['_class']

def GetStuffInfo(openid):
    if openid is None:
        return 2, None, None
    else:
        openid = str(openid)
        stuffdoc = db.GetUser(openid)
        if stuffdoc is None:
            return 1, None, None
        else:
            return 0, stuffdoc['_id'], stuffdoc['_name']

def VerifyStu(openid, stu_id, name):
    if None in (openid, stu_id, name):
        return 2, None, None, None, None
    else:
        openid = str(openid)
        stu_id = str(stu_id)
        name = str(name)
        ans = db.BindOpenid(openid, stu_id, name)
        if ans is None:
            return 1, None, None, None, None
        elif ans is False:
            return 0, False, None, None, None
        else:
            return 0, True, ans['_id'], ans['_name'], ans['_class']

def VerifyStuff(openid, stuff_id, name):
    if None in (openid, stuff_id, name):
        return 2, None, None, None
    else:
        openid = str(openid)
        stuff_id = str(stuff_id)
        name = str(name)
        ans = db.BindOpenid(openid, stuff_id, name)
        if ans is None:
            return 1, None, None, None
        elif ans is False:
            return 0, False, None, None
        else:
            return 0, True, ans['_id'], ans['_name']

def CancelBanding(user_id):
    if user_id is None:
        return 2, None
    else:
        user_id = str(user_id)
        ans = db.CancelBinding(user_id)
        if ans is None:
            return 1, None
        else:
            return 0, ans

def FormCourseInfoStu(dyndoc, stu_id):
    userdoc = db.GetUser(id=dyndoc['_lecturer_id'])
    basecoursedoc = db.GetBaseCourseInfo(dyndoc['_base_course_id'])
    course_info = {'base_course_id': dyndoc['_base_course_id'],
                   'dyn_course_id': dyndoc['_id'],
                   'course_name': basecoursedoc['_course_name'],
                   'lecturer_name': userdoc['_name'],
                   'campus': basecoursedoc['_campus'],
                   'classroom': basecoursedoc['_classroom'],
                   'main_class': basecoursedoc['_main_class'],
                   'week': dyndoc['_week'],
                   'class_time': dyndoc['_class_time']}
    for stu in dyndoc['_stu_set']:
        if stu['_id'] == stu_id:
            course_info['sign_in_status'] = stu['_status']
            break
    return course_info

def GetCourseInfoStu(stu_id):
    if stu_id is None:
        return 2, None, None
    else:
        stu_id = str(stu_id)
        current = {}
        _next = {}
        time = ConversionTime()
        dyndocs = db.GetDynamicCourseInfo(stu_id=stu_id, time=time, cnt=2)
        cur_dyndoc = None
        next_dyndoc = None
        if len(dyndocs) == 0:
            return 1, None, None
        else:
            if dyndocs[0]['_class_time'] == time:
                current['have_classes_or_not'] = True
                cur_dyndoc = dyndocs[0]
                if len(dyndocs) == 2:
                    _next['have_classes_or_not'] = True
                    next_dyndoc = dyndocs[1]
                else:
                    _next['have_classes_or_not'] = False
            else:
                current['have_classes_or_not'] = False
                _next['have_classes_or_not'] = True
                next_dyndoc = dyndocs[0]
        if cur_dyndoc is not None:
            cur_course_info = FormCourseInfoStu(cur_dyndoc, stu_id)
            current['course_info'] = cur_course_info
        if next_dyndoc is not None:
            next_course_info = FormCourseInfoStu(next_dyndoc, stu_id)
            _next['course_info'] = next_course_info
        return 0, current, _next

def FormCourseRecordStuff(dyndoc):
    lecturerdoc = db.GetUser(id=dyndoc['_lecturer_id'])
    counselordoc = db.GetUser(id=dyndoc['_counselor_id'])
    basecoursedoc = db.GetBaseCourseInfo(dyndoc['_base_course_id'])
    course_info = {'base_course_id': dyndoc['_base_course_id'],
                   'dyn_course_id': dyndoc['_id'],
                   'course_name': basecoursedoc['_course_name'],
                   'lecturer_name': lecturerdoc['_name'],
                   'counselor_name': counselordoc['_name'],
                   'campus': basecoursedoc['_campus'],
                   'classroom': basecoursedoc['_classroom'],
                   'main_class': basecoursedoc['_main_class'],
                   'week': dyndoc['_week'],
                   'class_time': dyndoc['_class_time']}
    stu_set = []
    for i in range(len(dyndoc['_stu_set'])):
        dyn_stu = dyndoc['_stu_set'][i]
        base_stu = basecoursedoc['_stu_set'][i]
        stu = {'stu_id': dyn_stu['_id'],
               'sign_in_status': dyn_stu['_status'],
               'remarks': dyn_stu['_remarks'],
               'total_num': base_stu['_total_num'],
               'ontime_num': base_stu['_ontime_num'],
               'late_num': base_stu['_late_num'],
               'absent_num': base_stu['_absent_num'],
               'cheat_num': base_stu['_cheat_num']}
        stu_set.append(stu)
    course_info['stu_set'] = stu_set
    return course_info

def GetCourseRecordStuff(stuff_id):
    if stuff_id is None:
        return 2, None
    else:
        stuff_id = str(stuff_id)
        dyndocs = db.GetDynamicCourseInfo(stuff_id=stuff_id)
        if len(dyndocs) == 0:
            return 1, None
        else:
            course_record = []
            for dyndoc in dyndocs:
                course_info = FormCourseRecordStuff(dyndoc)
                course_record.append(course_info)
            return 0, course_record

def FormSignInInfoStu(signindoc):
    sign_in_info = {'row': signindoc['_row'],
                    'col': signindoc['_col'],
                    'sign_in_time': signindoc['_sign_in_time']}
    return sign_in_info

def GetSignInInfoStu(stu_id):
    if stu_id is None:
        return 2, None
    else:
        stu_id = str(stu_id)
        time = ConversionTime()
        dyndoc = db.GetDynamicCourseInfo(stu_id=stu_id, time=time, cnt=1)
        if dyndoc is None:
            return 1, None
        else:
            signindoc = db.GetSignInInfo(stu_id=stu_id, dyn_course_id=dyndoc['_id'])
            if signindoc is None:
                return 1, None
            else:
                sign_in_info = FormSignInInfoStu(signindoc)
                return 0, sign_in_info

def FormSignInInfoStuff(signindoc):
    sign_in_stu = {'stu_id': signindoc['_stu_id'],
                   'row': signindoc['_row'],
                   'col': signindoc['_col'],
                   'sign_in_time': signindoc['_sign_in_time'],
                   'tags': signindoc['_tags']}
    return sign_in_stu

def GetSignInInfoStuff(dyn_course_id):
    if dyn_course_id is None:
        return 2, None
    else:
        dyn_course_id = ObjectId(dyn_course_id)
        signindocs = db.GetSignInInfo(dyn_course_id=dyn_course_id)
        if signindocs is None:
            return 1, None
        else:
            sign_in_info = []
            for signindoc in signindocs:
                sign_in_stu = FormSignInInfoStuff(signindoc)
                sign_in_info.append(sign_in_stu)
            return 0, sign_in_info

def GetRealTimeInfoStuff(stuff_id):
    if stuff_id is None:
        return 2, None, None
    else:
        stuff_id = str(stuff_id)
        current = {}
        _next = {}
        time = ConversionTime()
        dyndocs = db.GetDynamicCourseInfo(stuff_id=stuff_id, time=time, cnt=2)
        cur_dyndoc = None
        next_dyndoc = None
        if len(dyndocs) == 0:
            return 1, None, None
        else:
            if dyndocs[0]['_class_time'] == time:
                current['have_classes_or_not'] = True
                cur_dyndoc = dyndocs[0]
                if len(dyndocs) == 2:
                    _next['have_classes_or_not'] = True
                    next_dyndoc = dyndocs[1]
                else:
                    _next['have_classes_or_not'] = False
            else:
                current['have_classes_or_not'] = False
                _next['have_classes_or_not'] = True
                next_dyndoc = dyndocs[0]
        if cur_dyndoc is not None:
            cur_course_info = FormCourseRecordStuff(cur_dyndoc)
            current['course_info'] = cur_course_info
            temp, cur_sign_in_data = GetSignInInfoStuff(cur_dyndoc['_id'])
            if temp == 0:
                current['sign_in_data'] = cur_sign_in_data
            else:
                return temp, None, None
        if next_dyndoc is not None:
            next_course_info = FormCourseRecordStuff(next_dyndoc)
            _next['course_info'] = next_course_info
            temp, next_sign_in_data = GetSignInInfoStuff(next_dyndoc['_id'])
            if temp == 0:
                _next['sign_in_data'] = next_sign_in_data
            else:
                return temp, None, None
        return 0, current, _next

def GetHistoryRecord(stu_id):
    if stu_id is None:
        return 2, None
    else:
        stu_id = str(stu_id)
        dyndocs = db.GetDynamicCourseInfo(stu_id=stu_id)
        if len(dyndocs) == 0:
            return 1, None
        else:
            history_record = []
            for dyndoc in dyndocs:
                course_info = FormCourseInfoStu(dyndoc, stu_id)
                signindoc = db.GetSignInInfo(stu_id=stu_id, dyn_course_id=dyndoc['_id'])
                if signindoc is None:
                    return 2, None
                else:
                    sign_in_record = FormSignInInfoStu(signindoc)
                    history_info = {'course_info': course_info, 'sign_in_record': sign_in_record}
                    history_record.append(history_info)
            return 0, history_record

def SignIn(stu_id, dyn_course_id, row, col):
    if None in (stu_id, dyn_course_id, row, col):
        return 2, None, None, None, None
    else:
        stu_id = str(stu_id)
        dyn_course_id = ObjectId(dyn_course_id)
        row = int(row)
        col = int(col)
        if CheckSeat(dyn_course_id, row, col, None, None) is False:
            return 3, None, None, None, None
        else:
            if db.IsSeatEmpty(dyn_course_id, row, col) is False:
                return 0, False, None, None, None
            else:
                t = datetime.datetime.now()
                ans = db.SetSignInInfo(stu_id, dyn_course_id, row, col, t, 0)
                if ans is False:
                    return 4, None, None, None, None
                else:
                    status = CheckTime(dyn_course_id, t)
                    db.SetStuStatus(stu_id, dyn_course_id, status)
                    return 0, True, row, col, t

def DamageReport(row, col, classroom, campus, photo):
    if None in (row, col, classroom, campus, photo):
        return 2
    else:
        row = int(row)
        col = int(col)
        classroom = str(classroom)
        campus = int(campus)
        photo = str(photo)
        if CheckSeat(None, row, col, classroom, campus) is False:
            return 3
        else:
            ans = db.SetDamageReportInfo(row, col, classroom, campus, photo)
            if ans is False:
                return 4
            else:
                return 0

def SwitchSeat(stu_id, dyn_course_id, row, col):
    if None in (stu_id, dyn_course_id, row, col):
        return 2, None, None, None, None
    else:
        stu_id = str(stu_id)
        dyn_course_id = ObjectId(dyn_course_id)
        row = int(row)
        col = int(col)
        if CheckSeat(dyn_course_id, row, col, None, None) is False:
            return 3, None, None, None, None
        else:
            if db.IsSeatEmpty(dyn_course_id, row, col) is False:
                return 0, False, None, None, None
            else:
                ans = db.SwitchSeat(stu_id, dyn_course_id, row, col)
                if ans is None:
                    return 1, None, None, None, None
                else:
                    return 0, True, row, col, ans

def AskForLeave(stu_id, dyn_course_id):
    if None in (stu_id, dyn_course_id):
        return 2, None
    else:
        stu_id = str(stu_id)
        dyn_course_id = ObjectId(dyn_course_id)
        cur_status = db.GetStuStatus(stu_id, dyn_course_id)
        if cur_status is None:
            return 1, None
        elif cur_status == 3:
            return 0, False
        else:
            db.SetStuStatus(stu_id, dyn_course_id, 3)
            return 0, True

def CancelLeave(stu_id, dyn_course_id):
    if None in (stu_id, dyn_course_id):
        return 2, None
    else:
        stu_id = str(stu_id)
        dyn_course_id = ObjectId(dyn_course_id)
        cur_status = db.GetStuStatus(stu_id, dyn_course_id)
        if cur_status is None:
            return 1, None
        elif cur_status != 3:
            return 0, False
        else:
            db.SetStuStatus(stu_id, dyn_course_id, 0)
            return 0, True

def ModifyStuStatus(stu_id, dyn_course_id, target_status):
    if None in (stu_id, dyn_course_id, target_status):
        return 2
    else:
        stu_id = str(stu_id)
        dyn_course_id = ObjectId(dyn_course_id)
        target_status = int(target_status)
        if target_status < 0 or target_status > 6:
            return 3
        else:
            ans = db.SetStuStatus(stu_id, dyn_course_id, target_status)
            if ans is None:
                return 1
            else:
                return 0

def ModifyRemarks(stu_id, dyn_course_id, remarks):
    if None in (stu_id, dyn_course_id, remarks):
        return 2
    else:
        stu_id = str(stu_id)
        dyn_course_id = ObjectId(dyn_course_id)
        remarks = str(remarks)
        ans = db.SetStuRemarks(stu_id, dyn_course_id, remarks)
        if ans is None:
            return 1
        else:
            return 0

def ModifyTags(stu_id, dyn_course_id, tags):
    if None in (stu_id, dyn_course_id, tags):
        return 2
    else:
        stu_id = str(stu_id)
        dyn_course_id = ObjectId(dyn_course_id)
        tags = int(tags)
        if tags < 0 or tags > 3:
            return 3
        else:
            ans = db.SetStuTags(stu_id, dyn_course_id, tags)
            if ans is None:
                return 1
            else:
                return 0