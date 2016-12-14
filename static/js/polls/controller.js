pollApp.controller('PollCtrl', function($scope, pollFactory) {
    $scope.poll = "";

    function setPoll(response) {
        $scope.poll = response.data;
        console.log($scope.poll)
    }

    function showError(response) {
        if(response.data.error !== undefined) {
            alert(response.data.error);
        }
    }

    function getPoll() {
        console.log($scope.poll.id);
        console.log($pollFactory.getPoll(1));
        return pollFactory.getPoll(pollID);    // pollID - from our page variable made in our template
    }

    getPoll().then(setPoll);

    $scope.vote = function(poll, subject) {
        pollFactory.vote(poll, subject).then(getPoll).then(setPoll, showError);
    }
});
