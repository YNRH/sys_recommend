var express = require('express'),
    async = require('async'),
    { Pool } = require('pg'),
    cookieParser = require('cookie-parser'),
    bodyParser = require('body-parser'),
    path = require('path'),
    app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server),
    Redis = require("ioredis");

var port = process.env.PORT || 4000;

io.on('connection', function (socket) {
  socket.emit('message', { text : 'Welcome!' });
});

// Handle connection errors
var redis = new Redis({
  host: 'redis', 
  port: 6379
});


var pool = new Pool({
  connectionString: 'postgres://postgres:postgres@db/DBmovies'
});

async.retry(
  {times: 1000, interval: 1000},
  function(callback) {
    pool.connect(function(err, client, done) {
      if (err) {
        console.error("Waiting for db");
      }
      callback(err, client);
    });
  },
  function(err, client) {
    if (err) {
      return console.error("Giving up");
    }
    console.log("Connected to db");
  }
);

app.use(cookieParser());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(__dirname + '/views'));

app.get('/', function (req, res) {
  res.sendFile(path.resolve(__dirname + '/views/index.html'));
});

app.get('/random-movie', async function (req, res) {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT title FROM movies ORDER BY RANDOM() LIMIT 1');
    client.release();
    if (result.rows.length > 0) {
      res.json(result.rows[0]);  
    } else {
      res.status(404).json({ error: 'No movies found' });
    }
  } catch (err) {
    console.error(err);
    res.sendStatus(500);
  }
});

// Nueva ruta para manejar los votos
app.post('/submit-votes', async function (req, res) {
  var cookie_id = req.cookies.cookie_id;
  if (!cookie_id) {
    cookie_id = require('crypto').randomBytes(8).toString('hex');
    res.cookie('cookie_id', cookie_id, { maxAge: 900000, httpOnly: true });
  }

  var votes = req.body.votes;

  if (!votes || typeof votes !== 'object') {
    return res.status(400).send('Invalid votes data');
  }

  try {
    for (const [title, rating] of Object.entries(votes)) {
      const watched_duration = Math.floor(Math.random() * 17);
      const data = JSON.stringify({ title, rating, watched_duration });
      await redis.hset(`user_ratings:${cookie_id}`, title, data);
    }
    res.status(200).send('Votes submitted successfully');
  } catch (err) {
    console.error('Error saving votes:', err);
    res.status(500).send('Error saving votes');
  }
});


server.listen(port, function () {
  var port = server.address().port;
  console.log('App running on port ' + port);
});
