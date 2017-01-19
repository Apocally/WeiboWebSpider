# coding = utf-8
from selenium import webdriver
from tkinter import *
import urllib.request


def get_cookies(username,password):
    cookies = {}
    flag = ''
    global CAPTCHA
    driver = webdriver.PhantomJS(executable_path='phantomjs')  # 放在Script文件中
    driver.get(r'http://weibo.cn/pub/')
    login_button = driver.find_element_by_link_text('登录')
    login_button.click()
    driver.find_element_by_name('mobile').send_keys(username)
    driver.find_element_by_xpath(r'/html/body/div[2]//input[@type="password"]').send_keys(password)
    captcha_img_url = driver.find_element_by_xpath('/html/body/div[2]/form//img').get_attribute('src')
    urllib.request.urlretrieve(captcha_img_url, 'captcha.gif')
    show()
    driver.find_element_by_name('code').send_keys(CAPTCHA)
    driver.find_element_by_name('submit').click()
    if driver.title == '微博':
        flag = 'failed'
        print('登录失败')
    else:
        print('Collecting Cookie……')
        for item in driver.get_cookies():
            cookies[item['name']] = item['value']
            flag = 'succeeded'
        print('登录成功')
    try:
        root.destroy()
    except:
        pass
    return cookies, flag


root = Tk()
# root.resizable(False,False)
root.title = 'Captcha'
captcha_text = StringVar()


def submit():
    global CAPTCHA
    CAPTCHA = captcha_text.get()
    root.destroy()


def show():
    photo = PhotoImage(file='captcha.gif')
    Label(root, image=photo, width=100, height=20).grid(row=0, column=0)
    Entry(root, text=captcha_text).grid(row=1, column=0)
    Button(root, command=submit, text='提交并关闭').grid(row=2, column=0)
    root.mainloop()


# if __name__ == '__main__':
#     Login()



