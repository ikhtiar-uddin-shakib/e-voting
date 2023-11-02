from django.shortcuts import render, redirect, reverse
from account.views import account_login
from api.models import *
from django.http import JsonResponse
from django.utils.text import slugify
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from datetime import timedelta
import cloudinary



def generate_ballot(election, display_controls=False):
    # voters = Voter.objects.get(user=user)
    positions = Position.objects.filter(election=election).order_by('priority')
    output = ""
    candidates_data = ""
    num = 1
    instruction=" "
    # return None
    for position in positions:
        name = position.name
        position_name = slugify(name)
        candidates = Candidate.objects.filter(position=position)
        for candidate in candidates:
            if position.max_vote > 1:
                instruction = "You may select up to " + \
                    str(position.max_vote) + " candidates"
                input_box = '<input type="checkbox" value="'+str(candidate.id)+'" class="flat-red ' + \
                    position_name+'" name="' + \
                    position_name+"[]" + '">'
            else:
                instruction = "Select only one candidate"
                input_box = '<input value="'+str(candidate.id)+'" type="radio" class="flat-red ' + \
                    position_name+'" name="'+position_name+'">'
            image ='https://res.cloudinary.com/azurahat/image/upload/v1698829755/' + str(candidate.photo)
            candidates_data = candidates_data + '<li>' + input_box + '<button type="button" class="btn btn-primary btn-sm btn-flat clist platform" data-fullname="'+candidate.fullname+'" data-bio="'+candidate.bio+'"><i class="fas fa-receipt fa-lg"></i> Details</button><img src="' + \
                image+'" height="100px" width="100px" class="clist"><span class="cname clist">' + \
                candidate.fullname+'</span></li>'
        up = ''
        if position.priority == 1:
            up = 'disabled'
        down = ''
        if position.priority == positions.count():
            down = 'disabled'
        output = output + f"""<div class="row">	<div class="col-xs-12"><div class="box box-solid" id="{position.id}">
             <div class="box-header with-border">
            <h3 class="box-title"><b>{name}</b></h3>"""

        if display_controls:
            output = output + f""" <div class="pull-right box-tools">
        <button type="button" class="btn btn-default btn-sm moveup" data-id="{position.id}" {up}><i class="fa fa-arrow-up"></i> </button>
        <button type="button" class="btn btn-default btn-sm movedown" data-id="{position.id}" {down}><i class="fa fa-arrow-down"></i></button>
        </div>"""

        output = output + f"""</div>
        <div class="box-body">
        <p>{instruction}
        <span class="pull-right">
        <button type="button" class="btn btn-success btn-sm btn-flat reset" data-desc="{position_name}"><i class="fas fa-redo"></i> Reset</button>
        </span>
        </p>
        <div id="candidate_list">
        <ul>
        {candidates_data}
        </ul>
        </div>
        </div>
        </div>
        </div>
        </div>
        """
        position.priority = num
        position.save()
        num = num + 1
        candidates_data = ''
    return output


# def fetch_ballot(request):
#     election= request.user.voter.election
#     output = generate_ballot(election,display_controls=True)
#     return JsonResponse(output, safe=False)

def fetch_ballot(request):
    user = request.user
    if user.is_authenticated:
        election = user.voter.election
        output = generate_ballot(election, display_controls=True)
        return JsonResponse(output, safe=False)
    else:
        return JsonResponse({"message": "There is no election currently ongoing."}, safe=False)



def userProfile(request):
    user = request.user

    if user.is_authenticated:
        elections = Election.objects.filter(is_open = 1)
        election = request.user.voter.election
        if election:
            if user.voter.voted:  # * User has voted
                    context = {
                        'my_votes': Vote.objects.filter(voter=user.voter),
                        'election' : election
                    }
                    return render(request, "voting/result.html", context)
            else:
                    return redirect(reverse('show_ballot'))
        else:
            if request.method == 'POST':
                selected_election_id = request.POST.get('selectedElection')
                election = Election.objects.get(id=selected_election_id)
                voter = request.user.voter

                # Update the voter's election field
                voter.election = election
                voter.save()
                messages.success(request, "Election selection successful")
                return redirect(reverse('show_ballot'))
        context2 = {
                'elections' : elections
            }
        
        return render(request, "voting/voters_election.html", context2)
    
    return redirect('login')
    


def show_ballot(request):
    user = request.user
    if user.voter.voted:
        messages.error(request, "You have voted already")
        return redirect(reverse('userProfile'))

    election = user.voter.election
    current_time = timezone.now() + timedelta(hours=6)
    election_end_time = election.end_date
    current_time = current_time.astimezone(election_end_time.tzinfo)
    time_remaining = (election_end_time - current_time).total_seconds()

    # Check if the election is open
    if election and current_time <= election_end_time:
        ballot = generate_ballot(election, display_controls=False)

        context = {
            'ballot': ballot,
            'election': election,
            'time_remaining': time_remaining,
        }

        return render(request, "voting/ballot.html", context)
    else:
        context = {
            'election_ended': True 
        }
        return render(request, "voting/ballot.html", context)



