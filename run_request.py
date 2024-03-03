import random
import urllib.parse
import requests
import hashlib
import json
from datetime import datetime
import gui_ji
class SchoolActivityClient:
    def __init__(self, phone, password):
        self.app_key = "389885588s0648fa"
        self.phone = phone
        self.password = self.string_to_md5(password)
        self.host = "https://run-lb.tanmasports.com/"
        self.token = None
        self.user_Id=None
        self.school_Id=None
        self.student_Id=None
        self.app_secret="56E39A1658455588885690425C0FD16055A21676"

    """加密传参函数"""
    def string_to_md5(self,plain_text):
        md5 = hashlib.md5()
        md5.update(plain_text.encode('utf-8'))
        return md5.hexdigest()

    """传参中的签证"""
    def get_sign(self, query=None, body=None):
        if query is None:
            query = {}

        sign_str = ''.join(key + query.get(key, '') for key in sorted(query.keys()))
        sign_str += self.app_key + self.app_secret
        if body:
            sign_str += body

        for char in [' ', '~', '!', '(', ')', "'"]:
            sign_str = sign_str.replace(char, '')

        encoded_str = urllib.parse.quote(sign_str, safe='')
        final_str = self.string_to_md5(encoded_str).upper()

        if sign_str != encoded_str:
            final_str += "encodeutf8"

        return final_str

    """登录获取信息的函数"""
    def login(self):
        API_URL = "https://run-lb.tanmasports.com/v1/auth/login/password"
        body = {
            "password": self.password,
            "userPhone": self.phone
        }
        body_str = json.dumps(body)
        headers = {
            "sign": self.get_sign(None, body_str),
            "appkey": self.app_key,
            "Content-Type": "application/json; charset=UTF-8"
        }

        response = requests.post(API_URL, headers=headers, data=body_str)

        if response.status_code == 200:
            user_info_response = response.json()
            if user_info_response["code"] == 10000:
                user_info = user_info_response["response"]
                self.token=user_info['oauthToken']['token']
                self.user_Id=json.dumps(user_info['userId'])
                self.school_Id = json.dumps(user_info['schoolId'])
                # self.school_Id = user_info['schoolId']
                self.student_Id = json.dumps(user_info['studentId'])
                return user_info
            else:
                raise Exception(user_info_response["msg"])
        else:
            response.raise_for_status()

    """获取第几周的活动课程"""
    def get_activity_list(self,week):
        api_endpoint = f"{self.host}clubactivity/querySemesterClubActivity"
        params = {
            "weekDay": week,
            "pageNo": "1",
            "pageSize": "100"
        }

        headers = {
            "sign": self.get_sign(params,None),
            "token": self.token,
            "appkey": self.app_key,
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/3.12.0"
        }

        response = requests.get(api_endpoint, headers=headers, params=params)
        if response.status_code == 200:
            standard_response = response.json()
            return standard_response
        else:
            print(f"Error fetching activities: {response.status_code}")
            return []

    """主要用于请求获取学期"""
    def get_run_standard(self):
        API_ENDPOINT = "v1/unirun/query/runStandard"
        params = {"schoolId": self.school_Id}
        sign = self.get_sign(params, None)
        headers = {
            "sign": sign,
            "token": self.token,
            "appkey": self.app_key,
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/3.12.0"
        }
        API_URL = f"{self.host}{API_ENDPOINT}"
        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code == 200:
            sign_in_tf_info = response.json()
            return sign_in_tf_info
        else:
            print(f"Failed to fetch sign-in information: {response.status_code}, {response.text}")
            return None


    """主要用于请求获取学校标准"""

    def get_SchoolBound(self):
        API_ENDPOINT = "v1/unirun/querySchoolBound"
        params = {"schoolId": self.school_Id}
        sign = self.get_sign(params, None)
        headers = {
            "sign": sign,
            "token": self.token,
            "appkey": self.app_key,
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/3.12.0"
        }
        API_URL = f"{self.host}{API_ENDPOINT}"
        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code == 200:
            sign_in_tf_info = response.json()
            return sign_in_tf_info
        else:
            print(f"Failed to fetch sign-in information: {response.status_code}, {response.text}")
            return None

    def record_new(self, record_body):
        API_URL = "https://run-lb.tanmasports.com/v1/unirun/save/run/record/new"
        str_body=json.dumps(record_body)
        headers = {
            "sign": self.get_sign(None,str_body),
            "token": self.token,
            "appkey": self.app_key,
            "Content-Type": "application/json; charset=UTF-8",
        }
        response = requests.post(API_URL, headers=headers, data=str_body)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()



    def create_and_send_record(self,run_distance=random.randint(4500, 5000), run_time= random.randint(35, 50), school_site=0,file_path='map_cuit_hkg.json'):

        record_body = {
            "againRunStatus": "0",
            'appVersions' :"1.8.0",
            "againRunTime": '0',
            "trackPoints": json.dumps(gui_ji.run(file_path=file_path)),  # 跑步路线，假设已有变量或者直接赋值
            "distanceTimeStatus": "1",
            "innerSchool": "1",
            "runDistance": run_distance,  # 跑步距离，单位为米
            "runTime": run_time,  # 跑步时间，单位为分钟
            "userId": self.user_Id,  # 用户ID
            "vocalStatus": "1",
            "runValidDistance":run_distance,
            "runValidTime":run_time,
            "yearSemester":self.get_run_standard()['response']['semesterYear'],  # 学期
            "recordDate":  datetime.now().strftime("%Y-%m-%d"),  # 记录日期，格式为年-月-日
            "realityTrackPoints": self.get_SchoolBound()['response'][school_site]['siteBound'] + "--"  # 学校经纬度区间
        }

        return self.record_new(record_body)


    """加入俱乐部"""
    def joinClub (self, activityId):
        api_endpoint = f"{self.host}/clubactivity/joinClubActivity"
        params = {
            "studentId": self.student_Id,
            "activityId": activityId,
        }
        headers = {
            "sign": self.get_sign(params, None),
            "token": self.token,
            "appkey": self.app_key,
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/3.12.0"
        }
        response = requests.get(api_endpoint, headers=headers, params=params)
        if response.status_code == 200:
            standard_response = response.json()
            return standard_response
        else:
            print(f"Error fetching activities: {response.status_code}")
            return []


    def get_sign_in_tf(self):
        API_ENDPOINT = "v1/clubactivity/getSignInTf"
        params = {"studentId": self.student_Id}
        sign = self.get_sign(params,None)
        headers = {
            "sign": sign,
            "token": self.token,
            "appkey": self.app_key,
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/3.12.0"
        }
        API_URL = f"{self.host}{API_ENDPOINT}?studentId={self.student_Id}"
        response = requests.get(API_URL, headers=headers,params=params)

        if response.status_code == 200:
            sign_in_tf_info = response.json()
            return sign_in_tf_info
        else:
            print(f"Failed to fetch sign-in information: {response.status_code}, {response.text}")
            return None

    def get_MySportsClass_Clocking(self):
        API_ENDPOINT = "v1/sports/class/getMySportsClassClocking"

        sign = self.get_sign(None,None)
        headers = {
            "sign": sign,
            "token": self.token,
            "appkey": self.app_key,
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/3.12.0"
        }
        API_URL = f"{self.host}{API_ENDPOINT}"
        response = requests.get(API_URL, headers=headers)

        if response.status_code == 200:
            sign_in_tf_info = response.json()
            return sign_in_tf_info
        else:
            print(f"Failed to fetch sign-in information: {response.status_code}, {response.text}")
            return None


