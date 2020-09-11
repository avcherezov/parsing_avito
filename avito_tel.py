from selenium import webdriver
from PIL import Image
from pytesseract import image_to_string


class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.navigate()


    def take_screenshot(self):
        self.driver.save_screenshot('avito_screenshot.png')


    def tel_recon(self):
        image = Image.open('tel.gif')
        print(image_to_string(image))


    def crop(self, location, size):
        image = Image.open('avito_screenshot.png')
        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        image.crop((x, y, x+width, y+height)).save('tel.gif')
        self.tel_recon()


    def navigate(self):
        self.driver.get('https://www.avito.ru/moskva/avtomobili/kia_sportage_2020_1979245980')

        button = self.driver.find_element_by_xpath('//div[@class="item-phone js-item-phone"]')
        button.click()

        self.take_screenshot()

        image = self.driver.find_element_by_xpath('//div[@class="item-phone-big-number js-item-phone-big-number"]//*')
        location = image.location
        size = image.size

        self.crop(location, size)


def main():
    b = Bot()


if __name__ == '__main__':
    main()
