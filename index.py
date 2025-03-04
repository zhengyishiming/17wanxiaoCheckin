import time

from login import CampusLogin
from utils.config import load_config
from api.wanxiao_push import wanxiao_qmsg_push, wanxiao_server_push, wanxiao_email_push
from api.campus_check import get_id_list_v1, get_id_list_v2, get_customer_type_id, get_campus_check_post, campus_check_in
from api.healthy1_check import get_healthy1_check_post_json, healthy1_check_in
from api.healthy2_check import get_healthy2_check_posh_json, healthy2_check_in
from api.user_info import get_user_info
from setting import log


def get_token(username, password, device_id):
    for _ in range(3):
        try:
            campus_login = CampusLogin(phone_num=username, device_id=device_id)
        except Exception as e:
            log.warning(e)
            continue
        login_dict = campus_login.pwd_login(password)
        if login_dict["status"]:
            log.info(f"{username[:4]}，{login_dict['msg']}")
            return login_dict["token"]
        elif login_dict['errmsg'] == "该手机号未注册完美校园":
            log.warning(f"{username[:4]}，{login_dict['errmsg']}")
            return None
        elif login_dict['errmsg'].startswith("密码错误"):
            log.warning(f"{username[:4]}，{login_dict['errmsg']}")
            log.warning("代码是死的，密码错误了就是错误了，赶紧去查看一下是不是输错了!")
            return None
        else:
            log.info(f"{username[:4]}，{login_dict['errmsg']}")
            log.warning('正在尝试重新登录......')
            time.sleep(5)
    return None


def merge_post_json(dict1, dict2):
    for key, value in dict2.items():
        if value and key in dict1 and key != 'updatainfo':
            dict1[key] = value
        if key == 'updatainfo':
            dict3 = {}
            for i, j in enumerate(dict1['updatainfo']):
                dict3[j['propertyname']] = i
            for i in value:
                if i['propertyname'] in dict3:
                    dict1['updatainfo'][dict3[i['propertyname']]]['value'] = i['value']
                    dict1['checkbox'][dict3[i['propertyname']]]['value'] = i['value']
    

def info_push(push_dict, raw_info):
    flag = []
    if push_dict['wechat']['enable']:
        push = wanxiao_server_push(
            push_dict['wechat']['send_key'], raw_info
        )
        if push['status']:
            flag.append(1)
            log.info(push['msg'])
        else:
            flag.append(0)
            log.warning(push['errmsg'])
    if push_dict['email']['enable']:
        push = wanxiao_email_push(
            push_dict['email']['send_email'], push_dict['email']['send_pwd'],
            push_dict['email']['receive_email'], push_dict['email']['smtp_address'],
            push_dict['email']['smtp_port'], raw_info
        )
        if push['status']:
            flag.append(1)
            log.info(push['msg'])
        else:
            flag.append(0)
            log.warning(push['errmsg'])
    
    if push_dict['qmsg']['enable']:
        push = wanxiao_qmsg_push(
            push_dict['qmsg']['key'], push_dict['qmsg']['qq_num'],
            push_dict['qmsg']['type'], raw_info
        )
        if push['status']:
            flag.append(1)
            log.info(push['msg'])
        else:
            flag.append(0)
            log.warning(push['errmsg'])
    if 1 in flag:
        return True
    return False


