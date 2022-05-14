<h1 align="center">UESTC 自动健康打卡</h1>

电子科技大学研究生每日自动健康打卡。

# 本项目已失效，[这个项目](https://github.com/xiong233/uestc_report_playwright) 暂时还活着

## 前言

1、本项目将在每天早上7点半左右通过信息门户账号登陆[健康打卡系统](https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/*default/index.do) 进行健康打卡。

2、本项目打卡所提交的内容（比如是否留校，是否隔离等）取决于你昨天的打卡内容，如果有变化请及时手动更新自己的状态。

3、本项目创立的初衷在于技术交流、相互学习，而并非为学生提供打卡服务。因此，该项目不对提供的服务质量作出保障。

4、如果您决定使用该项目所提供的服务，那么其带来的一切后果，均将由您个人承担，与原作者、贡献者无关。

## 使用教程

1、点击右上角Fork本项目。

2、进入到Fork后的项目，点击Action，开启workflow。

3、依次点击Setting-Secrets-Actions。

点击右上角New repository secret；在name下输入username，在value下输入你的学号；保存。

点击右上角New repository secret；在name下输入password，在value下输入你的密码；保存。

4、至此部署完成，每天早上将会自动打卡，如果你没有禁用 GitHub 的邮件通知，打卡失败将收到邮件提醒。

5、如果你想关闭自动打卡，点击Action-DailyReport，再点击右上角三个小圆点，在下拉栏里点击Disable workflow。

## 其他

1、Github服务器有时候会打不开学校的打卡网站(早上居然进不去电脑端的打卡网站)，因此本项目将会在第一次打卡失败后再尝试一次，但只要第一次打卡失败你就会收到邮件提醒。

2、本项目的滑动验证识别部分用的[onion-rain/uestc_health_report](https://github.com/onion-rain/uestc_health_report) 的代码。

3、由于Selenium总会被判定为爬虫，所以用的Pyppeteer实现（各种坑还搜不到解决方案）。