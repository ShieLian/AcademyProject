# AcademyProject
##TodoList:

##底层：
- [ ] 完成资源下载逻辑的重构：
  - [x] 使用EventBus，将新获取的url用并入url池计算总量，上锁，更新进度
  - [ ] 完成中断逻辑：
	 <br>下载并写完当前资源(超时等待后强制结束) 
	 <br>**需要构建线程池,在保存资源后退出/等待200ms后强行杀线程
- [ ] 完成进度更新：
	- [x] frame为EventBus注册Listener：
- [ ] 包装接口：startFetch将被Launcher用于启动爬虫，Launcher将对AdvancedOption做出处理生成url列表

##GUI：
- [ ] 部分业务逻辑：
	- [ ] 设置了url列表文件则应使url参数、目标网页url失效
	- [ ] 设置了url参数则目标网页url的参数不应与其重复(或作为初始页面？)
	- [x] 所有文件路径在启动/退出设置页面前应检查，不存在的弹出警告。对于路径，额外提供是否新建路径的选项(二选一窗口)
	- [ ] 处理线程数，上限为url数
- [ ] AdvancedOption的界面：url参数列表

								添加
			paramName | values |删除
			paramName | values |删除
				确定		 取消　　
	<br>——确定：判断所有的paramName是否合法(冲突)，values是否符合eval的规范。　　
	<br>	是：保存　　
	<br>	否：弹出警告窗口，提示错误　　
- [ ] 接口对接:
	- [ ] 每个爬虫使用一个新线程，爬取一个url
	- [ ] 构建线程池
