## 模拟器抓包获取数据

## （如果你的手机已ROOT可以直接用手机哦）

### 1、模拟器配置及使用

- 天翼网盘（含雷神模拟器、完美校园、httpcanary安装包）
- 点链接进去全部下下来：https://cloud.189.cn/t/VRZryeb2aIBr
- 解压雷神模拟器压缩包并点击绿化（出现什么异常的话把杀毒软件关闭）
- 绿化完成点击桌面图标启动
- 拖动apk文件到模拟器窗口完成app的安装
- **（如出现模拟器抓包定位问题百度自行解决）**

![https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/安装雷神模拟器.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/安装雷神模拟器.png)

![https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/雷神模拟器设置.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/雷神模拟器设置.png)

![https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/安装apk文件.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/安装apk文件.png)

### 2、httpcanary的配置及使用

- 打开刚刚安装在桌面的Httpcanary
- 安装证书并移动到根目录
- 设置目标应用为完美校园APP（就不需要其余操作了，不要点右下角的小飞机）

![https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/合成1.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/合成1.png)

![https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/合成2.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/合成2.png)

![https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/合成3.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/合成3.png)

### 3、开始抓包

- 打开完美校园app（显示root忽略即可），进入健康打卡并设置相关信息（不提交）
- 切换到httpcanary，开启抓包（点右下角的小飞机）
- 切换完美校园提交信息，打卡成功
- 切换httpcanary，停止抓包

![https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/合成4.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/合成4.png)

### 4、抓包分析

- 翻阅找到sass字样的链接，点击进去（如果有多个, 请点靠上面的）
- 第一个框为请求连接，第二个框为此网络请求为post请求
- 点击请求一栏，并在底部选择text，即可查看自己所填写的数据（记下来，或者复制出去）
- 点击响应一栏，并在底部选择text，即可查看响应结果（成功则为打卡成功，打卡频繁则失败）
- 至此我们就获得了我们绝大多数的数据了（下面项目使用的数据填写需要）

![https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/合成5.png](https://cdn.jsdelivr.net/gh/ReaJason/17wanxiaoCheckin-Actions/Pictures/合成5.png)



## 清空Commit记录

> 可能由于大家测试填写自己的数据进入py文件中，会在commit记录中出现
>
> 为了保护自己的信息，应该清除commit记录

1、在自己电脑桌面新建一个文件夹(默认你已安装git)

2、进入文件夹，右键点击 Git Bash Here，依次运行如下命令

```
git init
git clone git@github.com:.../17wanxiaoCheckin-Actions.git(你项目的ssh地址)
```

3、进入克隆之后的文件夹，右键点击 Git Bash Here，依次运行如下命令即可

```
git checkout --orphan newBranch
git add -A  # Add all files and commit them
git commit -am "change"
git branch -D master  # Deletes the master branch
git branch -m master  # Rename the current branch to master
git push -f origin master  # Force push master branch to github
git gc --aggressive --prune=all     # remove the old files
```



