from seleniumbase import SB
import time
import requests
import uuid

prompt = "A dragon tatto with a phoenix on the back"

def verify_success(sb):
    sb.assert_element('div.relative img', timeout=4)
    sb.sleep(3)

def main_script():
    with SB(uc=True, headless=True) as sb:
        try:
            print("Navigating to the webpage...")
            sb.uc_open_with_reconnect("https://inkgen.ai/design", 3)

            try:
                verify_success(sb)
            except Exception as e:
                print(f"Error verifying success: {e}")

            print("Waiting for the text area to be visible...")
            try:
                text_area = sb.wait_for_element("textarea[placeholder='Use 5+ words...']", timeout=30)
            except Exception as e:
                print(f"Error finding the text area: {e}")
                main_script()
                return

            # Enter the text 
            if text_area:
                print("Entering text into the text area...")
                text_area.send_keys(prompt)
            else:
                print("Text area not found, skipping input.")

            print("Waiting for the generate button to be enabled...")
            try:
                button = sb.find_element("xpath", "//button//span[contains(text(), 'Generate')]")
                button.click()
                print("Button clicked successfully!")
            except Exception as e:
                print(f"An error occurred: {e}")

            print("Waiting for image generation...")
            sb.sleep(3)

            print("Waiting for the image to be visible...")
            try:
                image_element = sb.find_element("xpath", '//img[@alt="Tattoo Design"]')
            except Exception as e:
                print(f"Error finding the image: {e}")
                pass

            if image_element:
                print("Retrieving the image source URL...")
                image_src = image_element.get_attribute("src")

                if image_src:
                    response = requests.get(image_src)
                    if response.status_code == 200:
                        file_name = str(uuid.uuid4()) + ".png"
                        with open(file_name, "wb") as file:
                            file.write(response.content)
                        print("Image downloaded successfully!")
                    else:
                        print(f"Failed to download image. Status code: {response.status_code}")
                else:
                    main_script()
                    return

        except Exception as e:
            print(f"Unexpected error: {e}")

main_script()
