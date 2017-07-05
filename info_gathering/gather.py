#!/usr/bin/python

from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os, re, imp
from interactive import print_good, print_error, print_status, prompt
from ConfigParser import ConfigParser, NoOptionError, NoSectionError
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



def repeatOnError(fn, test, *args, **kwargs):
    while(True):
        try:
            x = fn(*args, **kwargs)
        except Exception as e:
            print_error('{}: {}'.format(type(e), e.message))
            sleep(1)
            continue
        if(test(x)):
            return x

class Web(object):
    path = os.path.dirname(os.path.realpath(__file__))
    def __init__(self, credfile, headless=False):
        self.creds = ConfigParser()
        self.creds.read(credfile)
        self.headless = headless
    def start(self):
        if self.headless:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
                "(KHTML, like Gecko) Chrome/15.0.87")
            self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
            self.driver.set_window_size(1024, 768)
        else:
            self.driver = webdriver.Chrome('/usr/bin/chromedriver')
    def setValue(self, element, value):
        if element.tag_name == 'textarea':
            self.driver.execute_script('arguments[0].innerText = arguments[1]', element, value)
        elif element.tag_name == 'select':
            self.driver.execute_script('arguments[0].value = arguments[1]', element, value)
        else:
            self.driver.execute_script('arguments[0].setAttribute("value", arguments[1])', element, value)
    def clickOn(self, s):
        self.driver.find_element_by_css_selector(s).click()
    def screenshot(self, filename):
        if self.headless:
            sleep(4)
        else:
            prompt('Adjust window for screenshot and press Enter')
        self.driver.save_screenshot(filename)
        print_status('Saved screenshot to ' + filename)

    def getCredentials(self, section):
        creds = {}
        try:
            creds['email'] = self.creds.get(section, 'email')
            creds['password'] = self.creds.get(section, 'password')
        except NoOptionError, NoSectionError:
            print_error("Credentials for %s not found" % section)
            return None
        return creds

    def goData(self, domain):
        creds = self.getCredentials('data.com')
        if creds == None:
            return
        self.driver.get('https://connect.data.com/')
        print_status('logging in to connect.data.com')
        self.driver.find_element_by_css_selector('#loginButton > div').click()
        self.driver.find_element_by_id('j_username').send_keys(creds['email'])
        self.driver.find_element_by_id('j_password').send_keys(creds['password'])
        self.driver.find_element_by_css_selector('#login_btn > span').click()
        print_status('using domain ' + domain)
        self.setValue(self.driver.find_element_by_id('homepageSBS'), domain)
        self.clickOn('#homepageSearchIcon')
        repeatOnError(self.clickOn, lambda x: True, '#findCompanies > div.search-result.general-display-none > div.column-right > div.result-table > table > tbody > tr > td.td-name.name > a')

        self.screenshot('Company Information Available on data.com.png')
        self.driver.find_element_by_xpath('//a[contains(., "see all")]').click()

        self.screenshot('Employee Information Available on data.com.png')

        with open(os.path.join(self.path, 'data.js')) as f:
            script = f.read()
        names = []
        while True:
            #self.driver.execute_script(script)
            names += [name.text.encode('utf-8') for name in 
                    self.driver.find_elements_by_css_selector('.td-name') if re.match('\S', name.text) is not None]
            try:
                self.clickOn('img#next.table-navigation-next-image-active')
            except NoSuchElementException:
                break
        print_status('executing script to extract names')

        with open('names.data', 'w') as f:
            f.write('\n'.join(names))
        print_status('Saved %d names to "names.data"' % len(names))
        print_good('Finished enumeration using data.com')
        print

    def goHunter(self, domain):
        creds = self.getCredentials('hunter.io')
        if creds == None:
            return
        self.driver.get('https://hunter.io/users/sign_in')
        self.driver.find_element_by_id('email-field').send_keys(creds['email'])
        self.driver.find_element_by_id('password-field').send_keys(creds['password'])
        print_status('logging in to hunter.io')
        self.clickOn('#signin_form > div.board-box > button')
        self.setValue(self.driver.find_element_by_id('domain-field'), domain)
        self.clickOn('#search-btn')
        print_status('using domain ' + domain)

        self.screenshot('Email Enumeration of ' + domain + ' using hunter.io.png')

        def showAll():
            try:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                button = self.driver.find_element_by_css_selector('button.show-more')
                sleep(1)
            except NoSuchElementException:
                return True
            if button.text == 'Show more':
                button.click()
                return False
            else:
                return True
        repeatOnError(showAll, lambda x: x)

        with open(os.path.join(self.path, 'hunterio.js')) as f:
            self.driver.execute_script(f.read())

        with open('emails.hunter', 'w') as f:
            emails = self.driver.find_elements_by_css_selector('p:nth-child(1) > div')
            for email in emails:
                f.write(email.text.encode('utf-8') + "\n")
            print_status('Saved %d emails to emails.hunter' % len(emails))
        print_good('Finished enumeration using hunter.io')
        print

    def goFacebook(self, company):
        creds = self.getCredentials('Facebook')
        if creds == None:
            return
        self.driver.get('https://www.facebook.com')
        self.setValue(self.driver.find_element_by_id('email'), creds['email'])
        self.setValue(self.driver.find_element_by_id('pass'), creds['password'])
        print_status('logging in to Facebook')
        self.clickOn('#loginbutton input')
        self.driver.get('https://searchisback.com/')
        self.setValue(self.driver.find_element_by_id('people-pronoun'), 'ANY')
        self.setValue(self.driver.find_element_by_id('company'), company)
        self.clickOn('#people button.submit')
        self.screenshot('Employee Information Available on Facebook.png')
        def scroller(max=75):
            num_scrolls = {'n':0, 'max': max}
            def scrollToBottom():
                print_status("{}: Scrolling for more results on Facebook".format(num_scrolls['n']))
                num_scrolls['n']+=1
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                try:
                    self.driver.find_element_by_id('browse_end_of_results_footer')
                except NoSuchElementException:
                    if num_scrolls['n'] < num_scrolls['max']:
                        return False
                return True
            return scrollToBottom

        repeatOnError(scroller(), lambda x: x)

        with open(os.path.join(self.path, 'searchisback.js')) as f:
            self.driver.execute_script(f.read())
        with open('names.facebook', 'w') as f:
            names = self.driver.find_elements_by_tag_name('div')
            for name in names:
                f.write(name.text.encode('utf-8') + "\n")
        print_status('Saved %d names to "names.facebook"' % len(names))
        print_good('Finished enumeration using searchisback')
        print
    def goDiscover(self, domain):
        if "HOME" not in os.environ:
            print_error("Don't know where to find discover files ($HOME not set)")
            return False
        path = 'file:///{}/data/{}'.format(os.environ['HOME'], domain)
        self.driver.get(path + '/data/hosts.htm')
        self.screenshot('Host Enumeration {} using discover.png'.format(domain))
        self.driver.get(path + '/pages/netcraft.htm')
        self.screenshot('Network History and Information of {} using discover.png'.format(domain))
        self.driver.get(path + '/data/emails.htm')
        self.screenshot('Email Enumeration of {} using discover.png'.format(domain))
        emails = self.driver.find_element_by_tag_name('pre').text
        print_status('Saving {} emails to emails.discover'.format(len(emails.split('\n'))))
        with open('emails.discover', 'w') as f:
            f.write(emails)
        self.driver.get(path + '/data/names.htm')
        self.screenshot('Name Enumeration of {} using discover.png'.format(domain))
        names = self.driver.find_element_by_tag_name('pre').text
        print_status('Saving {} names to names.discover'.format(len(names.split('\n'))))
        with open('names.discover', 'w') as f:
            f.write(names)

