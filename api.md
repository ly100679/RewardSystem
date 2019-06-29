# 登录验证:

  method: POST

  上传:
  
    {
      account:账号,
      password:密码
    }
  
  接收:
  
    {
      status:表示验证是否成功的布尔值
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


