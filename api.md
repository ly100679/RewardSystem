# 1 登录验证:

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
  
# 2 注册验证：

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

# 3 参赛者个人作品列表获取：

  method: GET

  上传:无
  
  接收:
  
    {
      competitionName:当前的竞赛名(string),
      data:[{
        id:作品id(int),
        projectName:作品名(string),
        projectID:作品代码(string),
        projectPeriod:作品所处阶段(string)
        nameOfWork:作品名称(string)
        classificationOfWork:作品类别(0-1)
        declarationOfWork:作品分类（A-F）
        overallDescriptionOfWork:作品总体情况说明(string)
        innovationPoint:创新点(string)
        keyWord:关键词(string)
        name:姓名(string)
        StudentID:学号(int)
        dateOfBirth:出生年月(yyyy-mm-dd)
        major:专业(string)
        inYear:入学年份(int)
        fullNameOfwork:作品全称(string)
        postalAddress:通讯地址(string)
        phoneNumber:联系电话(int)
        email:邮箱(string)
        currentEducation:现学历(0-3)
        partner:[{
          nameOfPartner:姓名(string)
          studentIDOfPartner:学号(int)
          phoneOfPartner:联系电话(int)
          emailOfPartner:邮箱(string)
          currenteducationOfPartner:现学历(0-3)
        },..]
      },...](只传当前竞赛的作品)
      
      
    }	
  
  url: "/studentProject?studentID=学号(int)&id=作品id(int)"
  
  # 4 在作品列表中删除作品：

  method: DELETE

  上传:无
  
  接收:
  
    {
      status:删除是否成功(bool)
    }	
  
  url: "/studentProject?id=作品id(int)"
  
  # 5 获取参赛者个人信息：

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
  
  # 6 新建页保存or提交作品信息：

  method: POST

  上传:
  
    {
      status:作品状态(string)
      nameOfWork:作品名称(string)
      classificationOfWork:作品类别(0-1)
      declarationOfWork:作品分类（A-F）
      overallDescriptionOfWork:作品总体情况说明(string)
      innovationPoint:创新点(string)
      keyWord:关键词(string)
      name:姓名(string)
      StudentID:学号(int)
      dateOfBirth:出生年月(yyyy-mm-dd)
      major:专业(string)
      inYear:入学年份(int)
      fullNameOfwork:作品全称(string)
      postalAddress:通讯地址(string)
      phoneNumber:联系电话(int)
      email:邮箱(string)
      currentEducation:现学历(0-3)
      partner:[{
        nameOfPartner:姓名(string)
        studentIDOfPartner:学号(int)
        phoneOfPartner:联系电话(int)
        emailOfPartner:邮箱(string)
        currenteducationOfPartner:现学历(0-3)
      },..]
    }	
  
  接收:
   
    {
      status:操作是否成功(bool)
    }	
  
  url: "/studentProject?studentID=学号(int)"
  
  # 7 修改页保存or提交作品信息：

  method: PUT

  上传:
  
    {
      status:作品状态(string)
      nameOfWork:作品名称(string)
      classificationOfWork:作品类别(0-1)
      declarationOfWork:作品分类（A-F）
      overallDescriptionOfWork:作品总体情况说明(string)
      innovationPoint:创新点(string)
      keyWord:关键词(string)
      name:姓名(string)
      StudentID:学号(int)
      dateOfBirth:出生年月(yyyy-mm-dd)
      major:专业(string)
      inYear:入学年份(int)
      fullNameOfwork:作品全称(string)
      postalAddress:通讯地址(string)
      phoneNumber:联系电话(int)
      email:邮箱(string)
      currentEducation:现学历(0-3)
      partner:[{
        nameOfPartner:姓名(string)
        studentIDOfPartner:学号(int)
        phoneOfPartner:联系电话(int)
        emailOfPartner:邮箱(string)
        currenteducationOfPartner:现学历(0-3)
      },..]
    }	
  
  接收:
   
    {
      status:操作是否成功(bool)
    }	
  
  url: "/studentProject?id=作品id(int)"

  # 8 新建比赛赛程：

  method: POST

  上传:
  
    {
      competitionName:赛事名称(string)
      acronym:赛事简称(string)
      startDate:开始日期(yyyy-mm-dd)
      submitDDL:提交截止(yyyy-mm-dd)
      checkDDL:初审截止(yyyy-mm-dd)
      reviewDDL:评审截止(yyyy-mm-dd)
      endDate:结果公布(yyyy-mm-dd)
      description:赛事描述(string)
    }	
  
  接收:
   
    {
      status:操作是否成功(bool)
    }	
  
  url: "/createCompetition"
  
  # 8 新建比赛赛程：

  method: GET

  上传:无
  
  接收:
   
    {
      competitionName:赛事名称(string)
      acronym:赛事简称(string)
      startDate:开始日期(yyyy-mm-dd)
      submitDDL:提交截止(yyyy-mm-dd)
      checkDDL:初审截止(yyyy-mm-dd)
      reviewDDL:评审截止(yyyy-mm-dd)
      endDate:结果公布(yyyy-mm-dd)
      description:赛事描述(string)
    }	
  
  url: "/competitionList"
