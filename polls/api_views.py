from rest_framework import generics, status
from rest_framework.response import Response
from models import Poll, Vote, Thread, PollSubject
from serializers import PollSerializer, VoteSerializer, ThreadSerializer
from threads.models import Thread

class PollViewSet(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class ThreadViewSet(generics.ListAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class PollInstanceView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class VoteCreateView(generics.ListCreateAPIView):

    serializer_class = VoteSerializer
    queryset = Vote.objects.all()

    def create(self, request, thread_id):
        thread = Thread.objects.get(id=thread_id)
        print "thread",thread.name
        subject = thread.poll.votes.filter(user=request.user).first()
        if subject:
            return Response({"error": "Already voted"},
                            status=status.HTTP_400_BAD_REQUEST)
        print "request.user.id:",request.user.id
        jareqdata = request.data
        post = request.POST.copy()
        #print "request data:", request.data
        print "post:", post
        #request.data['user'] = request.user.id
        post['user'] = request.user.id

        #serializer = VoteSerializer(data=request.data)
        serializer = VoteSerializer(data=post)


        if serializer.is_valid():
            self.perform_create(serializer)
            thread.poll.votes.add(serializer.instance)

            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response({"error": "Fuck Knows"}, status=status.HTTP_400_BAD_REQUEST)