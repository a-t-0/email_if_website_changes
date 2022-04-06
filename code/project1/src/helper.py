import getpass
import os
import time
import math
from selenium.webdriver.common.action_chains import ActionChains
from .Website_controller import Website_controller


def add_two(x):
    """Adds two to an incoming integer.

    :param x:

    """
    return x + 2


def do_browser():
    """Creates a browser object."""
    import selenium
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    driver = webdriver.Firefox(executable_path=r"firefox_driver/geckodriver")


def read_creds(hardcoded):
    """Reads username and password from credentials file,
    if the file exists, asks the user to manually enter them if the file is not found.

    TODO: verify this is not a duplicate method.

    :param hardcoded: An object containing all the hardcoded settings used in this program.

    """
    get_creds_if_not_exist(hardcoded)
    with open(hardcoded.cred_path, "r") as f:
        lines = []
        for line in f:
            lines.append(line)

    # creds.txt is changed to bash format in other project so the credentials need to be parsed
    # username = lines[0][:-1]
    # pswd = lines[1]
    username, pwd = parse_creds(lines)

    return username, pwd


def parse_creds(lines):
    username_identifier = "GITLAB_SERVER_ACCOUNT_GLOBAL="
    pwd_identifier = "GITLAB_SERVER_PASSWORD_GLOBAL="
    username = None
    pwd = None
    for line in lines:
        if line[: len(username_identifier)] == username_identifier:
            username = line[len(username_identifier) :]
        if line[: len(pwd_identifier)] == pwd_identifier:
            pwd = line[len(pwd_identifier) :]
    if not username is None:
        if not pwd is None:
            return username, pwd
        else:
            raise Exception("Did not get password.")
    else:
        raise Exception("Did not get username.")


def get_creds_if_not_exist(hardcoded):
    """Asks the user to enter the username and password for the login to the
    Radboud Universitiy Sports Center login.

    TODO: ask user to include 'read' before username and password,
    to indicate that they read the source code before entering their username
    and password (and verified that it is not shared). Give them a warning about
    security otherwise.

    :param hardcoded: An object containing all the hardcoded settings used in this program.

    """
    if not os.path.isfile(hardcoded.cred_path):
        username = getpass.getpass(prompt="What is your username for GitHub?")
        pwd = getpass.getpass(prompt="What is your password for GitHub?")

        f = open(hardcoded.cred_path, "a")
        f.write(f"{username}\n")
        f.write(pwd)
        f.close()


def get_labels_from_issues(issues):
    """

    :param issues: [List] of Issue objects containing the data (e.g. title, comments) of an issue.

    """
    labels = []
    for issue in issues:
        for label in issue.labels:
            labels.append(label.replace("%20", " "))
    unique_labels = list(set(labels))
    print(f"unique_labels={unique_labels}")
    return unique_labels


def loiter_till_gitlab_server_is_ready_for_login(
    hardcoded, scan_duration, interval_duration, website_controller
):
    # website_controller = Website_controller()

    for i in range(0, math.ceil(scan_duration / interval_duration)):
        # Refresh page
        try:
            # TODO: get the open_url function from the control_website.py file.
            website_controller.driver = open_url(
                website_controller.driver, hardcoded.gitlab_login_url
            )
            website_controller.driver.implicitly_wait(1)
        except:
            print("GitLab server was not yet ready to show website")

        print(
            f"Waiting for the GitLab server to get ready for {interval_duration} seconds"
        )
        time.sleep(interval_duration)

        # Only use this if a new state is found to find its unique characteristics
        # export_source(website_controller, f"source_{i}.txt")

        # Break loop if page is succesfully loaded.
        if check_if_login_page_is_loaded(website_controller):
            # GitLab server page is loaded correctly, can move on in script.
            break

    # close website controller
    website_controller.driver.close()
    print(
        "GitLab server is ready for first login. Code proceeding now to login and get GitLab runner Token."
    )


