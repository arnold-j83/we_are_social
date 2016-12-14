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
});