if __name__ == "__main__":
    from optparse import OptionParser
    from socket import getaddrinfo, gaierror

    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option('-c', '--credentials', dest="credential_file", help="ini style file with credentials")
    parser.add_option('-n', '--company', help='company name')
    parser.add_option('-d', '--domain', help='company domain')
    parser.add_option('-l', '--headless', action="store_true", help='use phantomjs for headless operation')
    (options, args) = parser.parse_args()
    if options.credential_file is None or options.company is None or options.domain is None:
        parser.print_usage()
        parser.print_help()
        exit(1)
    if not os.path.isfile(options.credential_file):
        print_error("'{}' is not a file".format(options.credential_file))
        exit(1)
    if re.match('\S', options.company) is None:
        print_error("'{}' is not a valid company name".format(options.company))
        exit(1)
    if re.match('[^\.]{1,63}(\.[^\.]{1,63})+', options.domain) is None:
        print_error("'{}' is not a valid domain".format(options.domain))
        exit(1)
    try:
        getaddrinfo(options.domain, None)
    except gaierror:
        print_error("DNS lookup of '{}' failed".format(options.domain))
        exit(1)


    w = Web(options.credential_file, headless=options.headless)
    w.start()
    w.goData(options.domain)
    w.goHunter(options.domain)
    w.goFacebook(options.company)
    w.goDiscover(options.domain)
    w.driver.close()
