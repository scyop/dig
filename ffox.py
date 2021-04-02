from selenium import webdriver
import requests
import time
import os
import re


Image_Folder = 'Images_1'
def main():
    if not os.path.exists(Image_Folder):
        os.mkdir(Image_Folder)
    download_images()


def download_images():
    data = input("What to search: ")
    num_images = int(input('Enter the number of images you want: '))
    search_url = f'https://www.google.com.vn/search?q={data}&tbm=isch&hl=en&tbs=isz:l&authuser=0&sa=X&ved=0CAEQpwVqFwoTCMjZnNPj3O8CFQAAAAAdAAAAABAG&biw=1903&bih=973'
    browser=webdriver.Firefox()
    browser.get(search_url)
    #response = browser.page_source    
    pattern = r"(\[\"https://.*\.jpg.*[0-9]+,[0-9]+\])"
    #print(len(response),"\n",len(re.findall(pattern, response)))

    #scroll den het trang:
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        try: 
            button = browser.find_element_by_css_selector("input.mye4qd")
            time.sleep(3)
            button.click()
            print("found button !!!")
        except:
            print("Continue scrolling ...")

        if lastCount==lenOfPage:
            match=True
    #browser.refresh()
    response = browser.page_source
    print(len(response),"\n",len(re.findall(pattern, response)))                 
    count = 0
    imagelinks= []
    for index, image in enumerate(re.findall(pattern, response)):    	  	
        link = eval(image)[0]
        imagelinks.append(link)
        count = count + 1        
        if (count >= num_images):
            break
    print(f"Download {num_images} images from total of {len(re.findall(pattern, response))} images found")
    print('Downloading ...')
    for i, imagelink in enumerate(imagelinks):
        # open each image link and save the file
        response = requests.get(imagelink)      
        imagename = Image_Folder + '/' + data + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)
    browser.close()
    print('Download Completed!')


if __name__ == '__main__':
    main()


###".mye4qd"
