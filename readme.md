## OnlineMall后端运行指南

**运行环境:**

- python 3.6.2或更高版本
- django 2.1.7或更高版本
- requests 2.19.1或更高版本
- pip包依赖工具

**运行步骤：**

1. 修改根目录下的config.py，将设置改为自己的appId和secret代码，以及图片服务器的域名

2. 运行start.sh脚本，将会自动安装所需依赖环境，或在backend/OnlineMall目录下运行以下命令：

   ```powershell
   pip3 install requests
   pip3 install django
   python manage.py runserver 0.0.0.0:[port]
   ```

   port指服务端口号，默认是80，如果使用其他的需要一并修改frontend中restURL的地址。

   