def check_in(user):
    check_dict_list = []
    
    # 登录获取token用于打卡
    token = get_token(user['phone'], user['password'], user['device_id'])
    
    if not token:
        errmsg = f"{user['phone'][:4]}，获取token失败，打卡失败"
        log.warning(errmsg)
        check_dict_list.append({"status": 0, "errmsg": errmsg})
        return check_dict_list
    
    # 获取个人信息
    user_info = get_user_info(token)
    if not user_info:
        errmsg = f"{user['phone'][:4]}，获取个人信息失败，打卡失败"
        log.warning(errmsg)
        check_dict_list.append({"status": 0, "errmsg": errmsg})
        return check_dict_list
    log.info(f'{user_info["username"][0]}-{user_info["school"]}，获取个人信息成功')
    
    healthy1_check_config = user['healthy_checkin']['one_check']
    healthy2_check_config = user['healthy_checkin']['two_check']
    if healthy1_check_config['enable']:
        # 第一类健康打卡
    
        # 获取第一类健康打卡的参数
        post_dict = get_healthy1_check_post_json(token)
        
        # 合并配置文件的打卡信息
        merge_post_json(post_dict, healthy1_check_config['post_json'])
        
        healthy1_check_dict = healthy1_check_in(token, user['phone'], post_dict)
        check_dict_list.append(healthy1_check_dict)
    elif healthy2_check_config['enable']:
        # 第二类健康打卡
        
        # 获取第二类健康打卡参数
        post_dict = get_healthy2_check_posh_json(token)
        
        # 合并配置文件的打卡信息
        if not healthy2_check_config['post_json']['latitude'] and not healthy2_check_config['post_json']['longitude']:
            post_dict['latitude'] = ""
            post_dict['longitude'] = ""
            log.info('当前打卡未设置经纬度，后台会将此次打卡计为手动打卡（学校没做要求可不管）')
        for i, j in healthy2_check_config['post_json'].items():
            if j:
                post_dict[i] = j
        healthy2_check_dict = healthy2_check_in(token, user_info["customerId"], post_dict)
    
        check_dict_list.append(healthy2_check_dict)
    else:
        log.info('当前并未配置健康打卡方式，暂不进行打卡操作')
        
    # 校内打卡
    campus_check_config = user['campus_checkin']
    if not campus_check_config['enable']:
        log.info('当前并未开启校内打卡，暂不进行打卡操作')
    else:
        # 获取校内打卡ID
        custom_type_id = user_info.get('customerAppTypeId', get_customer_type_id(token))
        if custom_type_id:
            id_list = get_id_list_v2(token, custom_type_id)
        else:
            id_list = get_id_list_v1(token)
    
        if not id_list:
            log.warning('当前未获取到校内打卡ID，请尝试重新运行，如仍未获取到，请反馈')
            return check_dict_list
        for index, i in enumerate(id_list):
            start_end = f'{i["templateid"]} ({i.get("startTime", "")}-{i.get("endTime", "")})'
            log.info(f"{start_end:-^40}")
        
            # 获取校内打卡参数
            campus_dict = get_campus_check_post(
                template_id=i['templateid'],
                custom_rule_id=i['id'],
                stu_num=user_info['stuNo'],
                token=token
            )
            # 合并配置文件的打卡信息
            merge_post_json(campus_dict, campus_check_config['post_json'])
        
            # 校内打卡
            campus_check_dict = campus_check_in(user['phone'], token, campus_dict, i['id'])
            check_dict_list.append(campus_check_dict)
            log.info("-" * 40)
    return check_dict_list


def main_handler(*args, **kwargs):
    
    # 推送数据
    raw_info = []
    
    # 加载用户配置文件
    user_config_dict = load_config(kwargs['user_config_path'])
    for user_config in user_config_dict:
        if not user_config['phone']:
            continue
        log.info(user_config['welcome'])
        
        # 单人打卡
        check_dict = check_in(user_config)
        # 单人推送
        if info_push(user_config['push'], check_dict):
            pass
        else:
            log.info("当前用户并未配置 push 参数，将统一进行推送")
            raw_info.extend(check_dict)
    
    # 统一推送
    if raw_info:
        all_push_config = load_config(kwargs['push_config_path'])
        if info_push(all_push_config, raw_info):
            pass
        else:
            log.info('统一推送未开启，如要开启，请修改 conf/push.json 配置文件')
    else:
        log.info('所有打卡数据已推送完毕，无需统一推送')


if __name__ == "__main__":
    main_handler(user_config_path='./conf/user.json', push_config_path='./conf/push.json')
