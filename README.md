# ZillowAPI_Python
Scraping www.zillow.com using their APIs and requests,Pandas libraries for support in Python


Transcript
Hope you are doing. There are one 4 main functions which we will be using in this code.
I'll let you know about each of them one by one. And we will discuss about everything else.

THE API URL :

How we are getting this API URL ? OK, let's start from the low.
And how do you take this URL? This is actually the API URL of Zillow. When you select a category or filter, go to the pagination at the bottom and click page number 2 or any Page. Make sure to open the Chrome dev console --> Network tab and in this tab click on Fetch/XHR. When you click on page 2 you will get URL like this.

https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-74.02469663281249%2C%22east%22%3A-73.17874936718749%2C%22south%22%3A40.617190229727065%2C%22north%22%3A40.89286338066993%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A1252%2C%22regionType%22%3A4%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D&wants={%22cat1%22:[%22listResults%22,%22mapResults%22],%22cat2%22:[%22total%22]}&requestId=4
Here is the image as well
 


This this is the URL we need and we also need the headers associated with this URL so. In order to get all the stuff attached to this world we we are going to copy the URL as fetch so just right click on it, go to copy and go for copy as fetch and come to console and just paste it.

THE FIRST FUNCTION TO GET THE COUNT:

Moving on to code, You need to copy that url in the array 'cat_urls' and I am attaching the image for the 1st function as well.

 
 

You can see that in the headers variable, I've copied those headers which get using Copy as Fetch while copying the urls. Just added the user agent
In response variable, the request to the URL 'link' which is the API link and its coming from the 2nd image. You can easily see I've applied loop over the array containing API url. In YDJ Response it will get JSON and I will be getting the total count of listings.That count will be saved in an array 'purls' which will later be used in Pagination.
THE 2ND FUNCTION TO GET THE ZILLOW IDS AND LOT IDS:
So move on to our next function. We got the category count and after that we move on to list page. What is the list page actually? The list page contains all the entries list and basic Information. There are two type of listings in Rentals category 
1 - The buildings with multiple portions / Apartments
2 - Houses for rent
The main thing we need to get the data is Zillow IDs. But in Buildings/Apartments case there are no proper zillow IDs but we have 'lot IDs' . So we have to create another function to get zillow IDs from lot IDs.
 
Here is a visual of Apartments/Building listings
 
Here is the house listing example
Here is the Function Code.
 
 
The above 1st image is showing the Function body and conditions to get Zillow and LOT IDs.
The 2nd image is showing the loop in which Function is called. It will get the total count of category from 'purls' array and then divide it by 40 ( Which is the maximum number of listings on a list page). It will get the number of list pages and then it will move to the next loop for generating pagination URLs. It will do so by applying regexes and concatening the loop counter. Meanwhile it will send the request.
In the result we will be getting Zillow IDs in 'alldata' array and Lot IDs in 'buildingkey' array.
Category count must be less than 1000 because zillow does not offer pagination beyond 1000 listings or 20 pages. To achieve the full count you need to apply filters on the website.
THE 3RD FUNCTION TO GET THE ZILLOW IDS FROM LOT IDS:
Now lets move on to 3rd function which is to Zillow IDs from lot IDs. First let me show you How to get the request for Lot IDs from Dev console.
 
In the attached image you can see that When I clicked a building listing. I got these request you have to find a POST request with URL
https://www.zillow.com/graphql/ and the request body must be like

  "body": "{"operationName":"BuildingQuery","variables":{"lotId":"2089054182","cache":false,"update":false},"queryId":"650473038587ed5269d22776ec1dcd01"}"
You can see that there is Lot ID in the request. So now move on to function
 
 
In the function, It will create a session for POST request and we have to provide headers and body. In body we have to provide the lot ID as a variable. So we will get the zillow IDs in response and we save all the zillow IDs in the 'alldata' array.
In the 2nd image you can see that its applying loop over array 'buildingkey'  because we have lot IDs in that array. these IDs will pass in the functions and will be use in the function's  request body.

THE 4TH FUNCTION TO GET THE DATA FROM LISTINGS:
Now we have all the required Zillow IDs in the 'alldata' array. So It will move to the 4th function to get the main data of listings or you can call it product page.
Here's how to get product page request
 
When you click on a house listing (Remember a house listing not a building one). You will get this request . A POST request with URL.
https://www.zillow.com/graphql/?zpid=2066497724&contactFormRenderParameter=&queryId=1a33d0a65c70c4fc7083477ee441b7bb&operationName=ForRentDoubleScrollFullRenderQuery
With the request body like
 "body":"{"operationName":"ForRentDoubleScrollFullRenderQuery","variables":{"zpid":2066497724,"contactFormRenderParameter":{"zpid":2066497724,"platform":"desktop","isDoubleScroll":true}},"clientVersion":"home-details/6.0.11.7155.master.4c57976","queryId":"1a33d0a65c70c4fc7083477ee441b7bb"}"
You will copy it as fetch and then move on to function body
 
 

 
In the first image, You can see the session and the request headers and request body in the data variable. In the 2nd one you can see the request URL and response variable and other Attributes we are getting in the response from the request.
In the 3rd image you can see the loop where the function has been called. I applied the loop over 'alldata' array in which we have all the Zillow IDs. it will send those IDs in the request URLs and body and allow us to get the data. the data then get stored in an Array name 'proddata'
 
This will lead to the final part of Pandas.
PUTTING DATA FROM ARRAY TO PANDAS DATAFRAME:
Now all the data has been stored in the array 'proddata'. But we want it in the excel/csv file for our use. For this I used Pandas.



You can see in the Image that I created a dataframe 'df' using pandas 'pd' and add the array into that dataframe and name the columns against the array variables. These will be the headers. Make sure to name the columns in accordance with array attributes.
In the 2nd line, It will create a variable for current date using datetime library of python which will later be use in Filename for avoiding duplication on day to day scraping.
In the 3rd line I remove all the duplicate entries from data frame using 'drop_duplicates' command.
Moving ahead It will use the 'OS' library and check if the file with the name is in the folder or not.
If not it will create a new file . If its already present then it will append to the file. The df.to_csv function's argument "mode='a' " will append the data into the file


