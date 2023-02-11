from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "C:\\Users\\61481\\PycharmProjects\\Hello World\\WebScraping\\chromedriver.exe"

wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com.au/search?q=bass+guitar&tbm=isch&ved=2ahUKEwj_v4iVl439AhUCG7cAHeJYBlwQ2-cCegQIABAA&oq=bass&gs_lcp=CgNpbWcQARgCMgQIIxAnMgcIABCxAxBDMgcIABCxAxBDMgcIABCxAxBDMgcIABCxAxBDMgQIABBDMgQIABBDMggIABCABBCxAzIFCAAQgAQyBAgAEENQAFgAYM0SaABwAHgAgAHJAogByQKSAQMzLTGYAQCqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=R2PnY7-AIIK23LUP4rGZ4AU&bih=937&biw=1920&hl=en-GB"
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb KAlRDb")
            for image in images:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print("Failed -", e)

urls = get_images_from_google(wd, 1, 6)

for i, url in enumerate(urls):
    download_image("imgs/", url, str(i) + ".jpg")

wd.quit()
