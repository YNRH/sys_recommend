var app = angular.module("moviesApp", []);
var socket = io.connect();

app.controller("moviesController", function ($scope, $http) {
  // Define API_URL
  //$scope.API_URL = ;

  var init = function () {
    document.body.style.opacity = 1;
  };
  socket.on("message", function (data) {
    init();
  });

  // Función para obtener la cookie "cookie_id" del navegador
  function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
  }

  // Obtener el cookie_id
  $scope.cookie_id = getCookie("cookie_id");

  // Obtener las películas aleatorias
  $http
    .get("/random-movie")
    .then(function (response) {
      $scope.randomMovie = response.data;
    })
    .catch(function (error) {
      console.log("Error al obtener película aleatoria:", error);
    });

  // Obtener las recomendaciones para el usuario
  if ($scope.cookie_id) {
    $http
      .get("http://localhost:5002/recommend/" + $scope.cookie_id)
      .then(function (response) {
        console.log("Datos de respuesta de la API:", response.data);
        $scope.recomendaciones = response.data;
        $scope.total_recomendadas = response.data.length;
      })
      .catch(function (error) {
        console.log("Error al obtener recomendaciones:", error);
      });
  }

  $scope.votes = {};

  $scope.rateMovie = function (title, rating) {
    $scope.votes[title] = rating;
  };

  $scope.submitVotes = function () {
    if (Object.keys($scope.votes).length === 0) {
      console.error('No votes to submit');
      return;
    }
    
    $http.post('/submit-votes', { votes: $scope.votes })
      .then(function (response) {
        console.log('Votes submitted successfully');
      })
      .catch(function (error) {
        console.error('Error submitting votes:', error);
      });
  };
});
