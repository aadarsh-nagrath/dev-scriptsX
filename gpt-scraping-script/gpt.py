# problem with the script: the script only cares about response under 3 seconds. So no big response is possible yet.
from seleniumbase import SB

prompt = "What is the meaning of life?"

def verify_success(sb):
    sb.assert_element('div[contenteditable="true"]', timeout=4)
    sb.sleep(3)

def main_script():
    # Main script with SeleniumBase
    with SB(uc=True, headless=True) as sb:
        try:
            sb.uc_open_with_reconnect("https://chatgpt.com/", 3)

            try:
                verify_success(sb)
            except Exception as e:
                print(f"Error verifying success: {e}")

            try:
                input_field = sb.wait_for_element(
                    'div[contenteditable="true"]', timeout=30
                )
            except Exception as e:
                print(f"Error finding the input field: {e}")
                main_script()
                return

            if input_field:
                input_field.send_keys(prompt)

            try:
                button = sb.find_element(
                    "xpath",
                    '//button[@aria-label="Send prompt" and @data-testid="send-button"]',
                )
                button.click()
                # print("Button clicked successfully!")
            except Exception as e:
                print(f"An error occurred: {e}")

            # print("Waiting for the response message...")
            sb.sleep(1)

            # Wait until the response element is visible
            print("Waiting for the response element to be visible...")
            try:
                response_element = sb.find_element(
                    "xpath", '//div[contains(@class, "markdown")]/p'
                )
            except Exception as e:
                print(f"Error finding the response element: {e}")
                pass

            if response_element:
                sb.sleep(3)
                response_message = response_element.text
                print(f"Response message: {response_message}")
            else:
                print("Response element not found.")

        except Exception as e:
            print(f"Unexpected error: {e}")

main_script()
