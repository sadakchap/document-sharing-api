from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.template.loader import render_to_string

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
        if request.user == doc.user:
            sub = f'{request.user.email} shared a document with you'
            msg = render_to_string('doc_share_email.html',{
                'doc': doc
            })
            send_mail(sub, msg, settings.EMAIL_HOST_USER, [form.cleaned_data.get('to')])
            return redirect('/')

    return render(request, 'docs/share.html', {'form': form})