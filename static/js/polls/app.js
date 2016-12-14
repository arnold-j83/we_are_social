var pollApp = angular.module('pollApp', []);

pollApp.config(function($interpolateProvider, $httpProvider){
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[names=csrfmiddlewaretoken]').val();
});

pollApp.factory('pollFactory', function($http) {
    var pollUrl = '/threads/polls/';
    var votingUrl = '/threads/polls/vote/';

    pollFactory = {};

    pollFactory.getPoll = function(id) {
        return $http.get(pollUrl + id);
    };

    pollFactory.vote = function(poll, subject) {
        var data = {'poll': poll.id, 'subject': subject.id};

        return $http.post(votingUrl + poll.thread + '/', data); // remember to add the slash for django urls to work!
    };

    return pollFactory;
})

.factory('threadFactory', function($http) {
    var threadURL = '/threads/threads/';

    threadFactory = {};

    threadFactory.getThread = function(){
        return $http.get(threadURL);
    }
    console.log(threadFactory);
    return threadFactory;

});

pollApp.controller('PollCtrl', function($scope, pollFactory) {
    $scope.poll = "";

    function setPoll(response) {
        $scope.poll = response.data;
        console.log("setPoll" + $scope.poll)
    }

    function showError(response) {
        if(response.data.error !== undefined) {
            alert(response.data.error);
        }
    }

    function getPoll() {
        console.log($scope.poll.id);
        console.log(pollFactory.getPoll(1));
        return pollFactory.getPoll(pollID);    // pollID - from our page variable made in our template
    }

    getPoll().then(setPoll);

    $scope.vote = function(poll, subject) {
        pollFactory.vote(poll, subject).then(getPoll).then(setPoll, showError);
    }
})

.controller('threadCtrl', function($scope, threadFactory){

    $scope.threads = "";

    function setThreads(response) {
        $scope.threads = response.data;
        console.log("setThreads" + $scope.threads)
    }

    function getThreads(response){
        console.log(threadFactory.getThread())

        return threadFactory.getThread();
    }

    getThreads().then(setThreads);

});