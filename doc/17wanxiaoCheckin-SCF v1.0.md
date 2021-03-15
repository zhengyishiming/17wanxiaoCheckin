# 🌈17wanxiaoCheckin-SCF v1.0

## 前提

1. 已有腾讯云账号（没有，可以注册）
2. 腾讯云已实名（觉得实名有困难，不建议用）

## 使用方法

### 1、进入控制台

![进入控制台.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/进入控制台.png)

### 2、进入云函数

![进入云函数.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/搜索云函数.png)

### 3、新建云函数

![新建云函数.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/选择地区.png)

### 4、上传代码

在此下载 ，https://lingsiki.lanzous.com/b0ekc7p9i 密码：7dwe

同时请下载，RegisterDeviceID.zip 下来，后续获取 ID 需要。如若软件打不开，可自行下载模拟器，短信登陆完美校园之后，在模拟器设置中复制 IMEI（即为 DEVICEID 字段）

![上传代码.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/新建函数.png)

### 5、触发器配置

配置时间可具体参考，它下面的 [链接](https://cloud.tencent.com/document/product/583/9708)

每日 6 点打卡：`0 0 6 * * * *`

每日 6、12、17点打卡：`0 0 6,12,17 * * * *`

![设置触发器.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/设置触发器.png)

### 6、添加环境变量

- 设置 900 秒（**重点**），因为 3 秒太短啦！
- 可选参数，刚接触的朋友我强烈建议使用 QQ 邮箱的推送方式，因为推送消息最全面！
- 如果无误再转 Qmsg 酱（可选），Server酱云函数好像被 ban 了
- USERNAME 字段（必填）：手机号1,手机号2,......（与下面密码对应），例如：`1737782***,13602***`
- PASSWORD 字段（必填）：密码1,密码2,......  （与上面账号对应），例如：`123456,456789`
- DEVICEID 字段（必填）：设备id1,设备id2....（与上面账号对应），例如：`1232,12312`，没有请下载 RegisterDeviceID 获取
- SCKEY 字段（可选）：用来开启 Server 酱推送服务，填写一个即可，没有请前往 [Server酱](https://sc.ftqq.com/3.version) 注册获取
- KEY 字段（可选）：用来开启 Qmsg 酱推送服务，填写一个即可，没有请前往 [Qmsg酱](https://qmsg.zendee.cn/index.html) 注册获取
- SEND_EMAIL 字段（可选）：用来开启 QQ邮箱推送服务，QQ邮箱地址
- SEND_PWD 字段（可选）：用来开启 QQ邮箱推送服务，QQ邮箱授权码，**不是 QQ 密码**
- RECEIVE_EMAIL 字段（可选）：用来开启 QQ邮箱推送服务，接收邮箱地址，理论上什么邮箱都可

![编辑环境变量.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/编辑环境变量.png)

![设置环境变量.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/设置环境变量.png)

### 7、部署测试

每一次修改代码之后，一定要点一下测试（自动部署），或者部署代码才能生效
**查看推送情况，确认是否成功**，（检查打卡 json 字段中的 areaStr 是否为自己所在地址，如果不在，请一定要修改代码，因为打卡的地址不对可不行；如果 json 字段中还有其他字段，如 deptid，stuNo 等等为 null 或者不对，请务必修改代码，如果 Message 有值为 None（QQ 邮箱推送打卡表格数据），请一定要修改代码，因为该值无法自动填写）如果你显示打卡成功或打卡频繁，且推送的 Message 中没有 None 值，即为成功，**至此每日六点多将会自行打卡**

![测试.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/测试.png)



## FQA

### ❄一、健康打卡

健康打卡目前我发现的一共分为两种界面的样式：

1. <a href='https://cdn.jsdelivr.net/gh/LingSiKi/images/img/第一类健康打卡.png' target='_blank'>第一类健康打卡</a>
2. <a href='https://cdn.jsdelivr.net/gh/LingSiKi/images/img/第二类健康打卡.png' target='_blank'>第二类健康打卡</a>

由于两种打卡的获取数据及打卡方式差距大，且未找到获取当前用户健康打卡模板的方法，因此有时需要修改代码

#### 🤺健康打卡常见问题汇总

**1、提交的部分数据未填写，或报错 {'msg': '参数不合法', 'code': '10002', 'data': 'areaStr can not be null'}，如何填写对应的数据？**

打开 17wanxiao.py 修改部分代码，去掉对应注释（选中代码，使用 ctrl + / 去掉注释）（敲重点，不然就语法错误，实在还是错误，复制下面代码粘贴覆盖对应位置再修改即可）。
此方法修改的只有 json 字段，因此下面的 message 仍为会为 None，并没关系 [#27](https://github.com/ReaJason/17wanxiaoCheckin-Actions/issues/27)。

```python
# 获取第一类健康打卡的参数
json1 = {"businessType": "epmpics",
         "jsonData": {"templateid": "pneumonia", "token": token},
         "method": "userComeApp"}
post_dict = get_post_json(json1)

if post_dict:
    # 第一类健康打卡
    # print(post_dict)

    # 修改温度等参数
    for j in post_dict['updatainfo']:  # 这里获取打卡json字段的打卡信息，微信推送的json字段
        if j['propertyname'] == 'temperature':  # 找到propertyname为temperature的字段
            j['value'] = '36.2'  # 由于原先为null，这里直接设置36.2（根据自己学校打卡选项来）
        if j['propertyname'] == '举一反三即可':
            j['value'] = '举一反三即可'

    # 修改地址 areaStr can not be null ，依照自己完美校园，查一下地址即可
    post_dict['areaStr'] = '{"streetNumber":"89号","street":"建设东路","district":"","city":"新乡市","province":"河南省",' \
                           '"town":"","pois":"河南师范大学(东区)","lng":113.91572178314209,' \
                           '"lat":35.327695868943984,"address":"牧野区建设东路89号河南师范大学(东区)","text":"河南省-新乡市",' \
                           '"code":""} '
    healthy_check_dict = healthy_check_in(token, post_dict)
    check_dict_list.append(healthy_check_dict)
else:
    # 获取第二类健康打卡参数
    post_dict = get_recall_data(token)
    # 第二类健康打卡
    healthy_check_dict = receive_check_in(token, custom_id_dict['customerId'], post_dict)
    check_dict_list.append(healthy_check_dict)
```

**2、健康打卡数据很奇怪，我们是第二类健康打卡，但是还是打的第一类健康打卡？**

由于没有获取哪一类的方法，所以第二类健康打卡的兄弟出现这个情况需要自己修改一下代码，将第一类健康打卡的代码全部注释，把第二类健康打卡缩进取消。

```python
# # 获取第一类健康打卡的参数
# json1 = {"businessType": "epmpics",
#          "jsonData": {"templateid": "pneumonia", "token": token},
#          "method": "userComeApp"}
# post_dict = get_post_json(json1)
# 
# if post_dict:
#     # 第一类健康打卡
#     # print(post_dict)
# 
#     # 修改温度等参数
#     for j in post_dict['updatainfo']:  # 这里获取打卡json字段的打卡信息，微信推送的json字段
#         if j['propertyname'] == 'temperature':  # 找到propertyname为temperature的字段
#             j['value'] = '36.2'  # 由于原先为null，这里直接设置36.2（根据自己学校打卡选项来）
#         if j['propertyname'] == '举一反三即可':
#             j['value'] = '举一反三即可'
# 
#     # 修改地址，依照自己完美校园，查一下地址即可
#     post_dict['areaStr'] = '{"streetNumber":"89号","street":"建设东路","district":"","city":"新乡市","province":"河南省",' \
#                            '"town":"","pois":"河南师范大学(东区)","lng":113.91572178314209,' \
#                            '"lat":35.327695868943984,"address":"牧野区建设东路89号河南师范大学(东区)","text":"河南省-新乡市",' \
#                            '"code":""} '
#     healthy_check_dict = healthy_check_in(token, post_dict)
#     check_dict_list.append(healthy_check_dict)
# else:
# 获取第二类健康打卡参数
post_dict = get_recall_data(token)
# 第二类健康打卡
healthy_check_dict = receive_check_in(token, custom_id_dict['customerId'], post_dict)
check_dict_list.append(healthy_check_dict)
```

**3、第二类健康打卡，显示成功打卡了，但是手机仍然显示今日无变化一键打卡？**

请加入自己打卡位置的经纬度，不然那边服务器不知道位置，无法获取你的打卡信息 [#24](https://github.com/ReaJason/17wanxiaoCheckin-Actions/issues/24)。

```python
"longitude": "",  # 请在此处填写需要打卡位置的longitude
"latitude": "",  # 请在此处填写需要打卡位置的latitude
```

**4、deptid获取不到，TypeError：'NoneType' object is not subscriptable，报错裂开？（已修复，Bug 转移）**

**5、我们学校数据很多都获取不了，数据也不对，怎么办？**

可以自己抓包，根据上面的问题 1 的提示，修改代码

也可以加群寻求帮助（在 issue 里面，点进去，暗号也在里边！）

**6、我们放假了，可是脚本打卡的地址仍然在学校，有些选项也没有更新，怎么办？**

首先可以尝试打开手机完美校园app，进行一次手动打卡，信息全部正确选填好，再使用脚本打一次卡，如果位置没改过来即修改代码，修改代码有一个问题，多人打卡的代码如何修改（每个人的家都不一样）？

请先尝试本校的打卡数据能否获取脚本上次打卡的地址，先使用一个账号信息，修改地址，进行一次打卡，然后把修改地址的代码注释，再进行一次打卡查看地址是否为上次修改的地址（此时代码已没指定地址，完全是获取上次打卡信息），如果行，那每个账号都如此操作一顿，再进行多人打卡，如果不行，那取消多人打卡，每个账号用一套代码（或每个账号用一个云函数），通过代码修改地址达到效果（看不懂，是我的问题，我表述不清了，泪目）

```python
# 获取第一类健康打卡的参数
json1 = {"businessType": "epmpics",
         "jsonData": {"templateid": "pneumonia", "token": token},
         "method": "userComeApp"}
post_dict = get_post_json(json1)

if post_dict:
    # 第一类健康打卡
    # print(post_dict)

    # 修改温度等参数
    for j in post_dict['updatainfo']:  # 这里获取打卡json字段的打卡信息，微信推送的json字段
        if j['propertyname'] == 'temperature':  # 找到propertyname为temperature的字段
            j['value'] = '36.2'  # 由于原先为null，这里直接设置36.2（根据自己学校打卡选项来）
        if j['propertyname'] == '举一反三即可':
            j['value'] = '举一反三即可'

    # 修改地址，依照自己完美校园，查一下地址即可（坐标拾取：http://api.map.baidu.com/lbsapi/getpoint/）
    post_dict['areaStr'] = '{"streetNumber":"89号","street":"建设东路","district":"","city":"新乡市","province":"河南省",' \
                           '"town":"","pois":"河南师范大学(东区)","lng":113.91572178314209,' \
                           '"lat":35.327695868943984,"address":"牧野区建设东路89号河南师范大学(东区)","text":"河南省-新乡市",' \
                           '"code":""} '
    healthy_check_dict = healthy_check_in(token, post_dict)
    check_dict_list.append(healthy_check_dict)
else:
    # 获取第二类健康打卡参数
    post_dict = get_recall_data(token)
    # 第二类健康打卡
    healthy_check_dict = receive_check_in(token, custom_id_dict['customerId'], post_dict)
    check_dict_list.append(healthy_check_dict)
```

**7、信息推送太过复杂，每次看得我眼花缭乱的，要晕了，要晕了，怎么办？**

可尝试将找到如下代码：

~~~python
				log_info.append(
    f"""#### {name}{check['type']}打卡信息：
```
{json.dumps(check['check_json'], sort_keys=True, indent=4, ensure_ascii=False)}
```
------
| Text                           | Message |
| :----------------------------------- | :--- |
{post_msg}
------
```
{check['res']}
```""")
~~~

改为（删掉中间那么多行）：

~~~python
                log_info.append(f"""#### {name}{check['type']}打卡信息：
```
{check['res']}
```""")
~~~

**8、如果健康打卡信息全为None，但是推送打卡成功了，到底成功了没？**

如果你是第一类健康打卡，建议使用完美校园 app 打一次卡，再看看脚本运行，因为目前只写了 app 端获取打卡信息的接口。

如果你是第二类健康打卡，你留下第二类健康打卡代码即可，方法在上面。

### ❄二、校内打卡

校内打卡部分学校有，部分学校没有，每个学校的校内打卡基本都不一样，有的只需要上午打一次，有点上午和下午两次，

而有的一天三次，不过能获取校内打卡模板id基本没什么差错。

#### 🔥打卡流程及函数

1. 获取校内打卡模板id函数为 --> [get_custom_id(token)](https://github.com/ReaJason/17wanxiaoCheckin-Actions/blob/master/17wanxiao.py#L332)
2. 根据模板id获取校内打卡具体id函数为 --> [get_id_list(token, custom_id)](https://github.com/ReaJason/17wanxiaoCheckin-Actions/blob/master/17wanxiao.py#L356)
3. 获取打卡数据函数为 --> [get_post_json(jsons)](https://github.com/ReaJason/17wanxiaoCheckin-Actions/blob/master/17wanxiao.py#L28)
4. 校内打卡函数 --> [campus_check_in(username, token, post_dict, id)](https://github.com/ReaJason/17wanxiaoCheckin-Actions/blob/master/17wanxiao.py#L194)

#### 🤺校内打卡常见问题汇总

**1、校内打卡老是不在业务时间，或者无法打卡？**

由于使用了获取了时间的函数，可能你们要求打卡时间和设置不一样，可自行修改。

```python
def get_ap():
    now_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    am = 0 <= now_time.hour < 12
    pm = 12 <= now_time.hour < 17
    ev = 17 <= now_time.hour <= 23
    return [am, pm, ev]
```

**2、放假回家了如何取消校内打卡？**

请注释掉 17wanxiao.py 如下代码（或者删掉），最后一行的 return 一定要留住，不然推送啥也没看见，可别把自己急着了。

```python
# 获取校内打卡ID
id_list = get_id_list(token, custom_id_dict['customerAppTypeId'])
# print(id_list)
if not id_list:
    return check_dict_list

# 校内打卡
# for index, i in enumerate(id_list):
#     if ape_list[index]:
#         # print(i)
#         logging.info(f"-------------------------------{i['templateid']}-------------------------------")
#         json2 = {"businessType": "epmpics",
#                  "jsonData": {"templateid": i['templateid'], "customerAppTypeRuleId": i['id'],
#                               "stuNo": post_dict['stuNo'],
#                               "token": token}, "method": "userComeAppSchool",
#                  "token": token}
#         campus_dict = get_post_json(json2)
#         campus_dict['areaStr'] = post_dict['areaStr']
#         for j in campus_dict['updatainfo']:
#             if j['propertyname'] == 'temperature':
#                 j['value'] = '36.4'
#             if j['propertyname'] == 'symptom':
#                 j['value'] = '无症状'
#         campus_check_dict = campus_check_in(username, token, campus_dict, i['id'])
#         check_dict_list.append(campus_check_dict)
#         logging.info("--------------------------------------------------------------")
return check_dict_list
```

**如果没有进行校内打卡，可尝试更换获取校内打卡模板id的接口。**  [#25](https://github.com/ReaJason/17wanxiaoCheckin-Actions/issues/25)