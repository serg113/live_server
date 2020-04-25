
example usage
	open http://192.168.99.100:8000/frames
	it redirects to http://192.168.99.100:8000/login
	login --> admin
	password --> root
	after successful login redirects to 
					http://192.168.99.100:8000/frames
	enter live stream link in input box and submit
		wait for 10-15 seconds until success will be written under the input box
		



To create docker image 
	clone git repository
	cd to repository folder
	
	$ docker build --tag flserver:1.0 .
	$ docker run --publish 7000:5000 --detach --name flaskserver1.0 flserver:1.0
	
to iterate directories 
	$ docker run -it flserver:1.0 shell
	
	
	http://192.168.99.1:8000/media/live
	
	
	
	