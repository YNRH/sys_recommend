const express = require('express');
const { Pool } = require('pg');
const cookieParser = require('cookie-parser');
const path = require('path');
const http = require('http');
const socketIO = require('socket.io');
const Redis = require('ioredis');
const axios = require('axios');  

const app = express();
const server = http.createServer(app);
const io = socketIO(server);
const redis = new Redis({ host: 'redis', port: 6379 });
const pool = new Pool({ connectionString: 'postgres://postgres:postgres@db/DBmovies' });

const port = process.env.PORT || 4000;

io.on('connection', (socket) => {
  socket.emit('message', { text: 'Welcome!' });
});

app.use(cookieParser());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

app.get('/', (req, res) => {
  res.sendFile(path.resolve(__dirname, 'views/index.html'));
});

app.post('/submit-votes', async (req, res) => {
  let cookie_id = req.cookies.cookie_id;
  if (!cookie_id) {
    cookie_id = require('crypto').randomBytes(8).toString('hex');
    res.cookie('cookie_id', cookie_id, { maxAge: 900000, httpOnly: true });
  }

  const votes = req.body.votes;

  if (!votes || typeof votes !== 'object') {
    return res.status(400).send('Invalid votes data');
  }

  try {
    for (const [title, voteData] of Object.entries(votes)) {
      const { rating, watched_duration } = voteData;
      const data = JSON.stringify({ title, rating, watched_duration });
      await redis.hset(`user_ratings:${cookie_id}`, title, data);
    }
    res.status(200).send('Votes submitted successfully');
  } catch (err) {
    console.error('Error saving votes:', err);
    res.status(500).send('Error saving votes');
  }
});

server.listen(port, () => {
  console.log(`App running on port ${port}`);
});
