#How to Run

- `python database_setup.py`
- `python lotsofitems` 
- `python app.py`


I try to make a single-page applicationi but somehow it gets sort of complicated. Please take some time to read my code.

#Updated v1.0
- fix `signup.html` script `ajax` syntax error
- fix `isLogin` misspelling in `app.py` **showItem** function
- add JsonEndpoint 
 
#Updated v1.1
Hey! I don't know if you've read my notes (that in the Udacity Page) along with last submission. I noticed that you would read my MD. So I would write down here too.

- bug fix
	- move module level to the top
	- fix edit error. (wrong url with my ajax function)
	- fix delete error. (wrong url and I change the **delete** function name to **deleteItem** in case of potential error)
	- change **app_id** value into string
	- fix FB connect error
		- This is  because I uploaded the project to my VPS and then changed the url the my own IP address. And later I found that for one FB application I can only specify one domain. So I now change it back to `localhost`
- sth about JSON
	- dear reviewer, actually, I desgin the JSON endpoint according to this [img](http://i.imgur.com/oMQaCs8.png) posted in the course. Check the image you may undertand why I set a emtpy **Item** property in the **Category** serialize propery and how I implement the endpoint function. I feel confused about the URL at the very beginning too :D.

- sth else
	- thank you for recommending the sublime linter and decorator instruction. ( I would try another time =.=)
	- btw, would you like to hire me or introduce a job to me lol :D. 