def check_if_login_page_is_loaded(website_controller):

    # This identifier only occurs in the first, and not-yet-ready stage.
    error_stage_identifier = (
        "The connection to the server was reset while the page was loading."
    )

    # This identifier only occurs in the second, and not-yet-ready stage.
    too_soon_stage_identifier = "GitLab is taking too much time to respond."

    # This identifier only occurs in the second, and ready stage.
    ready_stage_identifier = "Sign in"

    # Already logged into GitLab
    already_logged_in = "<title>Projects · Dashboard · GitLab</title>"

    # Verify if that condition is met.
    source = website_controller.driver.page_source
    if error_stage_identifier in source:
        return False
    elif too_soon_stage_identifier in source:
        return False
    elif ready_stage_identifier in source:
        return True
    elif already_logged_in in source:
        return True
    else:
        raise Exception(
            "The GitLab server webpage is in a state that is not yet known/recognised, its source code contains:{source}"
        )


def open_url(driver, url):
    """DUPLICATE, Remove
    Makes the browser open an url through the driver object in the webcontroller.

    :param driver: object within website_controller that can controll the driver.
    :param url: A link to a website.

    """
    driver.get(url)
    return driver


def export_source(website_controller, relative_filepath):
    source = website_controller.driver.page_source
    text_file = open(relative_filepath, "w")
    text_file.write(source)
    text_file.close()


def source_contains(website_controller, string):
    """USED
    Evaluates complete html source of the website that is being controlled, to determine
    if it contains the incoming string.
    Returns true if the string is found in the html source of the website, false if it is not found.

    :param website_controller: Object controlling the browser. Object that controls the browser.
    :param string: Set of characters that is searched for in the html code.

    """
    source = website_controller.driver.page_source
    source_contains_string = string in source
    return source_contains_string


def get_browser_drivers(hardcoded):
    """USED
    Installs wget and then uses that to download the firefox and chromium browser controller drivers.

    :param hardcoded: An object containing all the hardcoded settings used in this program.

    """
    os.system("yes | sudo apt install wget")

    firefox_driver_file_is_found = file_is_found(
        f"{hardcoded.firefox_driver_folder}/{hardcoded.firefox_driver_filename}",
        hardcoded,
    )

    if not file_is_found(
        f"{hardcoded.firefox_driver_folder}/{hardcoded.firefox_driver_filename}",
        hardcoded,
    ):
        get_firefox_browser_driver(hardcoded)
        install_firefox_browser()
    if not file_is_found(
        f"{hardcoded.chromium_driver_folder}/{hardcoded.chromium_driver_filename}",
        hardcoded,
    ):
        get_chromium_browser_driver(hardcoded)


def file_is_found(filepath, hardcoded):
    """

    :param filepath:
    :param hardcoded: An object containing all the hardcoded settings used in this program.

    """
    if os.path.isfile(filepath):
        return True
    else:
        return False


def get_firefox_browser_driver(hardcoded):
    """USED
    Creates a folder to store the firefox browser controller downloader and then downloads it into that.

    :param hardcoded: An object containing all the hardcoded settings used in this program.

    """
    # TODO: include os identifier and select accompanying file
    os.system(f"mkdir {hardcoded.firefox_driver_folder}")
    curl_firefox_drive = f"wget -O {hardcoded.firefox_driver_folder}/{hardcoded.firefox_driver_tarname} {hardcoded.firefox_driver_link}"
    os.system(curl_firefox_drive)
    # unpack_firefox_driver = (
    #    f"tar -xf {hardcoded.firefox_driver_folder}/{hardcoded.firefox_driver_tarname}"
    # )
    unpack_firefox_driver = f"tar -xf {hardcoded.firefox_driver_folder}/{hardcoded.firefox_driver_tarname} -C {hardcoded.firefox_driver_folder}/"
    print(f"unpacking with:{unpack_firefox_driver}")
    os.system(unpack_firefox_driver)


def install_firefox_browser():
    """USED"""
    install_firefox_browser = f"yes | sudo apt install firefox"
    print(f"install_firefox_browser:{install_firefox_browser}")
    os.system(install_firefox_browser)


