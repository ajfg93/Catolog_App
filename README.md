#A online version
- visit `http://52.41.206.23/`


#How to Run

- `python database_setup.py`
- `python lotsofitems` 
- `python app.py`

#Updated v1.0
- fix `signup.html` script `ajax` syntax error
- fix `isLogin` misspelling in `app.py` **showItem** function
- add JSON Enpoint 
 
#Updated v1.1
- bug fix
	- move module level to the top
	- fix edit error. (wrong url with my ajax function)
	- fix delete error. (wrong url and I change the **delete** function name to **deleteItem** in case of potential error)
	- change **app_id** value into string
	- fix FB connect error
		- This is  because I uploaded the project to my VPS and then changed the url the my own IP address. And later I found that for one FB application I can only specify one domain. So I now change it back to `localhost`

#Updated v1.2
- add JSON endpoint that serves an arbitrary item in the catalog
- add identification before users edits item through POST method
- update **back** button

