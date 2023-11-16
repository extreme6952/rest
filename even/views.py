from django.shortcuts import render,get_object_or_404

from django.views.generic import ListView

from django.core.mail import send_mail

from django.views.decorators.http import require_POST

from .models import Event,Comment

from .forms import EmailForm,CommentForm


class IndexList(ListView):

    queryset = Event.published.all()

    template_name = 'event/ev/index.html'

    context_object_name = 'events'

    paginate_by = 3







def event(request,year,month,day,event):

    event = get_object_or_404(Event,
                                status = Event.Status.PUBLISHED,
                                publish__year = year,
                                publish__month = month,
                                publish__day = day,
                                slug = event)
    

    comments = event.comments.filter(active=True)

    form_comment = CommentForm()

    return render(request,'event/ev/detail.html',{'details':event,
                                                  'form_comment':form_comment,
                                                  'comments':comments})





def event_share(request,post_id):

    share_event = get_object_or_404(Event,
                                    status = Event.Status.PUBLISHED,
                                    id=post_id)
    
    sent = False
    

    if request.method == 'POST':

        form_share = EmailForm(request.POST)

        if form_share.is_valid():

            cd = form_share.cleaned_data

            event_url = request.build_absolute_uri(share_event.get_absolute_url())

            subject = f"{cd['name']} reccomends you read {share_event.title}"

            message = f"Read {share_event.title} at {event_url}\n\n"
            f"{cd['comments']} to :{cd['name']}"

            send_mail(subject,message,'kaznacheev724@gmail.com',
                      [cd['to']])
            
            sent = True



    return render(request,{'share_event':share_event,
                           'form_share':form_share,
                           'sent':sent})





@require_POST
def post_comment(request,post_id):

    post = get_object_or_404(Event,
                             status=Event.Status.PUBLISHED,
                             id=post_id)
    

    comment = None

    form_comment = CommentForm(data=request.POST)

    if form_comment.is_valid():

        comment = form_comment.save(commit=False)

        comment.post = post

        comment.save()

    return render(request,'event/ev/comment.html',{
        'comment':comment,
        'form_comment':form_comment,
        'post':post
    })




