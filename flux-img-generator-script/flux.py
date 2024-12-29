from seleniumbase import SB
import time

prompt = "Astronaut on the moon with Earth in the background."

download_script = """
const imageUrl = document.querySelector('img').src;
const a = document.createElement('a');
a.href = imageUrl;
a.download = 'image.png';
document.body.appendChild(a);
a.click();
document.body.removeChild(a);
"""

# Define a function to verify the success
def verify_success(sb):
    sb.assert_element('div.relative img', timeout=4)
    sb.sleep(3)

# Function to delete the backdrop blur div if it exists
def delete_backdrop_blur(sb):
    try:
        # Locate the backdrop blur div and remove it
        backdrop_blur = sb.find_element("xpath", "//div[contains(@class, 'backdrop-blur-md')]")
        sb.execute_script("arguments[0].remove();", backdrop_blur)
        print("Backdrop blur div removed.")
    except Exception as e:
        print("No backdrop blur div found.")

def main_script():

    with SB(uc=True, headless=True) as sb:
        try:
            print("Navigating to the webpage...")
            sb.uc_open_with_reconnect("https://freeflux.ai/ai-image-generator", 3)

            try:
                verify_success(sb)
            except Exception as e:
                print(f"Error verifying success: {e}")

            print("Waiting for the text area to be visible...")
            try:
                text_area = sb.find_element("//textarea[@placeholder='Describe']")
            except Exception as e:
                print(f"Error finding the text area: {e}")
                main_script()
                return

            if text_area:
                print("Entering text into the text area...")
                text_area.clear()
                text_area.send_keys(prompt)
            else:
                print("Text area not found, skipping input.")

            print("Waiting for the generate button to be enabled...")
            sb.execute_script("window.scrollBy(0, 300);") 
            try:
                button = sb.find_element("xpath", "//button[contains(text(), 'Generate')]")
                button.click()
                print("Button clicked successfully!")
            except Exception as e:
                print(f"An error occurred: {e}")
                main_script()
                return

            print("Waiting for image generation...")
            delete_backdrop_blur(sb)
            print("Waiting for the image to be visible...")
            try:
                image_element = sb.find_element("xpath", '//img[@class="block cursor-pointer"]')
            except Exception as e:
                print(f"Error finding the image: {e}")
                pass

            if image_element:
                print("Retrieving the image source URL...")
                image_src = image_element.get_attribute("src")

                if image_src and image_src.startswith("blob:"):
                    print("Blob URL detected, trying to open it in a new tab...")
                    # Open a new tab with the blob URL
                    sb.execute_script(f"window.open('{image_src}', '_blank');")
                    sb.execute_script(download_script)
                    print(f"Blob URL opened in a new tab: {image_src}")
                    sb.sleep(1)

        except Exception as e:
            print(f"Unexpected error: {e}")

main_script()
