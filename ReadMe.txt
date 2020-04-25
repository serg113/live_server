
to create hls stream this repository server codes can be used
			https://github.com/oatpp/example-hls-media-stream

after building and running, enter this link as requires in step 3 below
			http://192.168.99.1:8000/media/live
	
	

example usage
	1. open http://192.168.99.100:8000/frames
	2. it redirects to http://192.168.99.100:8000/login
		login --> admin
		password --> root
	3. after successful login redirects to 
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
	
	
	
	
	
	