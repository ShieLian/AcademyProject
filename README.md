# AcademyProject
##TodoList:

##底层：
- [x] 完成资源下载逻辑的重构：
  - [x] 使用EventBus，将新获取的url用并入url池计算总量，上锁，更新进度
  - [x] 完成中断逻辑：
	 <br>下载并写完当前资源(超时等待后强制结束) 
	 <br>在保存资源后退出/等待200ms后强行杀线程
- [ ] 完成进度更新：
	- [x] frame为EventBus注册Listener
	- [ ] 测试

##GUI：
- [x] 部分业务逻辑：
	- [x] 设置了url列表文件则应使url参数、目标网页url失效
	- [x] 所有文件路径在启动/退出设置页面前应检查，不存在的弹出警告。对于路径，额外提供是否新建路径的选项(二选一窗口)
	- [x] 为下载完成前锁死界面
- [*] AdvancedOption的界面：url参数列表

								添加
			paramName | values |删除
			paramName | values |删除
				确定		 取消　　
	<br>——确定：判断所有的paramName是否合法(冲突)，values是否符合eval的规范。　　
	<br>	是：保存　　
	<br>	否：弹出警告窗口，提示错误　　
- [ ] 接口对接:
	- [x] 使用一个新线程启动爬虫，爬取一个url
	- [ ] Launcher对参数的预处理:
		- [x] 处理线程数，上限为url数
		- [x] 生成url列表优先级： url列表文件>url参数>目标地址
		- [x] 生成资源保存路径
		- [ ] 解决网页重名
		- [x] 设置了url参数则目标网页url参数覆盖