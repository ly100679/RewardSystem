# 登录验证:

  method: POST

  上传:
  
    {
      account:账号,
      password:密码
    }
  
  接收:
  
    {
      status:表示验证是否成功的布尔值,
      errorCode:错误原因，1表示账号不存在，2表示密码错误
    }	
  
  url: "/login/student", "/login/expert", "/login/school"
  
# 注册验证：

  method: POST

  上传:
  
    {
      account:账号,
      password:密码,
      name:姓名,
      department:学院,
      major:专业,
      inYear:入学年份,
      phoneNumber:电话号码,
      email:邮箱
    }	
  
  接收:
  
    {
      status:表示注册是否成功的布尔值,
      errorCode:错误原因，1表示账号已存在，2表示其他错误
    }	
  
  url: "/register"

# 参赛者个人作品列表获取：

  method: GET

  上传:无
  
  接收:
  
    [{
      id:作品id(int),
      projectName:作品名(string),
      projectID:作品代码(string)，
      projectPeriod:作品所处阶段(string)
    },...]	
  
  url: "/studentProject?studentID=学号(int)"
  
  # 在作品列表中删除作品：

  method: DELETE

  上传:无
  
  接收:
  
    {
      status:删除是否成功(bool)
    }	
  
  url: "/studentProject?id=作品id(int)"
  
  # 获取参赛者个人信息：

  method: GET

  上传:无
  
  接收:
  
    {
      account:账号,
      name:姓名,
      department:学院,
      major:专业,
      inYear:入学年份,
      phoneNumber:电话号码,
      email:邮箱
    }	
  
  url: "/studentInfo?studentID=学号(int)"
