const io = require('socket.io')(server, {
  cors: {
      origin: "http://localhost:3001",
      methods: ["GET", "POST"],
      transports: ['websocket', 'polling'],
      credentials: true
  },
  allowEIO3: true
});

io.engine.on("connection_error", (err) => {
  console.log(err);
});

socket.on("connect_error", (err) => {
  console.log(`connect_error due to ${err.message}`);
});

io.on('connection', socket => {
  console.log(`connect: ${socket.id}`);

  socket.on('hello!', () => {
    console.log(`hello from ${socket.id}`);
  });

  socket.on('disconnect', () => {
    console.log(`disconnect: ${socket.id}`);
  });
});



io.listen(3001);

setInterval(() => {
  io.emit('message', new Date().toISOString());
}, 1000);
