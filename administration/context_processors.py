from api.models import Election

def user_election(request):
    # try:
    #     election = Election.objects.get(admin=request.user)
    # except Election.DoesNotExist:
    election = None
    # print(election.id)
    return {'user_election': election}