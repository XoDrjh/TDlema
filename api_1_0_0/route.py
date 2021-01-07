from flask import jsonify, request
from . import api
from . import method
import logging
from datetime import datetime
# request.json.get('')     OR     request.json.get('')

# 获取 openid
@api.route('/getopenid', methods=['POST'])
def GetOpenId():
    appid = request.json.get('appid')
    secret = request.json.get('secret')
    js_code = request.json.get('js_code')
    logging.info('Get appid : ' + str(appid))
    logging.info('Get secret : ' + str(secret))
    logging.info('Get js_code : ' + str(js_code))
    status, openid, bind_status, user_id, user_name, user_class = method.GetOpenid(appid, secret, js_code)
    res = {'status': status,
           'openid': openid,
           'bind_status': bind_status,
           'user_info': {'id': user_id,
                         'name': user_name,
                         'class': user_class}}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 获取用户信息-学生
@api.route('/getuserinfo/stu', methods=['GET'])
def GetStudentInfo():
    openid = request.args.get('openid')
    logging.info('Get openid : ' + str(openid))
    status, stu_id, name, stu_class = method.GetStudentInfo(openid)
    res = {'status': status,
           'stu_info': {'stu_id': stu_id,
                        'name': name,
                        'class': stu_class}}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 获取用户信息-教职工
@api.route('/getuserinfo/staff', methods=['GET'])
def GetStaffInfo():
    openid = request.args.get('openid')
    logging.info('Get openid : ' + str(openid))
    status, staff_id, name = method.GetStaffInfo(openid)
    res = {'status': status,
           'staff_info': {'staff_id': staff_id,
                          'name': name}}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 身份验证-学生
@api.route('/verify/stu', methods=['POST'])
def VerifyStu():
    openid = request.json.get('openid')
    stu_id = request.json.get('stu_id')
    identify = request.json.get('identify')
    logging.info('Get openid : ' + str(openid))
    logging.info('Get stu_id : ' + str(stu_id))
    logging.info('Get identify : ' + str(identify))
    status, bind_status, stu_id, name, stu_class = method.VerifyStu(openid, stu_id, identify)
    if bind_status is True:
        res = {'status': status,
               'bind_status': bind_status,
               'stu_info': {'stu_id': stu_id,
                            'name': name,
                            'class': stu_class}}
    else:
        res = {'status': status, 'bind_status': bind_status}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 身份验证-教职工
@api.route('/verify/staff', methods=['POST'])
def VerifyStaff():
    openid = request.json.get('openid')
    staff_id = request.json.get('staff_id')
    identify = request.json.get('identify')
    logging.info('Get openid : ' + str(openid))
    logging.info('Get staff_id : ' + str(staff_id))
    logging.info('Get identify : ' + str(identify))
    status, bind_status, staff_id, name = method.VerifyStaff(openid, staff_id, identify)
    if bind_status is True:
        res = {'status': status,
               'bind_status': bind_status,
               'staff_info': {'staff_id': staff_id,
                              'name': name}}
    else:
        res = {'status': status, 'bind_status': bind_status}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 解除绑定
@api.route('/cancelbanding', methods=['POST'])
def CancelBanding():
    user_id = request.json.get('user_id')
    logging.info('Get : ' + str(user_id))
    status, cancel_status = method.CancelBanding(user_id)
    res = {'status': status, 'cancel_status': cancel_status}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 获取课程信息-学生
@api.route('/getcourseinfo/stu', methods=['GET'])
def GetCourseInfoStu():
    stu_id = request.args.get('stu_id')
    logging.info('Get : ' + str(stu_id))
    status, current, _next = method.GetCourseInfoStu(stu_id)
    res = {'status': status, 'current': current, 'next': _next}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 获取课程信息-教职工
@api.route('/getcourserecord/staff', methods=['GET'])
def GetCourseRecordStaff():
    staff_id = request.args.get('staff_id')
    logging.info('Get : ' + str(staff_id))
    status, course_record = method.GetCourseRecordStaff(staff_id)
    res = {'status': status, 'course_record': course_record}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 获取某一动态课程详细信息-教职工