def preview_vote(request):
    election= request.user.voter.election
    if request.method != 'POST':
        error = True
        response = "Please browse the system properly"
    else:
        output = ""
        form = dict(request.POST)
        # We don't need to loop over CSRF token
        form.pop('csrfmiddlewaretoken', None)
        error = False
        data = []
        positions = Position.objects.filter(election=election).order_by('priority')
        for position in positions:
            max_vote = position.max_vote
            pos = slugify(position.name)
            pos_id = position.id
            if position.max_vote > 1:
                this_key = pos + "[]"
                form_position = form.get(this_key)
                if form_position is None:
                    continue
                if len(form_position) > max_vote:
                    error = True
                    response = "You can only choose " + \
                        str(max_vote) + " candidates for " + position.name
                else:
                    # for key, value in form.items():
                    start_tag = f"""
                       <div class='row votelist' style='padding-bottom: 2px'>
		                      	<span class='col-sm-4'><span class='pull-right'><b>{position.name} :</b></span></span>
		                      	<span class='col-sm-8'>
                                <ul style='list-style-type:none; margin-left:-40px'>
                                
                    
                    """
                    end_tag = "</ul></span></div><hr/>"
                    data = ""
                    for form_candidate_id in form_position:
                        try:
                            candidate = Candidate.objects.get(
                                id=form_candidate_id, position=position)
                            data += f"""
		                      	<span class='col-sm-8'><li><i class="fa fa-check-square-o"></i> {candidate.fullname}  </li></span>
                            """
                        except:
                            error = True
                            response = "Please, browse the system properly"
                    output += start_tag + data + end_tag
            else:
                this_key = pos
                form_position = form.get(this_key)
                if form_position is None:
                    continue
                # Max Vote == 1
                try:
                    form_position = form_position[0]
                    candidate = Candidate.objects.get(
                        position=position, id=form_position)
                    output += f"""
                            <div class='row votelist' style='padding-bottom: 2px'>
		                      	<span class='col-sm-4'><span class='pull-right'><b>{position.name} :</b></span></span>
		                      	<span class='col-sm-4'><i class="fa fa-check-circle-o"></i> {candidate.fullname}</span>
		                    </div>
                      <hr/>
                    """
                except Exception as e:
                    error = True
                    response = "Please, browse the system properly"
    context = {
        'error': error,
        'list': output
    }
    return JsonResponse(context, safe=False)


def submit_ballot(request):
    if request.method != 'POST':
        messages.error(request, "Please, browse the system properly")
        return redirect(reverse('show_ballot'))

    # Verify if the voter has voted or not
    voter = request.user.voter
    if voter.voted:
        messages.error(request, "You have voted already")
        return redirect(reverse('voterDashboard'))

    form = dict(request.POST)
    form.pop('csrfmiddlewaretoken', None)  # Pop CSRF Token
    form.pop('submit_vote', None)  # Pop Submit Button

    # Ensure at least one vote is selected
    if len(form.keys()) < 1:
        messages.error(request, "Please select at least one candidate")
        return redirect(reverse('show_ballot'))
    election= request.user.voter.election
    positions = Position.objects.filter(election=election).order_by('priority')
    form_count = 0
    for position in positions:
        max_vote = position.max_vote
        pos = slugify(position.name)
        pos_id = position.id
        if position.max_vote > 1:
            this_key = pos + "[]"
            form_position = form.get(this_key)
            if form_position is None:
                continue
            if len(form_position) > max_vote:
                messages.error(request, "You can only choose " +
                               str(max_vote) + " candidates for " + position.name)
                return redirect(reverse('show_ballot'))
            else:
                for form_candidate_id in form_position:
                    form_count += 1
                    try:
                        candidate = Candidate.objects.get(
                            id=form_candidate_id, position=position)
                        vote = Vote()
                        vote.candidate = candidate
                        vote.voter = voter
                        vote.position = position
                        vote.election = election
                        vote.save()
                    except Exception as e:
                        messages.error(
                            request, "Please, browse the system properly " + str(e))
                        return redirect(reverse('show_ballot'))
        else:
            this_key = pos
            form_position = form.get(this_key)
            if form_position is None:
                continue
            # Max Vote == 1
            form_count += 1
            try:
                form_position = form_position[0]
                candidate = Candidate.objects.get(
                    position=position, id=form_position)
                vote = Vote()
                vote.candidate = candidate
                vote.voter = voter
                vote.position = position
                vote.election = election
                vote.save()
            except Exception as e:
                messages.error(
                    request, "Please, browse the system properly " + str(e))
                return redirect(reverse('show_ballot'))
    # Count total number of records inserted
    # Check it viz-a-viz form_count
    inserted_votes = Vote.objects.filter(voter=voter)
    if (inserted_votes.count() != form_count):
        # Delete
        inserted_votes.delete()
        messages.error(request, "Please try voting again!")
        return redirect(reverse('show_ballot'))
    else:
        # Update Voter profile to voted
        voter.voted = True
        voter.save()
        messages.success(request, "Thanks for voting")
        return redirect(reverse('userDashboard'))