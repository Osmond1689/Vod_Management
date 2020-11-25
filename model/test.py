import json,os

def test():
    with open('ftp-manage/model/profiles.json') as f:
        user_profiles = json.load(f)
        #logging.info(user_profiles)
        user_info = user_profiles.get('admin', None)
        if user_info is not None:
            return user_info[0]
if __name__=="__main__":
    a=test()
    print(a)
    #os.system('pwd')