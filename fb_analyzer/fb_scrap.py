import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import dateparser
import time


# initialize webdriver
def init_driver():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
        "(KHTML, like Gecko) Chrome/15.0.87"
    )
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.maximize_window()
    driver.wait = WebDriverWait(driver, 5)
    return driver


# login in facebook
def login(driver, email, password):
    url = "https://www.facebook.com"
    driver.get(url)
    time.sleep(4)
    driver.save_screenshot("use.png")
    email_element = driver.find_element_by_name("email")
    email_element.send_keys(email)
    pass_element = driver.find_element_by_name("pass")
    pass_element.send_keys(password)
    f = driver.find_element_by_id("loginbutton")
    f.click()
    time.sleep(4)
    try:
        time.sleep(6)
        driver.find_element_by_class_name("linkWrap")
        return True
    except NoSuchElementException:
        print("Fail to login")
        return False


# go to user page
def go_to_id(id, driver):
    url = "https://www.facebook.com/" + id
    driver.get(url)


# load all friends
def load_friends(driver):
    old = len(driver.find_elements_by_class_name("uiProfileBlockContent"))
    new = -1
    count = 0
    while old != new and count <= 3:
        elements = driver.find_elements_by_class_name('_698')
        element = elements[-1]
        new = old
        ActionChains(driver).move_to_element(element).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(10)
        time.sleep(4)
        old = len(driver.find_elements_by_class_name("uiProfileBlockContent"))
        if old == new:
            count += 1


# load all posts ( or number posts, which we setup) and click to load all comments
def load_posts(driver):
    element = driver.find_element_by_id("timeline_tab_content_extra")
    old = len(driver.find_elements_by_class_name("_1dwg"))
    new = -1
    count = 0
    while new <= 30 and count <= 3:
        new = old
        ActionChains(driver).move_to_element(element).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(5)
        try:
            comment_links = driver.find_elements_by_class_name("UFIPagerLink")
            for comment_link in comment_links:
                comment_link.click()
        except NoSuchElementException:
            "not found"
        try:
            sub_comment_links = driver.find_elements_by_class_name("UFIReplySocialSentenceLinkText")
            for sub_comment_link in sub_comment_links:
                sub_comment_link.click()
        except:
            "not found"
        old = len(driver.find_elements_by_class_name("_1dwg"))
        if old == new:
            count += 1


# take all friend's href
def take_friends(driver):
    friends = []  # list of friend's href
    element = driver.find_elements_by_class_name("_6-6")
    friends_tab = element[2]
    friends_tab.click()
    time.sleep(4)
    try:
        driver.find_element_by_class_name("uiSearchInput")
        load_friends(driver)
        f = driver.find_element_by_id("pagelet_timeline_medley_friends")
        soup = BeautifulSoup(f.get_attribute('innerHTML'), 'html.parser')
        for i in soup.find_all('div', class_='uiProfileBlockContent'):
            friends.append(i.find('a').get('href'))
        return friends
    except:
        print("User hasn't friends or has only subscribes")


# take id from href
def id_from_href(friends):
    friends_id = []
    try:
        for i in friends:
            str = ""
            if i.find("profile.php") == -1:
                a = i.rfind("com/")
                b = i.find("?")
                str = i[a + 4:b]
                friends_id.append(str)
            else:
                a = i.find("?")
                b = i.find("&")
                str = i[a + 4:b]
                friends_id.append(str)
        return friends_id
    except:
        print("user hasn't friends or hide it")


# take id from href for one src
def id_from_one_href(href):
    final_id = ""
    try:
        if href.find("profile.php") == -1:
            a = href.rfind("com/")
            b = href.find("?")
            str = href[a + 4:b]
            final_id = str
        else:
            a = href.find("?")
            b = href.find("&")
            str = href[a + 4:b]
            final_id = str
        return final_id
    except:
        print("user hasn't friends or hide it")


