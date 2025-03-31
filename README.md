# Urban Routes Test Automation

## Project Description

This project automates the testing of the Urban Routes web application using Selenium WebDriver. It covers various functionalities, including setting routes, requesting a taxi, adding a payment card, entering a phone number, and adding special requests for the ride.

## Technologies and Techniques

-   **Python:** The primary programming language used for scripting the tests.
-   **Selenium WebDriver:** Used for automating web browser interactions.
-   **Chrome WebDriver:** Specifically used for controlling the Chrome browser.
-   **pytest:** A testing framework for writing and running tests.
-   **XPath and CSS Selectors:** Used for locating web elements.
-   **WebDriverWait and Expected Conditions:** Used for handling dynamic web elements and ensuring elements are interactable before actions.
-   **Page Object Model:** The `UrbanRoutesPage` class represents the web page and encapsulates its elements and actions.
-   **Logging (Performance):** Used to retrieve the SMS code from the network logs.

## Files

-   **`main.py`:** Contains the test scripts and the `UrbanRoutesPage` class.
-   **`data.py`:** Contains test data such as URLs, addresses, phone numbers, and card details.

## Setup

1.  **Install Python:** Ensure you have Python 3.6 or later installed.
2.  **Install Dependencies:** Run the following command to install the required Python packages:

    ```bash
    pip install selenium pytest
    ```

3.  **Download ChromeDriver:** Download the ChromeDriver executable that matches your Chrome browser version and place it in a directory included in your system's PATH.

## Running the Tests

1.  **Navigate to the Project Directory:** Open your terminal and navigate to the directory containing `main.py` and `data.py`.
2.  **Run pytest:** Execute the following command to run the tests:

    ```bash
    pytest main.py -v -s
    ```

    -   `-v` (verbose) provides detailed output.
    -   `-s` disables output capturing, allowing print statements to be displayed.

## Test Cases

The `main.py` file includes the following test cases:

-   `test_set_route`: Tests setting the "from" and "to" addresses.
-   `test_request_taxi`: Tests requesting a taxi and selecting the "Comfort" option.
-   `test_phone_number`: Tests entering a phone number and verifying the SMS code.
-   `test_add_card`: Tests adding a payment card.
-   `test_message_driver`: Tests entering a message for the driver.
-   `test_requests_for_the_ride`: Tests adding special requests for the ride.

## Important Notes

-   The `retrieve_phone_code` function is used to extract the SMS verification code from the network logs. This function should only be called after the application has requested the code.
-   Ensure that the ChromeDriver version matches your Chrome browser version to avoid compatibility issues.
-   The tests assume that the web application is running at the URL specified in `data.py`.
-   The `time.sleep(10)` function at the end of the `test_requests_for_the_ride` test case is used to allow time for the application to process the request. Adjust the sleep time as needed.
-   The XPaths used in the code are very specific, if the application UI changes, the XPaths will need to be updated.