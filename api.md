# 作品阶段

  未提交，已提交，初审中，初审通过，初审未通过，评审中，进入答辩，未进入答辩，现场答辩，获奖，未获奖
  
# 竞赛阶段

  未开始，作品提交，团委初审，专家评审，现场答辩，奖项公布，已结束

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
        display(length = 8):[
          多选框值(bool)
        ,...]
        research(length = 15):[
          多选框值(bool)
        ,...]
        partner:[{
          nameOfPartner:姓名(string)
          studentIDOfPartner:学号(int)
          phoneOfPartner:联系电话(int)
          emailOfPartner:邮箱(string)
          currenteducationOfPartner:现学历(0-3)
        },..]
        files:[
          path:作品文件保存路径(string)
          filename:文件名(string)
        ,...]
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
  
  # 6 请求一个可用作品代码：

  method: POST

  上传:无
  
  接收:
   
    {
      code:一个可用的作品代码(string)
    }	
  
  url: "/studentProject"
  
  # 7 保存or提交作品信息：

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
      display(length = 8):[
        多选框值(bool)
      ,...]
      research(length = 15):[
        多选框值(bool)
      ,...]
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
      status:赛事阶段(string)
    }	
  
  接收:
   
    {
      status:操作是否成功(bool)
    }	
  
  url: "/competition"
  
  # 9 查看竞赛详情：

  method: GET

  上传:无
  
  接收:
   
    {
      id:竞赛id(int)
      competitionName:赛事名称(string)
      competitionStatus:竞赛状态(string)
      acronym:赛事简称(string)
      startDate:开始日期(yyyy-mm-dd)
      submitDDL:提交截止(yyyy-mm-dd)
      checkDDL:初审截止(yyyy-mm-dd)
      reviewDDL:评审截止(yyyy-mm-dd)
      endDate:结果公布(yyyy-mm-dd)
      description:赛事描述(string)
      status:赛事阶段(string)
      files:[{
        path:竞赛文件路径(string)
        name:文件名字(string)
      },...]
    }	
  
  url: "/competition?id=竞赛id(int)"
  
   # 10 上传文件：

  method: POST

  上传:
  
    {
    
    }
  
  接收:
   
    {
      "code": 上传是否成功(bool)
    }	
  
  url: "/file?type=文件类型(0-2)&projectID=作品id(int)" 0(图片) / 1(文档) / 2(音频)
  
   # 11 删除文件：

  method: DELETE

  上传:
  
    {
      filename:文件名(string)
    }
  
  接收:
   
    {
      "code": 删除是否成功(bool)
    }	
  
  url: "/file?type=文件类型(0-2)&projectID=作品id(int)" 0(图片) / 1(文档) / 2(音频)
  
   # 12 获取文件：

  method: GET

  上传:无
  
  接收:
   
    {
      files:[{
        filename:文件名(string),
        path:存储地址(string),
        type:文件类型(0-2）,
        datasize:文件大小(double)
      },...]
    }	
  
  url: "/file?projectID=作品id(int)" 0(图片) / 1(文档) / 2(音频)
  
   # 13 获取提交表：

  method: GET

  上传:无
  
  接收:
   
    {
      path:申请表的保存路径(string)
    }	
  
  url: "/submitfile?projectID=作品id(int)"
  
  # 14 团委竞赛作品列表获取：

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
        avgGrade:平均分(double)
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
        display(length = 8):[
          多选框值(bool)
        ,...]
        research(length = 15):[
          多选框值(bool)
        ,...]
        partner:[{
          nameOfPartner:姓名(string)
          studentIDOfPartner:学号(int)
          phoneOfPartner:联系电话(int)
          emailOfPartner:邮箱(string)
          currenteducationOfPartner:现学历(0-3)
        },..]
      },...]
      
      
    }	
  
  url: "/studentProject？competitionID=竞赛id(int)"
  
  # 15 团委竞赛列表获取：

  method: GET

  上传:无
  
  接收:
  
    {
      data:[{
        id:数据库中的序号(int)
        competitionName:竞赛名称(string)
        competitionStatus:竞赛状态(string)
        
      },...]
      
      
    }	
  
  url: "/competition"
  
# 16 专家评审作品列表获取：

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
        display(length = 8):[
          多选框值(bool)
        ,...]
        research(length = 15):[
          多选框值(bool)
        ,...]
        partner:[{
          nameOfPartner:姓名(string)
          studentIDOfPartner:学号(int)
          phoneOfPartner:联系电话(int)
          emailOfPartner:邮箱(string)
          currenteducationOfPartner:现学历(0-3)
        },..]
      },...](只传当前竞赛的作品)
      
      
    }	
  
  url: "/studentProject?expertID=专家账号(int)&id=作品id(int)" 
  
  # 17 团委查看作品评分：

  method: GET

  上传:无
  
  接收:
  
    {
      avgGrade:平均分(double)
      grades:[{
        name:某专家名字(string)
        grade:某专家的评分(double)
        advise:某专家的建议(string)
      },...]
    }	
  
  url: "/schoolProjectGrade?id=作品id(int)"
  
  # 18 专家查看作品评分：

  method: GET

  上传:无
  
  接收:
  
    {
      grade:评分(double)
      advise:建议(string)
    }	
  
  url: "/expertProjectGrade?id=作品id(int)"
  
  # 19 专家打分：

  method: POST

  上传:
  
    {
      grade:评分(double)
      advise:建议(string)
    }
  
  接收:
  
    {
      status:是否修改成功(bool)
    }	
  
  url: "/expertProjectGrade?expertID=专家id(int)&id=作品id(int)"
  
  # 20 团委上传竞赛文件：

  method: POST

  上传:
  
    {
    
    }
  
  接收:
   
    {
      "code": 上传是否成功(bool)
    }	
  
  url: "/competitionFile?competitionID=竞赛id(int)"
  
   # 21 团委删除竞赛文件：

  method: DELETE

  上传:
  
    {
      filename:文件名(string)
    }
  
  接收:
   
    {
      "code": 删除是否成功(bool)
    }	
  
  url: "/competitionFile?competitionID=竞赛id(int)"
  
   # 22 团委获取竞赛文件：

  method: GET

  上传:无
  
  接收:
   
    {
      files:[{
        filename:文件名(string),
        path:存储地址(string),
        datasize:文件大小(double)
      },...]
    }	
  
  url: "/competitionFile?competitionID=竞赛id(int)"

  # 23 团委导入专家信息：

  method: POST

  上传:
  
    {
      
    }
  
  接收:
   
    {
      [{
        name:专家姓名(string)
        account:专家账号(string)
        yield:专家领域(string)
      },..]
    }	
  
  url: "/expertInfo"
  
  # 24 修改比赛数据：

  method: PUT

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
      status:赛事阶段(string)
    }	
  
  接收:
   
    {
      status:操作是否成功(bool)
    }	
  
  url: "/competition?id="+竞赛id(string)
  
  # 25 团委获取专家信息：

  method: GET

  上传:文件
  
  接收:
   
    {
      [{
        name:专家姓名(string)
        account:专家账号(string)
        yield:专家领域(string)
      },..]
    }	
  
  url: "/expertInfo"
  
  # 26 获取打包文件
  
  method: POST
  
  上传：
  
    {
      id:[project id,.....]
    }
    
  接受：
  
    {
      filepath: 压缩包路径
    }
    
  url: "/zipProject?expertID=专家id"
