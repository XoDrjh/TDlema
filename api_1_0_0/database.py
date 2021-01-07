import pymongo

class DataBase:
    def __init__(self, db_name):
        self.db = pymongo.MongoClient(host='xxx.xx.xxx.xxx', port=27017)[db_name]

    def GetUser(self, openid, id):
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

    def GetDynamicCourseInfo(self, dyn_course_id, stu_id, stuff_id, time, cnt):
        mycol = self.db['DynamicCourseInfo']
        query = {}
        mydoc = None
        if dyn_course_id is not None:
            query['_id'] = dyn_course_id
            mydoc = mycol.find_one(query)
        else:
            if stu_id is not None:
                query['_stu_set._id'] = stu_id
            if stuff_id is not None:
                query['$or'] = [{'_lecturer_id': stuff_id}, {'_counselor_id': stuff_id}]
            if time is not None:
                if cnt > 1:
                    query['_class_time'] = {'$gte': time}
                    mydoc = list(mycol.find(query).limit(cnt))
                else:
                    query['_class_time'] = time
                    mydoc = mycol.find_one(query)
            else:
                mydoc = list(mycol.find(query))
        if mydoc is None:
            return None
        else:
            return mydoc

    def GetBaseCourseInfo(self, base_course_id):
        mycol = self.db['BaseCourseInfo']
        query = {'_id': base_course_id}
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return None
        else:
            return mydoc

    def GetSignInInfo(self, stu_id, dyn_course_id):
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

    def GetStuStatus(self, stu_id, dyn_course_id):
        mycol = self.db['DynamicCourseInfo']
        query = {'_id': dyn_course_id}
        args = {'_id': 0, '_stu_set': {'$elemMatch': {'_id': stu_id}}}
        mydoc = mycol.find_one(query, args)
        if mydoc is None:
            return None
        else:
            status = mydoc['_stu_set'][0]['_status']
            return status

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

    def SetDynamicCourseInfo(self, base_course_id, week, class_time, lecturer_id, counselor_id, stu_set):
        mycol = self.db['DynamicCourseInfo']
        query = {'_base_course_id': base_course_id, '_class_time': class_time}
        mydoc = mycol.find_one(query)
        if mydoc is not None:
            return False
        else:
            newdoc = {'_base_course_id': base_course_id, '_week': week, '_class_time': class_time,
                      '_lecturer_id': lecturer_id, '_counselor_id': counselor_id, '_stu_set': stu_set}
            mycol.insert_one(newdoc)
            return True

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

    def IsSeatEmpty(self, dyn_course_id, row, col):
        mycol = self.db['SignInInfo']
        query = {'_dyn_course_id': dyn_course_id, '_row': row, '_col': col}
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return True
        else:
            return False

    def SwitchSeat(self, stu_id, dyn_course_id, row, col):
        mycol = self.db['SignInInfo']
        query = {'_stu_id': stu_id, '_dyn_course_id': dyn_course_id}
        mydoc = mycol.find_one(query)
        if mydoc is None:
            return None
        else:
            update = {'$set': {'_row': row, '_col': col}}
            mycol.update_one(query, update)
            return mydoc['_sign_in_time']

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
                update = {'$set': {'_bind_status': True, '_openid': openid}}
                mycol.update_one(query, update)
                return mydoc

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
                update = {'$set': {'_bind_status': False}}
                mycol.update_one(query, update)
                return True
