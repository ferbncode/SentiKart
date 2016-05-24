# SentiKart
SentiKart is a system that analyses large amount of reviews of a product on e-commerce sites gathers sentiment pertaining to 
the product and represents the trends in an intelligible and attractive form.

SentiKart first creates a database of the reviews of the product by scraping the e-commerce site with the aid of python 
and the module 'Beautiful Soup'. Each review is then passed through an indigenous sentimental analysis model which calculates
the overall sentiment in the reviews. For certain products, sentiments of some other attributes are also calculated.
For example, a mobile phone may have attributes such as camera, performance, looks, service, etc.
Now to extract valuable info, the data is plotted with respect to time using 'Highcharts.com' to represent the changing  trends.
It also calculates the overall sentiment and represents it using pie charts.

Check it out on https://sentikart.herokuapp.com.
