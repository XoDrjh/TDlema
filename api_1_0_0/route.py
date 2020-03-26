from flask import jsonify, request, abort
from . import api
from . import method
import logging
from datetime import datetime
# request.args.get('') request.json.get('')

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

@api.route('/getuserinfo/stuff', methods=['GET'])
def GetStuffInfo():
    openid = request.args.get('openid')
    logging.info('Get openid : ' + str(openid))
    status, stuff_id, name = method.GetStuffInfo(openid)
    res = {'status': status,
           'stuff_info': {'stuff_id': stuff_id,
                          'name': name}}
    logging.info('Return : ' + str(res))
    return jsonify(res)

@api.route('/verify/stu', methods=['POST'])
def VerifyStu():
    openid = request.json.get('openid')
    stu_id = request.json.get('stu_id')
    name = request.json.get('name')
    logging.info('Get openid : ' + str(openid))
    logging.info('Get stu_id : ' + str(stu_id))
    logging.info('Get name : ' + str(name))
    status, bind_status, stu_id, name, stu_class = method.VerifyStu(openid, stu_id, name)
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

@api.route('/verify/stuff', methods=['POST'])
def VerifyStuff():
    openid = request.json.get('openid')
    stuff_id = request.json.get('stuff_id')
    name = request.json.get('name')
    logging.info('Get openid : ' + str(openid))
    logging.info('Get stuff_id : ' + str(stuff_id))
    logging.info('Get name : ' + str(name))
    status, bind_status, stuff_id, name = method.VerifyStuff(openid, stuff_id, name)
    if bind_status is True:
        res = {'status': status,
               'bind_status': bind_status,
               'stuff_info': {'stuff_id': stuff_id,
                              'name': name}}
    else:
        res = {'status': status, 'bind_status': bind_status}
    logging.info('Return : ' + str(res))
    return jsonify(res)

@api.route('/cancelbanding', methods=['POST'])
def CancelBanding():
    user_id = request.json.get('user_id')
    logging.info('Get : ' + str(user_id))
    status, cancel_status = method.CancelBanding(user_id)
    res = {'status': status, 'cancel_status': cancel_status}
    logging.info('Return : ' + str(res))
    return jsonify(res)

@api.route('/getcourseinfo/stu', methods=['GET'])
def GetCourseInfoStu():
    stu_id = request.args.get('stu_id')
    logging.info('Get : ' + str(stu_id))
    status, current, _next = method.GetCourseInfoStu(stu_id)
    res = {'status': status, 'current': current, 'next': _next}
    logging.info('Return : ' + str(res))
    return jsonify(res)

@api.route('/getcourserecord/stuff', methods=['GET'])
def GetCourseRecordStuff():
    stuff_id = request.args.get('stuff_id')
    logging.info('Get : ' + str(stuff_id))
    status, course_record = method.GetCourseRecordStuff(stuff_id)
    res = {'status': status, 'course_record': course_record}
    logging.info('Return : ' + str(res))
    return jsonify(res)

@api.route('/getsignininfo/stu', methods=['GET'])
def GetSignInInfoStu():
    stu_id = request.args.get('stu_id')
    logging.info('Get : ' + str(stu_id))
    status, sign_in_info = method.GetSignInInfoStu(stu_id)
    res = {'status': status, 'sign_in_info': sign_in_info}
    logging.info('Return : ' + str(res))
    return jsonify(res)

@api.route('/getsignininfo/stuff', methods=['GET'])
def GetSignInInfoStuff():
    dyn_course_id = request.args.get('dyn_course_id')
    logging.info('Get : ' + str(dyn_course_id))
    status, sign_in_info = method.GetSignInInfoStuff(dyn_course_id)
    res = {'status': status, 'sign_in_info': sign_in_info}
    logging.info('Return : ' + str(res))
    return jsonify(res)

@api.route('/getrealtimeinfo/stuff', methods=['GET'])
def GetRealTimeInfoStuff():
    stuff_id = request.args.get('stuff_id')
    logging.info('Get : ' + str(stuff_id))
    status, current, _next = method.GetRealTimeInfoStuff(stuff_id)
    res = {'status': status, 'current': current, 'next': _next}
    logging.info('Return : ' + str(res))
    return jsonify(res)

@api.route('/gethistoryrecord/stu', methods=['GET'])
def GetHistoryRecord():
    stu_id = request.args.get('stu_id')
    logging.info('Get : ' + str(stu_id))
    status, history_record = method.GetHistoryRecord(stu_id)
    res = {'status': status, 'history_record': history_record}
    logging.info('Return : ' + str(res))
    return jsonify(res)

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