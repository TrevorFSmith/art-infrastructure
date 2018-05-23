from ai.factories import *
from selenium.webdriver.common.keys import Keys


DEFAULT_LOGIN = 'admin'
DEFAULT_EMAIL = 'admin@domain.com'


def admin_login(context):
    create_user(context, is_staff=True, is_superuser=True)
    context.client.login(username=DEFAULT_LOGIN, password=DEFAULT_LOGIN)
    return True


def nonadmin_login(context):
    create_user(context, is_staff=False, is_superuser=False)
    context.client.login(username=DEFAULT_LOGIN, password=DEFAULT_LOGIN)
    return True


def login(context):
    return admin_login(context)


def logout(context):
    context.client.logout()
    user = current_user(context)
    if user:
        user.delete()
    return True


# def selenium_start(context):
#     from selenium import webdriver
#     # PhantomJS()
#     # Firefox
#     context.browser = webdriver.PhantomJS()
#     # context.browser = webdriver.Firefox()
#     context.browser.implicitly_wait(3)
#     # context.browser.set_page_load_timeout(30)
#     return True


# def selenium_stop(context):
#     context.browser.quit()
#     return True


def create_user(context, is_staff=True, is_superuser=True):
    try:
        user = User.objects.filter(email=DEFAULT_EMAIL)[0]
    except IndexError:
        user = User.objects.create_user(DEFAULT_LOGIN, DEFAULT_EMAIL, DEFAULT_LOGIN,
                                        is_staff=is_staff, is_superuser=is_superuser)
    return user


def current_user(context):
    try:
        return User.objects.filter(email=DEFAULT_EMAIL)[0]
    except IndexError:
        pass
    return None