@api.route('/getcourserecord/staff/dyncourse', methods=['GET'])
def GetCourseRecordStaffDyncourse():
    dyn_course_id = request.args.get('dyn_course_id')
    logging.info('Get : ' + str(dyn_course_id))
    status, course_record = method.GetCourseRecordStaffDyncourse(dyn_course_id)
    res = {'status': status, 'course_record': course_record}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 获取签到信息-学生
@api.route('/getsignininfo/stu', methods=['GET'])
def GetSignInInfoStu():
    stu_id = request.args.get('stu_id')
    logging.info('Get : ' + str(stu_id))
    status, sign_in_info = method.GetSignInInfoStu(stu_id)
    res = {'status': status, 'sign_in_info': sign_in_info}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 获取签到信息-教职工
@api.route('/getsignininfo/staff', methods=['GET'])
def GetSignInInfoStaff():
    dyn_course_id = request.args.get('dyn_course_id')
    logging.info('Get : ' + str(dyn_course_id))
    status, sign_in_info = method.GetSignInInfoStaff(dyn_course_id)
    res = {'status': status, 'sign_in_info': sign_in_info}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 获取当前课程信息+签到数据-教职工
@api.route('/getrealtimeinfo/staff', methods=['GET'])
def GetRealTimeInfoStaff():
    staff_id = request.args.get('staff_id')
    logging.info('Get : ' + str(staff_id))
    status, current, _next = method.GetRealTimeInfoStaff(staff_id)
    res = {'status': status, 'current': current, 'next': _next}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 获取过去课程信息+签到数据-学生
@api.route('/gethistoryrecord/stu', methods=['GET'])
def GetHistoryRecord():
    stu_id = request.args.get('stu_id')
    logging.info('Get : ' + str(stu_id))
    status, history_record = method.GetHistoryRecord(stu_id)
    res = {'status': status, 'history_record': history_record}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 签到
@api.route('/signin', methods=['POST'])
def SignIn():
    stu_id = request.json.get('stu_id')
    dyn_course_id = request.json.get('dyn_course_id')
    row = request.json.get('row')
    col = request.json.get('col')
    logging.info('Get : ' + str(stu_id))
    logging.info('Get : ' + str(dyn_course_id))
    logging.info('Get : ' + str(row))
    logging.info('Get : ' + str(col))
    status, sign_in_status, row, col, sign_in_time = method.SignIn(stu_id, dyn_course_id, row, col)
    res = {'status': status,
           'sign_in_status': sign_in_status,
           'sign_in_info': {'row': row,
                            'col': col,
                            'sign_in_time': sign_in_time}}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 报修
@api.route('/damagereport', methods=['POST'])
def DamageReport():
    row = request.json.get('row')
    col = request.json.get('col')
    classroom = request.json.get('classroom')
    campus = request.json.get('campus')
    photo = request.json.get('photo')
    logging.info('Get : ' + str(row))
    logging.info('Get : ' + str(col))
    logging.info('Get : ' + str(classroom))
    logging.info('Get : ' + str(campus))
    logging.info('Get : ' + str(photo))
    status = method.DamageReport(row, col, classroom, campus, photo)
    res = {'status': status}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 换座
@api.route('/switchseat', methods=['POST'])
def SwitchSeat():
    stu_id = request.json.get('stu_id')
    dyn_course_id = request.json.get('dyn_course_id')
    row = request.json.get('row')
    col = request.json.get('col')
    logging.info('Get : ' + str(stu_id))
    logging.info('Get : ' + str(dyn_course_id))
    logging.info('Get : ' + str(row))
    logging.info('Get : ' + str(col))
    status, switch_status, row, col, sign_in_time = method.SwitchSeat(stu_id, dyn_course_id, row, col)
    res = {'status': status, 'switch_status': switch_status}
    if switch_status is True:
        res['sign_in_info'] = {'row': row, 'col': col, 'sign_in_time': sign_in_time}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 请假
@api.route('/askforleave', methods=['POST'])
def AskForLeave():
    stu_id = request.json.get('stu_id')
    dyn_course_id = request.json.get('dyn_course_id')
    logging.info('Get : ' + str(stu_id))
    logging.info('Get : ' + str(dyn_course_id))
    status, leave_status = method.AskForLeave(stu_id, dyn_course_id)
    res = {'status': status, 'leave_status': leave_status}
    logging.info('Return :' + str(res))
    return jsonify(res)

