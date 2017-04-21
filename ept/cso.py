from time import sleep
from selenium import webdriver

def getTitleFromFilename(filename):
    title = os.path.basename(filename)
    title = os.path.splitext(title)[0]
    title = re.sub('\.\d+$', '', title)
    title = re.sub('%', '/', title)
    #if len(title) > 70:
    #   raise Exception("Figure title too long")
    return title[:70]

def repeatOnError(fn, test, *args, **kwargs):
    while(True):
        try:
            x = fn(*args, **kwargs)
        except:
            sleep(1)
            continue
        if(test(x)):
            return x

class CSO(object):
    def start(self):
        self.driver = webdriver.Chrome('/usr/lib/chromium/chromedriver')
        self.driver.get('https://cso.tracesecurity.com/')
        self.login()
        pass
    def login(self):
        self.driver.find_element_by_id('username').send_keys('dselig')
        self.driver.find_element_by_id('password').send_keys('pa$$4Trace')
        self.driver.find_element_by_id('LoginButton').click()

    def setValue(self, element, value):
        if element.tag_name == 'textarea':
            self.driver.execute_script('arguments[0].innerText = arguments[1]', element, value)
        else:
            self.driver.execute_script('arguments[0].setAttribute("value", arguments[1])', element, value)
    def clickOn(self, s):
        self.driver.find_element_by_css_selector(s).click()
    def analyzeVulnerabilities(self):
        self.clickOn('#MyAssignments')
        sleep(2)
        self.clickOn('#ui-accordion-accordion-panel-1 > div:nth-child(6) > a')
    def getVulnerabilities(self):
        vulns = []
        vulnLinks = self.driver.find_elements_by_css_selector('#vulnTable>tbody>tr>td:nth-child(2)>a')
        for idx in range(len(vulnLinks)):
            v = repeatOnError(
                    lambda: self.driver.find_elements_by_css_selector('#vulnTable>tbody>tr>td:nth-child(2)>a')[idx],
                    lambda: True)
            v.click()
            vInfo = repeatOnError(lambda: self.driver.find_element_by_id('Vulnerability'))
            name = vInfo.find_element_by_css_selector('table > tbody > tr:nth-child(1) > td.FormContent').text
            print "adding vulnerability", name

            nodes = repeatOnError(lambda: self.driver.find_elements_by_css_selector('#tableAssets>tbody>tr'),
                                lambda x: len(x) > 0)
            for n in nodes:
                parts = [x.text for x in n.find_elements_by_css_selector('td')]
                print "adding node", parts[7]
                vulns.append([name] + parts[7:])
            p = self.driver.find_element_by_xpath('//div[div[@id="dialogVulnDetails"]]')
            p.find_element_by_css_selector('button[title="close"]').click()
        return vulns
    def addFigure(self, filename):
        iframe = self.driver.find_element_by_css_selector('iframe')
        self.driver.switch_to.frame(iframe)
        try:
            upload_radio = self.driver.find_element_by_id('figureTypeImage')
            upload_radio.click()

            file_input = self.driver.find_element_by_css_selector('#figureFile')
            file_input.send_keys(filename)

            title_input = self.driver.find_element_by_css_selector('#title')
            self.setValue(title_input, getTitleFromFilename(filename))
            #title_input.send_keys("\t")
            #sleep(.1)
            self.driver.find_element_by_css_selector('#AttachButton > input[type="submit"]').click()
        except:
            self.driver.switch_to.default_content()
            raise
        self.driver.switch_to.default_content()


    def openManualVulnerabilites(self):
        self.driver.find_element_by_xpath('//div[@class="InnerFormTitle" and contains(., "Manual Vulnerabilities")]/img[contains(@src, "plus.gif")]').click()

    def addVulnerability(self, directory):
        self.driver.find_element_by_xpath('//a[contains(., "Add Vulnerability")]').click()
        #block = self.driver.find_element_by_xpath('//div[@class="InnerFormTitle" and contains(., "Manual Vulnerabilities")]/following-sibling::div')
        #tbody = block.find_element_by_tag_name('tbody')
        #manvulns = tbody.find_elements_by_css_selector('.RowmanualVulnerabilites')
        #curvuln = manvulns[len(manvulns) - 1]
        inputs = self.driver.find_elements_by_xpath('//td[contains(., "Name:")]/following-sibling::td/textarea')
        with open(os.path.join(directory, "name")) as f:
            self.setValue(inputs[len(inputs) - 2], f.read())
            inputs[len(inputs) - 2].send_keys("\t")
        inputs = self.driver.find_elements_by_xpath('//td[contains(., "Description:")]/following-sibling::td/textarea')
        with open(os.path.join(directory, "description")) as f:
            self.setValue(inputs[len(inputs) - 2], f.read())
            inputs[len(inputs) - 2].send_keys("\t")
        inputs = self.driver.find_elements_by_xpath('//td[contains(., "Remediation:")]/following-sibling::td/textarea')
        with open(os.path.join(directory, "remediation")) as f:
            self.setValue(inputs[len(inputs) - 2], f.read())
            inputs[len(inputs) - 2].send_keys("\t")

        addnotes = self.driver.find_elements_by_xpath('//a[contains(., "Add/Update Notes")]')
        addnotes[len(addnotes) - 2].click()
        notesdir = os.path.join(directory, 'notes')
        is_first_note = True
        for rel_notedir in os.listdir(notesdir):
            notedir = os.path.join(notesdir, rel_notedir)
            if os.path.exists(os.path.join(notedir, 'figures')):
                if not is_first_note:
                    self.driver.find_element_by_xpath('//a[contains(., "Add Note")]').click()
                sleep(.2)
                notes = self.driver.find_elements_by_css_selector('.RowInitialNote textarea')
                with open(os.path.join(notedir, 'note')) as f:
                    self.setValue(notes[len(notes) - 2], f.read())
                
                with open(os.path.join(notedir, 'figures')) as f:
                    for fig in f:
                        print 'Adding "{}"'.format(fig.strip())
                        addfigures = self.driver.find_elements_by_xpath('//a[contains(., "Add Figure")]')
                        addfigures[len(addfigures) - 2].click()
                        sleep(1)
                        self.addFigure(fig.strip())
                        sleep(1)
            else:
                print "Skipping", notedir

            is_first_note = False
        self.driver.find_element_by_xpath('//input[@type="submit" and @value="Save"]').click()

    def addAppendixFigure(self, filename):
        add_button = self.driver.find_element_by_xpath('//*[@id="tabContent"]/form/fieldset[3]/a')
        add_button.click()
        sleep(1)
        self.addFigure(filename)
