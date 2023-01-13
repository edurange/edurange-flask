EDURange Chat Guide

This is a reference guide for EDURange developers on the EDURange Database.

#### Set Up

Check that your .env file has the CHAT_PORT variable defined. Port 3001 works well. 
Ensure that traffic is allowed on the port in your firewall rules. (ingress and egress?) 
Insert this rule in your ssh-configuration file within the block of other options for the host you’re SSHing into:
LocalForward 127.0.0.1:3001 127.0.0.1:3001

#### chat_server.js

The chat_server.js class utilizes the socket.io library to establish a node server. This gives clients the ability to connect to the server and emit messages. The server directs these to the intended client recipient.

	Constructor
		The first 30 lines establish the server and its required features.  
		See Docs: Server Constructor

	Initialization
		The server is initalized with the following line:
            const server = http.createServer(app);

        The information below is intended to provide a somewhat in-depth review of the techonologies the server is built on. 

#### What is Node.js?

Node.js is a JavaScript runtime environment. It is built on Chrome's V8 JavaScript engine. This means the same engine is used in-browser and server-side, an essential feature which allows code to easily translate between the backend and frontend. 
Node.js includes its own package manager, npm, and a series of web frameworks available to use like express (which we'll discuss more below.) 
Node.js files, like chat_server.js, can be run with the command: 
	$ node <filename>
This can be useful for debugging. 


#### What is an HTTP Server?

An HTTP (Hyper Text Transfer Protocol) servers are an essential tool for communcating with the browser to handle (provide, parse, store) web content.
HTTP is a piece of software that listens on dev-specified ports for incoming HTTP requests and returns responses to clients. An HTTP server is configured to understand URLS and HTTP, which is, of course, the protocol used by your browser. 
HTTP servers are used to host web applications and APIs, and are an essential part of the modern web.
In the context of Node.js, the HTTP server is created using the built-in http module.

#### What is the express framework?

Express is a web application framework for Node.js, designed for building web applications and APIs. It is the de facto standard server framework for Node.js, and is very popular because of its simplicity and flexibility.
Express is built on top of the Node.js HTTP module, and adds support for routing, middleware, and more. It is easy to set up and use, and has a large and active developer community that has contributed a wide range of plugins called middleware to do everything from adding CORS support to handling file uploads.

If you are building a web application or API with Node.js, chances are you will use Express. It is a great choice for getting up and running quickly, and has the tools you need to build a wide range of web applications and APIs.

#### What is middleware?

In the context of web development, middleware refers to software that sits between the application and the server handling requests and responses. 
Middleware functions have access to the request and response objects, and can perform a variety of tasks before the request is forwarded to the application for handling.

Express middleware are functions that are invoked by the Express server before the request is handed off to the route handling function..
What is Connect/Express?

Connect is a middleware framework for Node.js that was developed before Express. It is similar to Express in that it provides a way to define middleware functions that can be used to perform tasks such as parsing the request body, handling authentication, adding CORS support (see below), or modifying the response in some way.

Express is built on top of Connect, and provides many of the same features as Connect, as well as additional features such as routing and support for view engines. If you are using Express, you are effectively using Connect as well, as Express builds on top of Connect and uses it to provide many of its core features.


#### What is CORS?

CORS is a node.js package providing a Connect/Express middleware that is used to enable CORS with various options. For more information on Connect/Express middleware, see above notes.

CORS stands for Cross-Origin Resource Sharing. It is a security feature implemented by web browsers that blocks web pages from making requests to a different domain than the one that served the web page.

For example, if a web page served from https://internet.com makes a request to https://api.internet.com, the browser will block the request by default because the domains are different. This is done to prevent malicious web pages from making unauthorized requests on behalf of the user.
How does CORS work? CORS can be used to allow web pages to make requests to a different domain by adding appropriate headers to the server response. When the browser receives the response, it checks the headers to see if the server has granted permission to make the request. If permission is granted, the browser allows the request to be made.

================================================ Code ======================================================>

#### Dictionaries (masterListChats and masterLiveStuds)

The array variables, masterListChats and masterLiveStuds, hold all of the chat correspondences and the list of active students, respectively. 

#### Middleware

	io.use () …
	The above code registers middleware for the io (traffic-directing node server) object. This is utilized every time a socket joins or rejoins. 
	The uid is passed within the initial TCP handshake. Error handling is found in the client connection event hook, see below. 

#### Client Connection Event
	io.on(“connection”,...
	The above code is called whenever a socket connects or reconnects.
	See Docs: Event “Connection”
	Message Persistence
	If masterListChats contains an entry for the uid, this will be sent to the socket so that the correspondence will appear for the user.

#### Joining Rooms
Initially, each student joins their own room (indicated by their user id). 
Each instructor joins their own room, and each of the rooms of their students.
See Docs: Sockets Joining Rooms

#### Sending Alerts (trafficAlert function) 
Alerts are formed and sent primarily for their use in the Student_List.Component, in the Instructor View folder. They’re passed to the instructor (received in the Instructor_View component). 
Each alert indicates who has joined, left, and sent a message, so these traits can be indicated visually for the instructor. 

#### socket.on(“send message”...
When a socket emits a “send message” event, this is received by the io server object with the data and the intended recipient. 
The server stores the message in the masterListChats dictionary. 
The server creates an alert for the instructor, if the message is from a student. 
The server emits a “new message” event to the intended recipient, who is listening from either the client_socket or instructor_view component. 
socket.on(“disconnected”...
If the socket that is left is the instructor, “instructor left” is emitted for student sockets. 
Otherwise, the instructor is notified of the student leaving via a traffic alert, and the live property is changed from true to false in the masterStudLive dictionary. 

