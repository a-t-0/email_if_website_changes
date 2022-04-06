# Code that automatically copies all issues of a repository to another
import os
from shutil import move

from code.project1.src.compare import compare, is_changed
from code.project1.src.send_email import send_email
from .control_website import gitlab_login
from .Hardcoded import Hardcoded
from .helper import get_browser_drivers
from .control_website import open_url
from .Website_controller import Website_controller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import time


class Main:
    """ """

    def __init__(self, project_nr, should_login=True):
        """Initialises object that gets the browser controller, then it gets the issues
        from the source repo, and copies them to the target repo.

        :param project_nr: [Int] that indicates the folder in which this code is stored.
        :param login: [Boolean] True if the website_controller object should be
        created and should login to GitHub.
        """
        sender_email = getpass("Type <your gmail account>@gmail.com and press enter: ")
        target_email=sender_email
        password = getpass("Type your password and press enter: ")
        message = 'ETHcc TICKETS ARE ON SALE!here is the email'

        # project_nr is an artifact of folder structure
        self.project_nr = project_nr
        self.relative_src_filepath = f"code/project{self.project_nr}/src/"
        # Store the hardcoded values used within this project
        self.hc = Hardcoded()

        # get browser drivers
        get_browser_drivers(self.hc)

        # website_controller = get_website_controller(self.hc)
        url="https://ethcc.io/tickets"
        image_name="tickets.png"

        
        for i in range(0,10):
            self.get_screenshot(url,image_name)
            website_changed=is_changed(image_name,f"old_{image_name}")
            if website_changed:
                send_email(sender_email,target_email,message,password)
        print(
            f"Done."
        )

    def rename_old_file_if_exists(self,src,dest):
        
        if os.path.isfile(src):
            move(src,dest)
        
    def get_screenshot(self,url, image_name):
        self.rename_old_file_if_exists(image_name,f"old_{image_name}")
        website_controller = Website_controller()
        website_controller.driver = open_url(website_controller.driver, url)
        website_controller.driver.execute_script("window.scrollTo(0, 1800)")
        time.sleep(6)

        screenshot = website_controller.driver.save_screenshot(image_name)

        
        
        # close website controller
        website_controller.driver.close()
        

if __name__ == "__main__":
    # initialize main class
    main = Main()
