**This is a lipstick try and recommendation project.**

## Group Information
* Section: 1
* Group Name:  Columbia_Analysts
* Group Members:
  * Jianyao Fu (jf3186)
  * Jing Qian (jq2286)
  * Zheng Wang (zw2520)
  * Yongcheng Zhu( yz3461)

## Project Overview
Our main goal of this project is to allow people who either do not have time or the ability to come to a physical beauty store to try lipsticks. Therefore, we have built a program that allows users to upload their self-images and to choose any color they would like to try on their lips. The program will then take these user inputs and apply the color chosen by the user to his or her self-image to show how the color looks like on his or her lip. Our program will also select five lipsticks that have colors closest to the color chosen by the user for recommendation. A word cloud in a lip shape will also be displayed once user clicks the lipstick he or she is interested in.

## Group Work Description

### Web Scraping (Fu)
Use requests and bs4 module to get all the links of lipsticks on Sephora product page. Then web scrap on each lipstick link to the the basic information of every lipstick, including product name, brand name, price, number of loves as well as all the rbg values of colors of each lipstick (using BytesIO and PIL) and export a csv file. Build the function to get all the reveiws of each lipstick.

### Recommending Lipsticks with the Closest Color and Analysis(Wang)
Utilize the rgb returned by the web scraping step, clean data, fill the none values and change rgb type from string to tuple. Use squared Euklidian distance to get the distance from different lipstick colors and return 5 closest products to the user.  

*Note: the following analyses are shown in the notebook, but is worthwhile to implement them in the interface in the future*

Text Summary, Sensitive Analysis and Price Analysi: build up a sensitive analysis based on the reviews get from scraping part. Established get_pos_neg_words function from the http://ptrckprry.com to identify the words and get probability of the positive word and negative word inside the reviews. Finally, get frequency of words and return 2 sentence that have most high frequency word as the summary for the reviews. Build a function to return the price of specific product. Then conduct a price analysis based on different product, brand and category of the product to get the average price in different field. 

### Text Mining and Analysis (Zhu)
Build a search link function to take what the user wanted and return a search link for the information. After that, using reviews returned by the web scraping function, the word cloud function firstly conducts some text cleaning and transforming, and then delete some words base on reviews samples and filter words tags to have a better output. Finally, the function plots the word cloud in the lip shape and saves the image to file.

*Note: the following analyses are shown in the notebook, but is worthwhile to implement them in the interface in the future*

Data cleaning, brand emotion analysis: for data cleaning part, NaN values in the results csv and some other unwanted information such as lipstick sets are deleted. The groupby function is applied for choosing the top 5 loved lipsticks as the first recommendation for the user. Brand emotion analysis part gives back the information about emotions that come from customers, and it gives a straight impression of customers’ feeling about the brand.

### Digital Makeup and User Interface (Qian)
An interface is created which has three buttons, one asking the user to upload an image of self, one asking the user to choose a color to apply, the last applying the changes to the image just uploaded by the user. The frames of the interface are straightforward. The top frames contain three buttons described above, the middle frames contain the two “before and after” images, and the bottom frames show the recommended lipsticks and the word cloud (drawn in the shape of a lip) of reviews associated with them. A demonstration will be shown below in the “run instructions” section. The code for applying the new color to the lip is based on the code from https://github.com/ageitgey/face_recognition/blob/master/examples/digital_makeup.py

## Installation Instructions
To install [numpy](http://www.numpy.org/), [pandas](https://pandas.pydata.org/), [requests](http://docs.python-requests.org/en/master/), [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [PIL](https://pillow.readthedocs.io/en/5.3.x/), and [wordcloud](https://github.com/amueller/word_cloud):
```
pip install numpy pandas requests bs4 Pillow wordcloud
```
<br />

To install [scipy](https://www.scipy.org/):
```
python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
```
<br />

To install [nltk](https://www.nltk.org/):
```
pip install nltk
```
then in Python, run:
```
import nltk
nltk.download()
```
In the output console, select all and click download to download all modules in nltk. In case of any problem, in Python, run:
```
nltk.download('averaged_perceptron_tagger')
```
<br />

To install [opencv](https://opencv.org/):
```
pip install opencv-python
```
<br />

To install [face_recognition](https://github.com/ageitgey/face_recognition), which is really troublesome, please refer to https://media.readthedocs.org/pdf/face-recognition/latest/face-recognition.pdf: 1.2 installation part to get the tutorial of installation.

## Run Instructions
1. Make sure that lipstick_web_scraping.py, lipstick_closest_colors.py, lipstick_text_mining.py, lipstick_inferface.py, lipstick.csv and lip.jpg in the same directory.
2. Run lipstick_inferface.py.
3. In the interface, upload an headshot image without any cover on the lip by clicking "Select an image" button (In this instruction, we use the [test_image.jpg](https://www.google.com/search?q=face&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjYxP6bjoLfAhVCn-AKHatkCsUQ_AUIDigB&biw=1504&bih=861#imgrc=hIOwS97FhaduqM:)).
4. After uploading the image, choose the color by clicking “Choose a color” button and then clicking "OK".

![](https://github.com/jianyaofu/lipstick_try_recommend/blob/master/test1.jpg)

5. After a color is chosen, click “Apply” button and the chosen color will be applied to the lip area in the image and display the new image. Meanwhile, 5 lipsticks whose colors are the closest to the chosen color will be selected and their brand name + lipstick color(/number) will be displayed at the bottom left corner. 

![](https://github.com/jianyaofu/lipstick_try_recommend/blob/master/test2.jpg)

6. Among the five recommended lipsticks, the user can click the one he/she is interested. Then the program will search for the reviews associated with the lipstick the user chooses, and draw a word cloud of the reviews and display it at the bottom right corner.

![](https://github.com/jianyaofu/lipstick_try_recommend/blob/master/test3.jpg)

7. User can also click other lipsticks to see the wordcloud of them. User can also choose another color and go through the same process again for the new color without quitting the current interface and restarting a new one. *Note: Getting a wordcloud of reviews may take a while to complete, so if nothing is prompted up after you click some lipstick, it’s because it takes time to get and process the reviews (some lipsticks have long reviews) not because the program is interrupted due to some error.*
