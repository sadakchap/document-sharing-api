from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives

from .models import Doc
from .forms import EmailPostForm

# Create your views here.

@login_required
def add_doc(request):
    file_formset = modelformset_factory(Doc, fields=('f',), extra=4)
    if request.method == 'POST':  
        formset = file_formset(request.POST or None, request.FILES or None)
        if formset.is_valid():
            for form in formset:
                print(form)
                try:
                    doc = Doc(user=request.user, f=form.cleaned_data['f'])
                    doc.save()
                    print('saving')
                except Exception as e:
                    print('exceplt block')
                    pass
            return redirect('/')
            # formset.save()
    else:
        formset = file_formset(queryset=Doc.objects.none())
    return render(request, 'docs/add_file.html', {'formset': formset})


@login_required
def my_docs_list(request):
    docs = Doc.objects.filter(user=request.user) 
    return render(request, 'docs/docs_list.html', {'docs': docs})

@login_required
def delete_doc(request, pk):
    doc = get_object_or_404(Doc, pk=pk)
    if request.user == doc.user:
        doc.delete()
        return redirect('docs:list')
    return HttpResponseForbidden('You are not Authorizaed!') 
    # return render(request, 'docs/remove_delete.html', {})

@login_required
def share_doc(request, pk):
    form = EmailPostForm(request.POST or None)
    doc = get_object_or_404(Doc, pk=pk)
    if form.is_valid():
        
        current_site = get_current_site(request)
        if request.user == doc.user:
            name = form.cleaned_data.get('name')
            sub = f'{name} shared a document with you'
            html_content = render_to_string('doc_share_email.html',{
                'doc': doc,
                'domain': current_site.domain
            })
            comment = form.cleaned_data.get('comment')
            from_email = form.cleaned_data.get('email')
            to_email = form.cleaned_data.get('to')
            msg = f'{name} shared a document with you.\n\n {name} comments are {comment}.\n\n You can back at {from_email}'
            msg = EmailMultiAlternatives(sub, msg, settings.EMAIL_HOST_USER, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect('/')

    return render(request, 'docs/share.html', {'form': form})