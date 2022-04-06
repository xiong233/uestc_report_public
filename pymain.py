import asyncio
import pdb
from pyppeteer import launch
import tkinter
import base64
from slide import SlideCrack
from time import time, sleep
import sys
# from pyppeteer import launcher
# launcher.DEFAULT_ARGS.remove("--enable-automation")

username = sys.argv[1]
password = sys.argv[2]

check_button = '#app > div > div.mint-tabbar.mt-bg-lv3.mt-bColor-grey-lv6.is-fixed > a.mint-tab-item.is-selected > div.mint-tab-item-icon > i'
add_button = '#app > div > div.mint-layout-container.pjcse52gj > div.mint-fixed-button.mt-color-white.sjarvhx43.mint-fixed-button--bottom-right.mint-fixed-button--primary.mt-bg-primary'
save_button = "#app > div > div > div.mint-layout-container.OPjctwlgzsl > button"
confirm_button = "body > div.mint-msgbox-wrapper > div > div.mint-msgbox-btns > button.mint-msgbox-btn.mint-msgbox-confirm.mt-btn-primary"


async def get_decode_image(page):
    await page.waitForSelector('#img1', {"timeout":10000})
    src = await page.Jeval('#img1', 'e => e.outerHTML')
    im_base64 = src.split(',')[1].split('"')[0]  # 拿到base64编码的图片信息
    im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
    with open('bg.png', 'wb') as f:  # 保存图片到本地
        f.write(im_bytes)
    # pdb.set_trace()

    src = await page.Jeval('#img2', 'e => e.outerHTML')
    im_base64 = src.split(',')[1].split('"')[0]  # 拿到base64编码的图片信息
    im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
    with open('front.png', 'wb') as f:  # 保存图片到本地
        f.write(im_bytes)

async def log_in(page):
    # url = 'https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/index.do#/dailyReport'
    url = 'https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/*default/index.do'
    await page.goto(url)
    await page.type("#mobileUsername", username)
    await page.type("#mobilePassword", password)
    await page.click("#load")
    # pdb.set_trace()
    for i in range(5):
        try:
            await asyncio.sleep(1)
            await get_decode_image(page)
            image1 = "./front.png"
            # 背景图片
            image2 = "./bg.png"
            # 处理结果图片,用红线标注
            image3 = "./3.png"
            sc = SlideCrack(image1, image2, image3)
            distance = int((sc.discern()) * 0.48)  # 280/590
            print(distance)
            # pdb.set_trace()
            await asyncio.sleep(0.1)
            # 滑动验证：获取要位置的距离

            elem = await page.waitForSelector('#captcha > div > div.sliderMask > div', {"timeout": 2000})
            await elem.hover()
            await page.mouse.down()
            await page.waitFor(400)
            await page.mouse.move(int(page.mouse._x + distance - 2), 5, {'steps': 35})
            await page.waitFor(800)
            await page.mouse.up()
            print("Loading...")
            await page.waitFor(2000)

        except:
            print("Error loading or swiping captcha image.")
            continue

        try:
            await page.waitForSelector("#mobileUsername", {"timeout": 1000})
            print("Verification failed")
            continue
        except:
            print("Verified")
            return
    # 5次滑动都不过
    await page.waitForSelector(check_button, {"timeout": 10000})


async def main():
    # 浏览器 启动参数
    start_parm = {
        # 启动chrome的路径
        "executablePath": "chrome-win/chrome.exe",
        # 关闭无头浏览器 默认是无头启动的
        "headless": False,
        "args": [
            '--disable-infobars',  # 关闭自动化提示框
            '--log-level=30',  # 日志保存等级， 建议设置越好越好，要不然生成的日志占用的空间会很大 30为warning级别
            '--no-sandbox',  # 关闭沙盒模式
            '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            # '--start-maximized',  # 窗口最大化模式
        ],
    }
    # 创建浏览器对象，可以传入 字典形式参数
    browser = await launch(**start_parm)

    page = await browser.newPage()
    # tk = tkinter.Tk()
    # width = tk.winfo_screenwidth()
    # height = tk.winfo_screenheight()
    # tk.quit()
    await page.setViewport(viewport={'width': 800, 'height': 800})
    # pdb.set_trace()

    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                     '{ webdriver:{ get: () => false } }) }')

    for i in range(3):
        try:
            await log_in(page)
            print("Login successful")
            break
        except:
            print("Login failed")
            continue
    logtime = time()
    try:
        await page.waitForSelector(check_button, {"timeout": 30000})
    except:
        print("Reload page")
        await page.reload()
    print("Check login status:", time()-logtime)
    await page.waitForSelector(check_button, {"timeout": 30000})
    print("Check login status:", time()-logtime)

    await page.waitFor(5000)

    try:
        add = await page.waitForSelector(add_button, {"timeout": 10000})
        await add.click()
        print("Add OK ", time() - logtime)
        await page.waitFor(1000)
        await page.keyboard.press('ArrowDown', {"delay": 500})
        sleep(1)
        save = await page.waitForSelector(save_button, {"timeout": 10000})
        await save.click()
        print("Save OK ", time() - logtime)
    except:
        print("Repeat report")
        await browser.close()
        return

    await page.waitFor(1000)
    confirm = await page.waitForSelector(confirm_button, {"timeout": 10000})
    await confirm.click()
    print("Confirm OK ", time() - logtime)

    await page.waitFor(1000)
    await browser.close()
    print("Successfully reported")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
