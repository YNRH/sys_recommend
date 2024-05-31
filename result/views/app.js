var app = angular.module("moviesApp", ['ngSanitize']);
var socket = io.connect();

app.controller("moviesController", function ($scope, $http, $sce) {
  let player;
  let startTime = 0;
  let watchedDuration = 0;

  function init() {
    document.body.style.opacity = 1;
  }

  socket.on("message", function (data) {
    init();
  });

  function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
  }

  function setCookie(name, value, days) {
    var expires = "";
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
  }

  function generateTempCookieId() {
    return 'temp' + Math.random().toString(36).substr(2, 9);
  }

  $scope.cookie_id = getCookie("cookie_id");

  if (!$scope.cookie_id) {
    $scope.cookie_id = generateTempCookieId();
    setCookie("cookie_id", $scope.cookie_id, 1);
  }

  $scope.votes = {};
  $scope.recomendaciones = [];

  async function fetchRecommendations() {
    if ($scope.cookie_id) {
      try {
        const response = await $http.get(`http://localhost:5002/recommend/${$scope.cookie_id}`);
        $scope.recomendaciones = [response.data];
        $scope.recomendaciones.forEach(movie => {
          movie.video_url = $sce.trustAsResourceUrl(movie.video_url.replace("youtu.be", "www.youtube.com/embed"));
        });
        onYouTubeIframeAPIReady();
        console.log("Recomendación actualizada");
      } catch (error) {
        console.error('Error fetching recommendations: ', error);
      } finally {
        $scope.$apply();
      }
    }
  }

  

  $scope.rateMovie = async function (title, rating) {
    $scope.votes[title] = { rating: rating, watched_duration: watchedDuration };
    console.log(`Rating submitted: ${title} - ${rating}, Watched Duration: ${watchedDuration} seconds`);

    try {
      await $http.post('/submit-votes', { votes: $scope.votes });
      console.log('Votes submitted successfully');
      $scope.votes = {};
      watchedDuration = 0;
      fetchRecommendations();
    } catch (error) {
      console.error('Error submitting votes:', error);
    }
  };

  fetchRecommendations();
  window.onYouTubeIframeAPIReady = function() {
    player = new YT.Player('player', {
      events: {
        'onStateChange': onPlayerStateChange
      }
    });
  }

  function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
      if (!startTime) {
        startTime = Date.now();
      }
      console.log('Video started playing');
    } else if (event.data == YT.PlayerState.PAUSED || event.data == YT.PlayerState.ENDED) {
      if (startTime) {
        watchedDuration += Math.floor((Date.now() - startTime) / 1000);
        console.log(`Video paused or ended. Watched Duration: ${watchedDuration} seconds`);
        startTime = 0;
      }
    }
  }
  // Manejar la interrupción por actualización de página
  window.addEventListener('beforeunload', function() {
    if (startTime) {
      watchedDuration += Math.floor((Date.now() - startTime) / 1000);
      console.log(`Page is unloading. Watched Duration: ${watchedDuration} seconds`);
      startTime = 0;
    }
  });
});

app.config(['$sceDelegateProvider', function($sceDelegateProvider) {
  $sceDelegateProvider.resourceUrlWhitelist([
    'self',
    'https://www.youtube.com/**'
  ]);
}]);
