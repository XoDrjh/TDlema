import pymongo


class DataBase:
    def __init__(self, db_name):
        self.db = pymongo.MongoClient('mongodb://user:password@127.0.0.1', 27017)[db_name]   # 注意：user和password要替换
        # self.db = pymongo.MongoClient('mongodb://127.0.0.1', 27017)[db_name]

    # 获取用户
    def GetUser(self, openid=None, id=None):
        mycol = self.db['User']
        query = {}
        if openid is not None:
            query['_openid'] = openid
        if id is not None:
            query['_id'] = id
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return None
        else:
            return mydoc

    # 获取学生班级
    def GetClass(self, cls):
        mycol = self.db['User']
        query = {'_class': cls}
        mydoc = mycol.find(query)
        if mydoc is None:
            return None
        else:
            return mydoc

    # 获取动态课程信息（cnt : 1-查找正在进行的课程（1节），2-查找正在或即将进行的课程（2节），3-查找已经上过的课程（*节））
    def GetDynamicCourseInfo(self, dyn_course_id=None, stu_id=None, staff_id=None, time=None, cnt=1):
        mycol = self.db['DynamicCourseInfo']
        query = {}
        mydoc = None
        if dyn_course_id is not None:
            query['_id'] = dyn_course_id
            mydoc = mycol.find_one(query)
        else:
            if stu_id is not None:
                query['_stu_set._id'] = stu_id
            if staff_id is not None:
                query['$or'] = [{'_lecturer_id': staff_id}, {'_counselor_id': staff_id}]
            if time is not None:
                if cnt == 1:
                    query['_class_time'] = time
                    mydoc = mycol.find_one(query)
                elif cnt == 2:
                    query['_class_time'] = {'$gte': time}
                    mydoc = list(mycol.find(query).sort([("_class_time", 1)]).limit(cnt))
                elif cnt == 3:
                    mydoc = list(mycol.find({'$and': [{'_class_time': {'$lt': time}}, query]}).sort([("_class_time", 1)]))
            else:
                mydoc = list(mycol.find(query))
        if mydoc is None:
            return None
        else:
            return mydoc

    # 获取基础课程信息
    def GetBaseCourseInfo(self, base_course_id=None, course_name=None, main_class=None):
        mycol = self.db['BaseCourseInfo']
        query = {}
        mydoc = None
        if base_course_id is not None:
            query = {'_id': base_course_id}
        else:
            query = {'_course_name': course_name, '_main_class': main_class}
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return None
        else:
            return mydoc

    # 获取签到表信息
    def GetSignInInfo(self, stu_id=None, dyn_course_id=None):
        mycol = self.db['SignInInfo']
        query = {}
        mydoc = None
        if None not in (stu_id, dyn_course_id):
            query['_stu_id'] = stu_id
            query['_dyn_course_id'] = dyn_course_id
            mydoc = mycol.find_one(query)
        else:
            if stu_id is not None:
                query['_stu_id'] = stu_id
            if dyn_course_id is not None:
                query['_dyn_course_id'] = dyn_course_id
            mydoc = list(mycol.find(query))
        if mydoc is None:
            return None
        else:
            return mydoc

    # 获取某节课的学生状态
    def GetStuStatus(self, stu_id, dyn_course_id):
        mycol = self.db['DynamicCourseInfo']
        mydoc = mycol.find_one({"_id": dyn_course_id}, {'_stu_set': {'$elemMatch': {'_id': stu_id}}, '_id': 0})
        if mydoc == {}:
            return None
        else:
            status = mydoc['_stu_set'][0]['_status']
            return status

    # 获取学生上课状况统计次数
    def GetStuSigninNum(self, stu_id, base_course_id, choice):
        # 1:_total_num 2:_ontime_num 3:_late_num 4:_absent_num 5:_cheat_num
        num_type = {1: "_total_num", 2: "_ontime_num", 3: "_late_num", 4: "_absent_num", 5: "_cheat_num"}
        mycol = self.db['BaseCourseInfo']
        mydoc = mycol.find_one({"_id": base_course_id}, {'_stu_set': {'$elemMatch': {'_id': stu_id}}, '_id': 0})
        if mydoc == {}:
            return None
        else:
            status = mydoc['_stu_set'][0][num_type[choice]]
            return status

    # 设置学生信息
    def SetUser(self, id, name, cls, identify):
        mycol = self.db['User']
        query = {'_id': id}
        mydoc = mycol.find_one((query))
        if mydoc is not None:
            return False
        else:
            newdoc = {'_id': id, '_name': name, '_class': cls, '_bind_status': False, '_openid': '', '_identify': identify}
            mycol.insert_one(newdoc)
            return True

    # 设置基础课程信息
    def SetBaseCourseInfo(self, course_name, lecturer_id, counselor_id, campus, classroom, main_class, stu_set):
        mycol = self.db['BaseCourseInfo']
        query = {'_course_name': course_name, '_main_class': main_class}
        mydoc = mycol.find_one(query)
        if mydoc is not None:
            return False
        else:
            newdoc = {'_course_name': course_name, '_lecturer_id': lecturer_id, '_counselor_id': counselor_id,
                      '_campus': campus, '_classroom': classroom, '_main_class': main_class, '_stu_set': stu_set}
            mycol.insert_one(newdoc)
            return True

    # 设置动态课程信息
    def SetDynamicCourseInfo(self, base_course_id, week, classroom, class_time, lecturer_id, counselor_id, stu_set):
        mycol = self.db['DynamicCourseInfo']
        query = {'_base_course_id': base_course_id, '_class_time': class_time}
        mydoc = mycol.find_one(query)
        if mydoc is not None:
            return False
        else:
            newdoc = {'_base_course_id': base_course_id, '_week': week,'_classroom': classroom, '_class_time': class_time,
                      '_lecturer_id': lecturer_id, '_counselor_id': counselor_id, '_stu_set': stu_set}
            mycol.insert_one(newdoc)
            return True

    # 设置报修信息
    def SetDamageReportInfo(self, row, col, classroom, campus, photo):
        mycol = self.db['DamageReportInfo']
        query = {'_row': row, '_col': col, '_classroom': classroom, '_campus': campus}
        mydoc = mycol.find_one(query)
        if mydoc is not None:
            return False
        else:
            newdoc = {'_row': row, '_col': col, '_classroom': classroom, '_campus': campus, '_photo_url': photo}
            mycol.insert_one(newdoc)
            return True
    # 设置签到表信息
    def SetSignInInfo(self, stu_id, dyn_course_id, row, col, sign_in_time, tags):
        mycol = self.db['SignInInfo']
        query = {'_stu_id': stu_id, '_dyn_course_id': dyn_course_id}
        mydoc = mycol.find_one(query)
        if mydoc is not None:
            return False
        else:
            newdoc = {'_stu_id': stu_id, '_dyn_course_id': dyn_course_id, '_row': row, '_col': col,
                      '_sign_in_time': sign_in_time, '_tags': tags}
            mycol.insert_one(newdoc)
            return True

    # 设置某节课学生的状态
    def SetStuStatus(self, stu_id, dyn_course_id, status):
        mycol = self.db['DynamicCourseInfo']
        query = {'_id': dyn_course_id}
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return None
        else:
            query['_stu_set._id'] = stu_id
            update = {'$set': {'_stu_set.$._status': status}}
            mycol.update_one(query, update)
            return True

    # 设置学生上课情况统计次数
    def SetStuSigninNum(self, stu_id, base_course_id, num, choice):
        num_type = {1: "_total_num", 2: "_ontime_num", 3: "_late_num", 4: "_absent_num", 5: "_cheat_num"}
        mycol = self.db['BaseCourseInfo']
        query = {'_id': base_course_id}
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return None
        else:
            query['_stu_set._id'] = stu_id
            num_filed = '_stu_set.$.' + num_type[choice]
            update = {'$set': {num_filed: num}}
            mycol.update_one(query, update)
            return True

    # 设置某节课学生的备注
    def SetStuRemarks(self, stu_id, dyn_course_id, remark):
        mycol = self.db['DynamicCourseInfo']
        query = {'_id': dyn_course_id}
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return None
        else:
            query['_stu_set._id'] = stu_id
            update = {'$set': {'_stu_set.$._remarks': remark}}
            mycol.update_one(query, update)
            return True

    # 设置某节课学生的状态标签
    def SetStuTags(self, stu_id, dyn_course_id, tags):
        mycol = self.db['SignInInfo']
        query = {'_stu_id': stu_id, '_dyn_course_id': dyn_course_id}
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return None
        else:
            update = {'$set': {'_tags': tags}}
            mycol.update_one(query, update)
            return True

    # 判断座位是否为空
    def IsSeatEmpty(self, dyn_course_id, row, col):
        mycol = self.db['SignInInfo']
        query = {'_dyn_course_id': dyn_course_id, '_row': row, '_col': col}
        mydoc = list(mycol.find(query))
        if len(mydoc) == 0:
            return True
        else:
            return mydoc

    # 换座
    def SwitchSeat(self, stu_id, dyn_course_id, row, col):
        mycol = self.db['SignInInfo']
        query = {'_stu_id': stu_id, '_dyn_course_id': dyn_course_id}
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return None
        else:
            update = {'$set': {'_row': row, '_col': col}}
            mycol.update_one(query, update)
            return mydoc

    # 绑定openid
    def BindOpenid(self, openid, user_id, name):
        mycol = self.db['User']
        query = {'_id': user_id, '_name': name}
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return None
        else:
            if mydoc['_bind_status'] is True:
                if mydoc['_openid'] == openid:
                    return mydoc
                else:
                    return False
            else:
                query1 = {'_openid': openid}
                mydoc1 = mycol.find_one(query1)
                if mydoc1 is None:
                    update = {'$set': {'_bind_status': True, '_openid': openid}}
                    mycol.update_one(query, update)
                    return mydoc
                else:
                    return 4

    # 取消绑定
    def CancelBinding(self, user_id):
        mycol = self.db['User']
        query = {'_id': user_id}
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return None
        else:
            if mydoc['_bind_status'] is False:
                return False
            else:
                update = {'$set': {'_bind_status': False, '_openid': ""}}
                mycol.update_one(query, update)
                return True