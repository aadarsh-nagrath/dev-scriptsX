from seleniumbase import SB
import time
import base64
import uuid

prompt = "A futuristic car"

# Define a function to verify the success
def verify_success(sb):
    sb.assert_element('img.min-w-min.mb-4', timeout=4)
    sb.sleep(3)

def main_script():
    # Main script with SeleniumBase
    with SB(uc=True,headless=True) as sb:
        try:
            # Open the URL and try to handle any Cloudflare checks
            print("Navigating to the webpage...")
            sb.uc_open_with_reconnect("https://stabledifffusion.com/tools/ai-image-generator", 3)

            # Attempt to bypass Cloudflare CAPTCHA
            try:
                print("Trying to bypass Cloudflare verification...")
                if sb.is_element_visible('input[value*="Verify"]'):
                    sb.uc_click('input[value*="Verify"]')  # Click the verification checkbox
                    print("Verification checkbox clicked.")
                else:
                    sb.uc_gui_click_captcha()  # Handle CAPTCHA manually if it's displayed
                    print("Captcha Failed")
                    main_script()
                    return
            except Exception as e:
                print("Error bypassing CAPTCHA (ignoring this error): ", e)
                pass

            # Verify success after bypassing the CAPTCHA
            try:
                verify_success(sb)
            except Exception as e:
                print(f"Error verifying success: {e}")

            # Wait until the text area is visible
            print("Waiting for the text area to be visible...")
            try:
                text_area = sb.wait_for_element("textarea[class*='min-h-'][rows='3']", timeout=30)
            except Exception as e:
                print(f"Error finding the text area: {e}")
                main_script()
                return

            # Enter the text into the text area if it's found
            if text_area:
                print("Entering text into the text area...")
                text_area.send_keys(prompt)
            else:
                print("Text area not found, skipping input.")

            # Wait for the "Generate" button to become clickable and enabled
            print("Waiting for the generate button to be enabled...")
            time.sleep(2)
            try:
                button = sb.find_element("xpath", "//button[contains(text(), 'Generate')]")
                button.click()
                print("Button clicked successfully!")
            except Exception as e:
                print(f"An error occurred: {e}")

            # Add a delay to allow for image generation
            print("Waiting for image generation...")
            sb.sleep(10)

            # Wait until the image element is visible
            print("Waiting for the image to be visible...")
            try:
                image_element = sb.find_element("xpath", '//img[@alt="Stable Diffusion" and contains(@class, "mb-4")]')
            except Exception as e:
                print(f"Error finding the image: {e}")
                main_script()
                return

            if image_element:
                print("Retrieving the image source URL...")
                image_src = image_element.get_attribute("src")

            if image_src:
                if image_src.startswith("data:image"):
                                # Handle Base64-encoded image data
                                print("Decoding Base64 image data...")
                                base64_data = image_src.split(",")[1]  # Remove the 'data:image/jpg;base64,' part
                                image_data = base64.b64decode(base64_data)
                
                                file_name = str(uuid.uuid4()) + ".jpg"
                                with open(file_name, "wb") as file:
                                    file.write(image_data)

                                print(f"Image decoded and saved successfully as {file_name}.")
                else:
                    print("Unexpected image source format.")

        except Exception as e:
            print(f"Unexpected error: {e}")

        # Browser will stay open even if errors occur
        print("Browser session will stay open for inspection.")
        sb.sleep(1)

main_script()