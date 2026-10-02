
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


# Number of requests for this test run
MAX_REQUESTS = 100


# ==========================================
# START BRAVE
# ==========================================

print("Starting Brave...")

options = Options()
options.binary_location = (
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
)

driver = webdriver.Chrome(options=options)
driver.maximize_window()


try:
    # ==========================================
    # OPEN LINKEDIN
    # ==========================================

    print("Opening LinkedIn...")

    driver.get("https://www.linkedin.com/login")

    time.sleep(1)


    # ==========================================
    # MANUAL LOGIN
    # ==========================================

    print()
    print("==========================================")
    print("           LINKEDIN LOGIN")
    print("==========================================")
    print()
    print("Log in manually in Brave.")
    print("Complete any verification if requested.")
    print()
    print("Do NOT close Brave.")
    print()

    input("When you are fully logged in, press ENTER...")


    # ==========================================
    # OPEN MY NETWORK
    # ==========================================

    print()
    print("Opening My Network...")

    driver.get("https://www.linkedin.com/mynetwork/")

    time.sleep(5)

    print("My Network opened.")


    # ==========================================
    # SEND CONNECTION REQUESTS
    # ==========================================

    requests_sent = 0
    attempts = 0

    while requests_sent < MAX_REQUESTS:

        print()
        print("Searching for Connect buttons...")

        buttons = driver.find_elements(
            By.XPATH,
            "//button[normalize-space()='Connect']"
        )

        print("Connect buttons found:", len(buttons))


        if not buttons:

            print("No Connect buttons visible.")
            print("Scrolling for more people...")

            driver.execute_script(
                "window.scrollBy(0, 600);"
            )

            time.sleep(3)

            attempts += 1

            if attempts >= 5:
                print("Could not find additional Connect buttons.")
                break

            continue


        # Reset failed-search counter
        attempts = 0


        # Use the first visible Connect button
        button = buttons[0]


        try:

            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                button
            )

            time.sleep(1)

            print("Sending connection request...")

            button.click()

            time.sleep(2)


            # ==========================================
            # HANDLE OPTIONAL SEND BUTTON
            # ==========================================

            send_buttons = driver.find_elements(
                By.XPATH,
                "//button[normalize-space()='Send']"
            )

            if send_buttons:
                send_buttons[0].click()
                time.sleep(2)


            requests_sent += 1

            print(
                f"Request {requests_sent} of "
                f"{MAX_REQUESTS} sent."
            )


            # ==========================================
            # MOVE TO NEXT PEOPLE
            # ==========================================

            driver.execute_script(
                "window.scrollBy(0, 450);"
            )

            time.sleep(3)


        except Exception as error:

            print("Could not process this button.")
            print(type(error).__name__)

            driver.execute_script(
                "window.scrollBy(0, 400);"
            )

            time.sleep(2)


    # ==========================================
    # FINISHED
    # ==========================================

    print()
    print("==========================================")
    print("Finished.")
    print("Requests sent:", requests_sent)
    print("==========================================")

    input("Press ENTER to close Brave...")


except Exception as error:

    print()
    print("Something went wrong.")
    print("Error:", type(error).__name__)
    print(error)

    input("Press ENTER to close Brave...")


finally:

    try:
        driver.quit()
    except:
        pass

