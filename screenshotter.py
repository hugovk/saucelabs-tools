import new
import os
import sys
import unittest
from sauceclient import SauceClient
from selenium import webdriver

# Run tests in parallel like this:
# py.test -n2 --boxed screenshotter.py
# Or on Windows:
# py.test -n2 screenshotter.py

# Set your Sauce Labs credentials as environment variables
USERNAME = os.environ.get('SAUCE_USERNAME')
ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')
sauce = SauceClient(USERNAME, ACCESS_KEY)

# Test site details
# SITE_USERNAME = "TODO"
# SITE_PASSWORD = "TODO"
# SITE_URL = ("http://%s:%s@www.example.com/" %
#            (SITE_USERNAME, SITE_PASSWORD))
# Some browsers give phishing warnings for URLs with @, so it's easier to
# temporarily make the site public and use this:
SITE_URL = "http://www.example.com/"
OUTDIR = "output"

browsers = [
    # Windows 8.1
    {"platform": "Windows 8.1", "browserName": "firefox", "version": "31"},
    {"platform": "Windows 8.1", "browserName": "firefox", "version": "30"},
    {"platform": "Windows 8.1", "browserName": "firefox", "version": "29"},
    {"platform": "Windows 8.1", "browserName": "chrome", "version": "36"},
    {"platform": "Windows 8.1", "browserName": "chrome", "version": "35"},
    {"platform": "Windows 8.1", "browserName": "chrome", "version": "34"},
    {"platform": "Windows 8.1", "browserName": "internet explorer",
     "version": "11"},

    # Windows 8
    {"platform": "Windows 8", "browserName": "firefox", "version": "31"},
    {"platform": "Windows 8", "browserName": "firefox", "version": "30"},
    {"platform": "Windows 8", "browserName": "firefox", "version": "29"},
    {"platform": "Windows 8", "browserName": "chrome", "version": "36"},
    {"platform": "Windows 8", "browserName": "chrome", "version": "35"},
    {"platform": "Windows 8", "browserName": "chrome", "version": "34"},
    {"platform": "Windows 8", "browserName": "internet explorer",
     "version": "10"},

    # Windows 7
    {"platform": "Windows 7", "browserName": "firefox", "version": "31"},
    {"platform": "Windows 7", "browserName": "firefox", "version": "30"},
    {"platform": "Windows 7", "browserName": "firefox", "version": "29"},
    {"platform": "Windows 7", "browserName": "chrome", "version": "36"},
    {"platform": "Windows 7", "browserName": "chrome", "version": "35"},
    {"platform": "Windows 7", "browserName": "chrome", "version": "34"},
    {"platform": "Windows 7", "browserName": "internet explorer",
     "version": "11"},
    {"platform": "Windows 7", "browserName": "internet explorer",
     "version": "10"},
    {"platform": "Windows 7", "browserName": "internet explorer",
     "version": "9"},
    {"platform": "Windows 7", "browserName": "opera", "version": "12"},
    {"platform": "Windows 7", "browserName": "opera", "version": "11"},

    # Mavericks
    {"platform": "OS X 10.9", "browserName": "firefox", "version": "30"},
    {"platform": "OS X 10.9", "browserName": "firefox", "version": "29"},
    {"platform": "OS X 10.9", "browserName": "firefox", "version": "28"},
    {"platform": "OS X 10.9", "browserName": "chrome", "version": "35"},
    {"platform": "OS X 10.9", "browserName": "chrome", "version": "34"},
    {"platform": "OS X 10.9", "browserName": "chrome", "version": "33"},
    # phishing warning:
    {"platform": "OS X 10.9", "browserName": "safari", "version": "7"},

    # Mountain Lion
    {"platform": "OS X 10.8", "browserName": "chrome", "version": "35"},
    {"platform": "OS X 10.8", "browserName": "chrome", "version": "34"},
    {"platform": "OS X 10.8", "browserName": "chrome", "version": "33"},
    {"platform": "OS X 10.8", "browserName": "safari", "version": "6"},

    # Linux
    {"platform": "Linux", "browserName": "chrome", "version": "36"},
    {"platform": "Linux", "browserName": "chrome", "version": "35"},
    {"platform": "Linux", "browserName": "chrome", "version": "34"},
    {"platform": "Linux", "browserName": "firefox", "version": "31"},
    {"platform": "Linux", "browserName": "firefox", "version": "30"},
    {"platform": "Linux", "browserName": "firefox", "version": "29"},
    {"platform": "Linux", "browserName": "opera", "version": "12"},

    # iPhone

    {"platform": "OS X 10.9", "browserName": "iPhone", "version": "7.1",
     "device-orientation": "portrait"},  # phishing warning
    {"platform": "OS X 10.9", "browserName": "iPhone", "version": "7.0",
     "device-orientation": "portrait"},
    {"platform": "OS X 10.8", "browserName": "iPhone", "version": "6.1",
     "device-orientation": "portrait"},

    # iPad
    {"platform": "OS X 10.9", "browserName": "iPad", "version": "7.1",
     "device-orientation": "portrait"},  # phishing warning
    {"platform": "OS X 10.9", "browserName": "iPad", "version": "7.0",
     "device-orientation": "portrait"},
    {"platform": "OS X 10.8", "browserName": "iPad", "version": "6.1",
     "device-orientation": "portrait"},

    # Android
    {"platform": "Linux", "browserName": "Android", "version": "4.4",
     "device-orientation": "portrait"},
    ]


def create_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)
    return decorator


@on_platforms(browsers)
class ScreenshotTest(unittest.TestCase):
    def setUp(self):
        self.desired_capabilities['name'] = self.id()

        caps = self.desired_capabilities
        self.outfile = "platform_" + self.desired_capabilities['platform'] \
            + "-browser_" + caps['browserName'] \
            + "-v_" + caps['version'] + ".png"
        self.outfile = os.path.join(OUTDIR, self.outfile)
        print self.outfile
        create_dir(OUTDIR)

        if os.path.isfile(self.outfile):
            self.skipTest(("File", self.outfile, "already exists. Skipping."))
            # return

        sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_capabilities,
            command_executor=sauce_url % (USERNAME, ACCESS_KEY)
        )
        self.driver.implicitly_wait(30)

    def test_screenshot(self):
        print "get page"
        self.driver.get(SITE_URL)

        print "save screenshot"
        self.driver.get_screenshot_as_file(self.outfile)

    def tearDown(self):
        print("Link to your job: https://saucelabs.com/jobs/%s"
              % self.driver.session_id)
        try:
            if sys.exc_info() == (None, None, None):
                sauce.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()
