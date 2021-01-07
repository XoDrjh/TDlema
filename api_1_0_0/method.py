from . import db
from bson import ObjectId
import datetime
import requests
import json

# 获取 openid
def GetOpenid(appid, secret, js_code):
    if None in (appid, secret, js_code):
        return 2, None, None, None, None, None
    else:
        text = requests.get(f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={js_code}&grant_type=authorization_code").text
        if not "openid" in str(text):
            return 5, None, None, None, None, None
        else:
            jtext = json.loads(text)
            openid = jtext['openid']
            doc = db.GetUser(openid)
            if doc is None:
                return 0, openid, False, None, None, None
            else:
                if not '_class' in str(doc):
                    return 0, openid, True, doc['_id'], doc['_name'], None
                else:
                    return 0, openid, True, doc['_id'], doc['_name'], doc['_class']

# 检查座位是否在合法数据范围内（前端已校验，这里作废）
def CheckSeat(dyn_course_id, row, col, classroom, camps):
    return True

# 检查时间是否迟到，准点1，迟到2
def CheckTime(dyn_course_id, time):
    dyndoc = db.GetDynamicCourseInfo(dyn_course_id=dyn_course_id)
    if time <= dyndoc['_class_time']:
        return 1
    else:
        return 2

# 将当前时间划分到各个时间节点
def ConversionTime():
    now = datetime.datetime.now()
    t = datetime.time(now.hour, now.minute, now.second)
    if datetime.time(7, 30, 0) <= t < datetime.time(9, 45, 0):
        return datetime.datetime(now.year, now.month, now.day, 8, 0, 0)
    elif datetime.time(9, 45, 0) <= t < datetime.time(12, 0, 0):
        return datetime.datetime(now.year, now.month, now.day, 10, 15, 0)
    elif datetime.time(12, 0, 0) <= t < datetime.time(13, 30, 0):
        return datetime.datetime(now.year, now.month, now.day, 12, 0, 0)
    elif datetime.time(13, 30, 0) <= t < datetime.time(15, 45, 0):
        return datetime.datetime(now.year, now.month, now.day, 14, 0, 0)
    elif datetime.time(15, 45, 0) <= t < datetime.time(18, 0, 0):
        return datetime.datetime(now.year, now.month, now.day, 16, 15, 0)
    elif datetime.time(18, 15, 0) <= t < datetime.time(20, 30, 0):
        return datetime.datetime(now.year, now.month, now.day, 18, 45, 0)
    else:
        return datetime.datetime(now.year, now.month, now.day, 21, 00, 00)
    # return datetime.datetime(2021, 12, 12, 12, 00, 00)  # 测试使用，把时间定在2021年12月12日12:00:00

# 获取学生信息
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

# 获取教职工信息
def GetStaffInfo(openid):
    if openid is None:
        return 2, None, None
    else:
        openid = str(openid)
        staffdoc = db.GetUser(openid)
        if staffdoc is None:
            return 1, None, None
        else:
            return 0, staffdoc['_id'], staffdoc['_name']

# 验证与绑定openid-学生
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
        elif ans == 4:
            return 4, None, None, None, None
        else:
            return 0, True, ans['_id'], ans['_name'], ans['_class']

# 验证与绑定openid-教职工
def VerifyStaff(openid, staff_id, name):
    if None in (openid, staff_id, name):
        return 2, None, None, None
    else:
        openid = str(openid)
        staff_id = str(staff_id)
        name = str(name)
        ans = db.BindOpenid(openid, staff_id, name)
        if ans is None:
            return 1, None, None, None
        elif ans is False:
            return 0, False, None, None
        elif ans == 4:
            return 4, None, None, None
        else:
            return 0, True, ans['_id'], ans['_name']

# 解绑用户openid
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

# 生成课程信息-学生
def FormCourseInfoStu(dyndoc, stu_id):
    userdoc = db.GetUser(id=dyndoc['_lecturer_id'])
    if userdoc is None:
        lecturer_name = None
    else:
        lecturer_name = userdoc['_name']
    basecoursedoc = db.GetBaseCourseInfo(dyndoc['_base_course_id'])
    course_info = {'base_course_id': str(dyndoc['_base_course_id']),
                   'dyn_course_id': str(dyndoc['_id']),
                   'course_name': basecoursedoc['_course_name'],
                   'lecturer_name': lecturer_name,
                   'campus': basecoursedoc['_campus'],
                   'classroom': dyndoc['_classroom'],
                   'main_class': basecoursedoc['_main_class'],
                   'week': dyndoc['_week'],
                   'class_time': dyndoc['_class_time']}
    for stu in dyndoc['_stu_set']:
        if stu['_id'] == stu_id:
            course_info['sign_in_status'] = stu['_status']
            break
    return course_info

# 获取课程信息-学生
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

# 生成课程信息-教师（choice=1不包括学生集合，choice=2包括学生集合）
def FormCourseRecordStaff(dyndoc, choice=1):
    lecturerdoc = db.GetUser(id=dyndoc['_lecturer_id'])
    counselordoc = db.GetUser(id=dyndoc['_counselor_id'])
    basecoursedoc = db.GetBaseCourseInfo(dyndoc['_base_course_id'])
    if lecturerdoc is None:
        lecturer_name = None
    else:
        lecturer_name = lecturerdoc['_name']
    if counselordoc is None:
        counselor_name = None
    else:
        counselor_name = counselordoc['_name']
    if basecoursedoc is None:
        course_name = None
        campus = None
        classroom = None
        main_class = None
    else:
        course_name = basecoursedoc['_course_name']
        campus = basecoursedoc['_campus']
        classroom = dyndoc['_classroom']
        main_class = basecoursedoc['_main_class']
    course_info = {'base_course_id': str(dyndoc['_base_course_id']),
                   'dyn_course_id': str(dyndoc['_id']),
                   'course_name': course_name,
                   'lecturer_name': lecturer_name,
                   'counselor_name': counselor_name,
                   'campus': campus,
                   'classroom': classroom,
                   'main_class': main_class,
                   'week': dyndoc['_week'],
                   'class_time': dyndoc['_class_time']}
    if choice == 2:
        stu_set = []
        for i in range(len(dyndoc['_stu_set'])):
            dyn_stu = dyndoc['_stu_set'][i]
            base_stu = basecoursedoc['_stu_set'][i]
            studoc = db.GetUser(id=dyn_stu['_id'])
            stu = {'stu_id': dyn_stu['_id'],
                   'stu_name': studoc['_name'],
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

# 获取课程信息-教职工
def GetCourseRecordStaff(staff_id):
    if staff_id is None:
        return 2, None
    else:
        staff_id = str(staff_id)
        time = ConversionTime()
        dyndocs = db.GetDynamicCourseInfo(staff_id=staff_id, time=time, cnt=3)
        if len(dyndocs) == 0:
            return 1, None
        else:
            course_record = []
            for dyndoc in dyndocs:
                course_info = FormCourseRecordStaff(dyndoc)
                course_record.append(course_info)
            return 0, course_record

# 获取某一动态课程详细信息-教职工
def GetCourseRecordStaffDyncourse(dyn_course_id):
    if dyn_course_id is None:
        return 2, None
    else:
        dyn_course_id = ObjectId(dyn_course_id)
        dyndoc = db.GetDynamicCourseInfo(dyn_course_id=dyn_course_id)
        if dyndoc is None:
            return 1, None
        else:
            course_info = FormCourseRecordStaff(dyndoc, 2)
            return 0, course_info

# 生成签到表信息-学生
def FormSignInInfoStu(signindoc):
    sign_in_info = {'row': signindoc['_row'],
                    'col': signindoc['_col'],
                    'sign_in_time': signindoc['_sign_in_time']}
    return sign_in_info

# 获取签到信息-学生
def GetSignInInfoStu(stu_id):
    if stu_id is None:
        return 2, None
    else:
        stu_id = str(stu_id)
        time = ConversionTime()
        dyndoc = db.GetDynamicCourseInfo(stu_id=stu_id, time=time)
        if dyndoc is None:
            return 1, None
        else:
            signindoc = db.GetSignInInfo(stu_id=stu_id, dyn_course_id=dyndoc['_id'])
            if signindoc is None:
                return 1, None
            else:
                sign_in_info = FormSignInInfoStu(signindoc)
                return 0, sign_in_info

# 生成签到表信息-教职工
def FormSignInInfoStaff(signindoc):
    studoc = db.GetUser(id=str(signindoc['_stu_id']))
    sign_in_stu = {'stu_id': signindoc['_stu_id'],
                   'stu_name': studoc['_name'],
                   'row': signindoc['_row'],
                   'col': signindoc['_col'],
                   'sign_in_status': db.GetStuStatus(signindoc['_stu_id'], signindoc['_dyn_course_id']),
                   'sign_in_time': signindoc['_sign_in_time'],
                   'tags': signindoc['_tags']}
    return sign_in_stu

# 获取签到信息-教职工
def GetSignInInfoStaff(dyn_course_id):
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
                sign_in_stu = FormSignInInfoStaff(signindoc)
                sign_in_info.append(sign_in_stu)
            return 0, sign_in_info

# 获取当前课程信息 +签到数据-教职工
def GetRealTimeInfoStaff(staff_id):
    if staff_id is None:
        return 2, None, None
    else:
        staff_id = str(staff_id)
        current = {}
        _next = {}
        time = ConversionTime()
        dyndocs = db.GetDynamicCourseInfo(staff_id=staff_id, time=time, cnt=2)
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
            cur_course_info = FormCourseRecordStaff(cur_dyndoc, 2)
            current['course_info'] = cur_course_info
            temp, cur_sign_in_data = GetSignInInfoStaff(cur_dyndoc['_id'])
            if temp == 0:
                current['sign_in_data'] = cur_sign_in_data
            else:
                return temp, None, None
        if next_dyndoc is not None:
            next_course_info = FormCourseRecordStaff(next_dyndoc, 2)
            _next['course_info'] = next_course_info
            temp, next_sign_in_data = GetSignInInfoStaff(next_dyndoc['_id'])
            if temp == 0:
                _next['sign_in_data'] = next_sign_in_data
            else:
                return temp, None, None
        return 0, current, _next

# 获取过去课程信息+签到数据-学生
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
                    sign_in_record = None
                else:
                    sign_in_record = FormSignInInfoStu(signindoc)
                history_info = {'course_info': course_info, 'sign_in_record': sign_in_record}
                history_record.append(history_info)
            return 0, history_record

# 签到
def SignIn(stu_id, dyn_course_id, row, col):
    if None in (stu_id, dyn_course_id, row, col):
        return 2, None, None, None, None
    else:
        stu_id = str(stu_id)
        dyn_course_id = ObjectId(dyn_course_id)
        row = int(row)
        col = int(col)

        mydoc = db.IsSeatEmpty(dyn_course_id, row, col)
        t = datetime.datetime.now()
        ans = db.SetSignInInfo(stu_id, dyn_course_id, row, col, t, 0)
        if ans is False:
            return 4, None, None, None, None
        else:
            if mydoc is not True:
                status = 4
                db.SetStuStatus(stu_id, dyn_course_id, status)
                if len(mydoc) == 1:
                    db.SetStuStatus(mydoc[0]['_stu_id'], dyn_course_id, status)
            else:
                status = CheckTime(dyn_course_id, t)
                db.SetStuStatus(stu_id, dyn_course_id, status)
            return 0, True, row, col, t

# 报修
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

# 换座
def SwitchSeat(stu_id, dyn_course_id, row, col):
    if None in (stu_id, dyn_course_id, row, col):
        return 2, None, None, None, None
    else:
        stu_id = str(stu_id)
        dyn_course_id = ObjectId(dyn_course_id)
        row = int(row)
        col = int(col)
        signin_info = db.GetSignInInfo(stu_id, dyn_course_id)
        if signin_info['_row'] == row and signin_info['_col'] == col:
            return 0, True, row, col, signin_info['_sign_in_time']
        else:
            mydoc = db.IsSeatEmpty(dyn_course_id, row, col)
            ans = db.SwitchSeat(stu_id, dyn_course_id, row, col)
            if ans is None:
                return 1, None, None, None, None
            else:
                if mydoc is not True:
                    status = 4
                    db.SetStuStatus(stu_id, dyn_course_id, status)
                    db.SetStuStatus(mydoc[0]['_stu_id'], dyn_course_id, status)
                else:
                    status = db.GetStuStatus(stu_id, dyn_course_id)
                    if status == 4:
                        status = CheckTime(dyn_course_id, signin_info['_sign_in_time'])
                        db.SetStuStatus(stu_id, dyn_course_id, status)
                mydoc = db.IsSeatEmpty(dyn_course_id, ans['_row'], ans['_col'])
                if mydoc is not True:
                    if len(mydoc) == 1:
                        status = db.GetStuStatus(mydoc[0]['_stu_id'], dyn_course_id)
                        if status == 4:
                            status = CheckTime(dyn_course_id, mydoc[0]['_sign_in_time'])
                            db.SetStuStatus(mydoc[0]['_stu_id'], dyn_course_id, status)
                return 0, True, row, col, ans['_sign_in_time']

# 请假
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

# 撤销请假
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

# 修改某节课学生的状态
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

# 修改某节课学生的状态
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

# 修改某节课学生的状态标签
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

# 导入基础课程信息
def ImportBaseCourse(course_name, lecturer_id, counselor_id, campus, classroom, main_class):
    course_name = str(course_name)
    lecturer_id = str(lecturer_id)
    counselor_id = str(counselor_id)
    campus = int(campus)
    classroom = list(classroom)
    main_class = list(main_class)

    stu_set = []
    for cls in main_class:
        res = db.GetClass(cls)
        for stu in res:
            stu_ = {'_id': stu['_id'],
                    '_default_status': 0,
                    '_total_num': 0,
                    '_ontime_num': 0,
                    '_late_num': 0,
                    '_absent_num': 0,
                    '_cheat_num': 0
                    }
            stu_set.append(stu_)
    return db.SetBaseCourseInfo(course_name, lecturer_id, counselor_id, campus, classroom, main_class, stu_set)

# 导入动态课程信息
def ImportDynamicCourse(base_course_id, start_week, end_week, classroom, class_time):
    base_course_id = ObjectId(base_course_id)
    start_week = int(start_week)
    end_week = int(end_week)
    classroom = str(classroom)
    class_time = list(class_time)
    class_time = datetime.datetime(class_time[0], class_time[1], class_time[2], class_time[3], class_time[4], class_time[5])
    base_course = db.GetBaseCourseInfo(base_course_id)
    lecturer_id = base_course['_lecturer_id']
    counselor_id = base_course['_counselor_id']
    stu_set = []
    for stu in base_course['_stu_set']:
        stu_ = {'_id': stu['_id'],
                '_status': stu['_default_status'],
                '_remarks': ""
                }
        stu_set.append(stu_)
    for week in range(start_week, end_week + 1):
        status = db.SetDynamicCourseInfo(base_course_id, week, classroom, class_time, lecturer_id, counselor_id, stu_set)
        if status is False:
            return False
        else:
            class_time += datetime.timedelta(days=7)
    return True