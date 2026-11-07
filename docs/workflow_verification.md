# 实验二自动评分流程验证

验证日期：2026-11-07。

## 本地功能验证

- 教师参考实现通过31项环境、T/S、连接、释放与整合测试，以及4项身份关联测试，共35项。
- 四帧、两组连接、两个方向共16次实际字节核对通过；冲突拒绝、释放及另一连接保留通过。
- 完整参考交付按公开规则得到100/100；未完成模板得到5/100，明确区分环境成功与核心功能未完成。
- 私有名单中37组姓名与完整学号均通过匹配检查；完整名单没有进入Git历史或公开代码。

## 真实跨Fork验证

模拟Fork：https://github.com/plan-lab-szu/lab02-dsnetwork-e2e

测试PR：https://github.com/jwentong/Experimenet02-DSNetwork-Bidirectional-Speech/pull/2

1. 使用未完成模板创建PR，提交触发器自行启动教师评分，得到5/100。故意使用未匹配身份时，机器人明确提示修改标题，不写入真实学生记录。
2. 向原分支补交仅支持空闲输出的不完整T实现，自动重新评分为8.33/100，T项仅通过1/6测试。
3. 修改PR为流程测试标题，自动重新关联到模拟记录，不计入37人成绩。
4. 最终运行中的grade、publish、board三个任务均成功，PR评论指向当前学生提交，Issue #1包含37条脱敏记录，真实学生均保持未提交。

首次评分：https://github.com/jwentong/Experimenet02-DSNetwork-Bidirectional-Speech/actions/runs/42339132610

最终评分与看板：https://github.com/jwentong/Experimenet02-DSNetwork-Bidirectional-Speech/actions/runs/42339664281

全程未点击Approve workflows，未手工调用评分workflow_dispatch。workflow_dispatch由受信任的PR元数据触发器自动调用。测试Fork由教师可管理的组织持有，不代表使用了某位真实学生的账号。

## 权限与记录

学生代码只在无凭据、禁网络、非root、只读文件系统和资源受限容器运行。反馈与看板在独立可信任务运行。成绩看板采用同一评分流程的依赖任务，不依赖跨工作流完成事件，也不提升评分反馈任务的actions:read权限。

教师已授权将37人名单加密保存为CLASS_ROSTER_JSON。公开看板与CSV的姓名、学号脱敏，保留名单序号供教师对应本地名单。Secret仅由身份关联与看板任务使用，不传入评分容器。

Word规范9页、讲授课件16页均已在本机Office渲染并逐页检查；课件使用宋体及逐步显示动画。教师完整源码仅保留本地.teacher目录，不在学生模板中公开。
