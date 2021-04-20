from selenium import webdriver
import requests
import time
import os
import re

from os import listdir
from os.path import isfile, join
from pathlib import Path
import numpy
import cv2
import csv


import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


Image_Folder = 'Images_1'
csv_folder = 'csv'
def main():
    if not os.path.exists(Image_Folder):
        os.mkdir(Image_Folder)
    if not os.path.exists(csv_folder):
        os.mkdir(csv_folder)
    download_images()
    digi()
    stats()


def download_images():
    data = input("What to search: ")
    num_images = int(input('Enter the number of images you want: ' + '\n' + 'Note: Input (-1), id you want skip image downloading  ' + '\n') )
    if num_images == -1:return
    search_url = f'https://www.google.com.vn/search?q={data}&tbm=isch&hl=en&tbs=isz:l&authuser=0&sa=X&ved=0CAEQpwVqFwoTCMjZnNPj3O8CFQAAAAAdAAAAABAG&biw=1903&bih=973'
    #browser=webdriver.Firefox()
    browser=webdriver.Chrome()
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


#xu ly so hoa anh

def digi():
    # Check whether the CSV 
    # exists or not if not then create one.
    my_file = Path("csv/details.csv")
    
    if my_file.is_file():
        f = open(my_file, "w+")
        with open('csv/details.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow(["S.No.", "Name", "Height",
                            "Width", "Channels",
                            "Avg Blue", "Avg Red",
                            "Avg Green"])
        f.close()
        pass
        
    else:
        with open('csv/details.csv', 'w', newline = '') as file:
            writer = csv.writer(file)
            
            writer.writerow(["S.No.", "Name", "Height",
                            "Width", "Channels",
                            "Avg Blue", "Avg Red",
                            "Avg Green"])

    #Image_Folder = 'Image_1'
    mypath = os.getcwd() + '/' + Image_Folder
    
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    images = numpy.empty(len(onlyfiles), dtype = object)
    
    for n in range(0, len(onlyfiles)):
        
        path = join(mypath,onlyfiles[n])
        images[n] = cv2.imread(join(mypath,onlyfiles[n]),
                            cv2.IMREAD_UNCHANGED)
        
        try : 
            img = cv2.imread(path)
            h,w,c = img.shape
            print(h, w, c)
        except:
            print("Image error found !!! Skip image ...")
            continue
        
        avg_color_per_row = numpy.average(img, axis = 0)
        avg_color = numpy.average(avg_color_per_row, axis = 0)
        
        with open('csv/details.csv', 'a', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow([n+1, onlyfiles[n], h, w, c, 
                            avg_color[0], avg_color[1],
                            avg_color[2]])
            file.close()


# cac so lieu thong ke va ve bieu do
def stats():
    my_file = Path("csv/details.csv")
    df = pd.read_csv(my_file)
    print(df.columns)
    print('Min of height: ' + str(df['Height'].min()))
    print('Max of height: ' + str(df['Height'].max()))
    print('Average of height: ' + str(df['Height'].mean()))
    print('Median of height: ' + str(df['Height'].median()))
    print('Std of height: ' + str(df['Height'].std()))
    print('Var of height: ' + str(df['Height'].var()))

    sns.set_style("whitegrid")
    sns.set_context("notebook", font_scale=1.25)

    f, ax = plt.subplots(figsize=(12,7))
    ax = sns.distplot(df['Height'], norm_hist=True)
    ax.set_title('Histogram of heights')

    f,ax2=plt.subplots(figsize=(12,7))
    sns.distplot(df['Avg Blue'], hist = True, kde =True, label='Avg Blue', color='blue', bins=100)
    sns.distplot(df['Avg Red'], hist = True, kde = True, label='Avg Red', color='red', bins=100)
    sns.distplot(df['Avg Green'], hist = True, kde = True, label='Avg Green', color='green', bins=100)
    # Plot formatting
    plt.legend(prop={'size': 12})
    plt.title('RGB Histogram')
    plt.xlabel('Value')
    plt.ylabel('Density')  

    plt.show()

if __name__ == '__main__':
    main()


###".mye4qd"