# parse all posts on user page
def parse_page(driver, id):
    comm_name = []  # comment's user
    comm_time = []  # comment's time
    post_user = []  # post's user
    post_time = []  # post's time
    all_active = []  # all activity
    try:
        url = "https://www.facebook.com/" + id
        driver.get(url)
        time.sleep(4)
        load_posts(driver)
    except:
        print("Not load posts")
    try:
        p = driver.find_element_by_id("recent_capsule_container")
        soup = BeautifulSoup(p.get_attribute('innerHTML'), 'html.parser')
        for i in soup.find_all('a', class_=' UFICommentActorName'):
            if i.get_text() == "":
                comm_name.append("comment's_no")
            else:
                comm_name.append(i.get('href'))
        for j in soup.find_all('abbr', class_='UFISutroCommentTimestamp'):
            if j.get('title') == "":
                comm_time.append("com's_time_no")
            else:
                comm_time.append(dateparser.parse(str(j.get('title'))))
        for j in soup.find_all('h5'):
            if j.get_text() == "":
                post_user.append("noname")
            else:
                post_user.append(j.find('a').get('href'))
        for i in soup.find_all('abbr', class_='_5ptz'):
            if i.get('title') == "":
                post_time.append("notime")
            else:
                post_time.append(dateparser.parse(str(i.get('title'))))
        post_user = id_from_href(post_user)
        comm_name = id_from_href(comm_name)
        for i in range(len(post_user)):
            help = []
            help.append(post_user[i])
            help.append(post_time[i])
            help.append("Post")
            all_active.append(help)
        for i in range(len(comm_name)):
            help = []
            help.append(comm_name[i])
            help.append(comm_time[i])
            help.append("Comment")
            all_active.append(help)
        return all_active
    except:
        print("can't parse page")


# clean activity from users, who is'n friend
def clean(all_active, friends):
    clean_active = []  # list for friend's active
    for activity in all_active:
        if activity[0] in friends:
            clean_active.append(activity)
    return clean_active


# find last friend's activity
def find_last_active(all_active):
    for i in range(len(all_active) - 1, -1, -1):
        for j in range(len(all_active) - 1, -1, -1):
            if all_active[i][0] == all_active[j][0]:
                a = dateparser.parse(str(all_active[i][1]))
                b = dateparser.parse(str(all_active[j][1]))
                a = a.timestamp()
                b = b.timestamp()
                if a < b:
                    all_active.pop(i)
                else:
                    continue
    return all_active


# change date type of activities
def change_date(all_active):
    for active in all_active:
        active[1] = active[1].isoformat(' ')
    return all_active


# find all likes
def likes_on_post(friends, driver):
    likes = []
    posts = driver.find_elements_by_class_name("userContentWrapper")
    for post in range(len(posts)):
        print(post)
        try:
            a = driver.find_element_by_class_name("_2x4v")[post]
            time = driver.find_element_by_class_name("_5ptz")[post].get_attribute("title")
            a.click()
            time.sleep(5)
            f = driver.find_element_by_class_name("uiScrollableAreaWrap")
            sou = BeautifulSoup(f.get_attribute('innerHTML'), 'html.parser')
            for friend in sou.find_all('div', class_="_5j0e"):
                if id_from_one_href(friend.find('a').get('href')) in friends:
                    helps = []
                    helps.append(id_from_one_href(friend.find('a').get('href')))
                    helps.append(dateparser.parse(time))
            close = driver.find_element_by_class_name("_50z-")
            close.click()
            time.sleep(5)
        except:
            continue
    return likes


def main(user_id):
    email = ""
    password = ""
    driver = init_driver()
    login(driver, email, password)
    driver.save_screenshot("use1.png")
    go_to_id(user_id, driver)
    time.sleep(4)
    friends = take_friends(driver)
    driver.save_screenshot("use3.png")
    friends = id_from_href(friends)
    all_active = parse_page(driver, user_id)
    all_active = clean(all_active, friends)
    all_active = find_last_active(all_active)
    all_active = change_date(all_active)
    driver.save_screenshot("use4.png")
    driver.quit()
    return all_active


if __name__ == '__main__':
    user_id = sys.argv[1]
    main(user_id)