# 撤销请假
@api.route('/cancelleave', methods=['POST'])
def CancelLeave():
    stu_id = request.json.get('stu_id')
    dyn_course_id = request.json.get('dyn_course_id')
    logging.info('Get : ' + str(stu_id))
    logging.info('Get : ' + str(dyn_course_id))
    status, cancel_status = method.CancelLeave(stu_id, dyn_course_id)
    res = {'status': status, 'cancel_status': cancel_status}
    logging.info('Return :' + str(res))
    return jsonify(res)

# 更改学生状态
@api.route('/modifystustatus', methods=['POST'])
def ModifyStuStatus():
    stu_id = request.json.get('stu_id')
    dyn_course_id = request.json.get('dyn_course_id')
    target_status = request.json.get('target_status')
    logging.info('Get : ' + str(stu_id))
    logging.info('Get : ' + str(dyn_course_id))
    logging.info('Get : ' + str(target_status))
    status = method.ModifyStuStatus(stu_id, dyn_course_id, target_status)
    res = {'status': status}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 修改备注
@api.route('/modifyremarks', methods=['POST'])
def ModifyRemarks():
    stu_id = request.json.get('stu_id')
    dyn_course_id = request.json.get('dyn_course_id')
    remarks = request.json.get('remarks')
    logging.info('Get : ' + str(stu_id))
    logging.info('Get : ' + str(dyn_course_id))
    logging.info('Get : ' + str(remarks))
    status= method.ModifyRemarks(stu_id, dyn_course_id, remarks)
    res = {'status': status}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 修改状态标签
@api.route('/modifytags', methods=['POST'])
def ModifyTags():
    stu_id = request.json.get('stu_id')
    dyn_course_id = request.json.get('dyn_course_id')
    tags = request.json.get('tags')
    logging.info('Get : ' + str(stu_id))
    logging.info('Get : ' + str(dyn_course_id))
    logging.info('Get : ' + str(tags))
    status = method.ModifyRemarks(stu_id, dyn_course_id, tags)
    res = {'status': status}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 测试接口
@api.route('/test', methods=['GET', 'POST'])
def Test():
    content = ""
    if request.method == 'GET':
        content = request.args.get('content')
        if content == "":
            content = "NULL"
    elif request.method == 'POST':
        content = request.json.get('content')
        if content == "":
            content = "NULL"
    status = 0
    content = str(content)
    time = datetime.now()
    res = {'status': status, 'time': time, 'content': content}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 导入基础课程信息
@api.route('/importBaseCourse', methods=['POST'])
def ImportBaseCourse():
    course_name = request.json.get('course_name')
    lecturer_id = request.json.get('lecturer_id')
    counselor_id = request.json.get('counselor_id')
    campus = request.json.get('campus')
    classroom = request.json.get('classroom')
    main_class = request.json.get('main_class')
    logging.info('Get : ' + str(course_name))
    logging.info('Get : ' + str(lecturer_id))
    logging.info('Get : ' + str(counselor_id))
    logging.info('Get : ' + str(campus))
    logging.info('Get : ' + str(classroom))
    logging.info('Get : ' + str(main_class))
    status = method.ImportBaseCourse(course_name, lecturer_id, counselor_id, campus, classroom, main_class)
    res = {'status': status}
    logging.info('Return : ' + str(res))
    return jsonify(res)

# 导入动态课程信息
@api.route('/importDynamicCourse', methods=['POST'])
def ImportDynamicCourse():
    base_course_id = request.json.get('base_course_id')
    start_week = request.json.get('start_week')
    end_week = request.json.get('end_week')
    classroom = request.json.get('classroom')
    class_time = request.json.get('class_time')
    logging.info('Get : ' + str(base_course_id))
    logging.info('Get : ' + str(start_week))
    logging.info('Get : ' + str(end_week))
    logging.info('Get : ' + str(classroom))
    logging.info('Get : ' + str(class_time))
    status = method.ImportDynamicCourse(base_course_id, start_week, end_week, classroom, class_time)
    res = {'status': status}
    logging.info('Return : ' + str(res))
    return jsonify(res)