def get_chromium_browser_driver(hardcoded):
    """USED
    Creates a folder to store the chromium browser controller downloader and then downloads it into that.
    TODO: include os identifier and select accompanying file

    :param hardcoded: An object containing all the hardcoded settings used in this program.

    """
    # mak dir
    os.system(f"mkdir {hardcoded.chromium_driver_folder}")
    # get the zip
    curl_chromium_drive = f"wget -O {hardcoded.chromium_driver_folder}/{hardcoded.chromium_driver_tarname} {hardcoded.chromium_driver_link}"
    os.system(curl_chromium_drive)
    # unpak the zip
    unpack_chromium_driver = f"unzip -d  {hardcoded.chromium_driver_folder}/{hardcoded.chromium_driver_filename} {hardcoded.chromium_driver_folder}/{hardcoded.chromium_driver_tarname}"
    os.system(unpack_chromium_driver)

    # move file one dir up
    move_chromium_driver = f"mv  {hardcoded.chromium_driver_folder}/{hardcoded.chromium_driver_filename}/{hardcoded.chromium_driver_unmodified_filename} {hardcoded.chromium_driver_folder}"
    print(move_chromium_driver)
    os.system(move_chromium_driver)
    # remove unpacked dir
    cleanup = (
        f"rm -r {hardcoded.chromium_driver_folder}/{hardcoded.chromium_driver_filename}"
    )
    print(cleanup)
    os.system(cleanup)

    # remove zip file
    cleanup = (
        f"rm -r {hardcoded.chromium_driver_folder}/{hardcoded.chromium_driver_tarname}"
    )
    print(cleanup)
    os.system(cleanup)

    # rename driver file name to include hardcoded version name
    rename_chromium_driver = f"mv  {hardcoded.chromium_driver_folder}/{hardcoded.chromium_driver_unmodified_filename} {hardcoded.chromium_driver_folder}/{hardcoded.chromium_driver_filename}"
    print(rename_chromium_driver)
    os.system(rename_chromium_driver)


def click_element_by_xpath(website_controller, xpath):
    """Clicks an html element based on its xpath.

    :param website_controller: Object controlling the browser. Object that controls the browser.
    :param xpath: A direct link to an object in an html page.

    """
    source_element = website_controller.driver.find_element_by_xpath(xpath)
    if "firefox" in website_controller.driver.capabilities["browserName"]:
        scroll_shim(website_controller.driver, source_element)

    # scroll_shim is just scrolling it into view, you still need to hover over it to click using an action chain.
    actions = ActionChains(website_controller.driver)
    actions.move_to_element(source_element)
    actions.click()
    actions.perform()
    return website_controller


def scroll_shim(passed_in_driver, object):
    """Scrolls down till object is found.

    :param passed_in_driver: An object within the object that controls an internet browser.
    :param object: Unknown, most likely an arbitrary html object..

    """
    x = object.location["x"]
    y = object.location["y"]
    scroll_by_coord = "window.scrollTo(%s,%s);" % (x, y)
    scroll_nav_out_of_way = "window.scrollBy(0, -120);"
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)


def write_string_to_file(string, output_path):
    """
    :param string: content you write to file
    :param output_path: Relative path to a file that is outputted.

    """
    with open(output_path, "w") as f:
        f.write(string)


def get_runner_registration_token_filepath():
    # get lines from hardcoded data
    lines = read_file_content("../src/hardcoded_variables.txt")
    runner_registration_token_filepath_identifier = (
        "RUNNER_REGISTRATION_TOKEN_FILEPATH="
    )
    runner_registration_token_filepath = None
    for line in lines:
        if (
            line[: len(runner_registration_token_filepath_identifier)]
            == runner_registration_token_filepath_identifier
        ):
            runner_registration_token_filepath = line[
                len(runner_registration_token_filepath_identifier) :
            ]
    if not runner_registration_token_filepath is None:
        # remove newline character
        print(f"FILEPATH=../{runner_registration_token_filepath.strip()}")
        return f"../{runner_registration_token_filepath.strip()}"
    else:
        raise Exception("Did not get runner_registration_token_filepath.")


def read_file_content(filepath):
    with open(filepath, "r") as f:
        lines = []
        for line in f:
            lines.append(line)
    return lines


def delete_file_if_exists(filepath):
    try:
        os.remove(filepath)
    except OSError:
        pass
