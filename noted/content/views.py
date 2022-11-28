from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse


from content.forms import NoteForm, SourceForm
from content.models import Note


def home(request):
    notes = Note.objects.all()
    context = {"notes": notes}
    return render(request, "index.html", context)


@login_required
def create_note(request):
    if request.method == "GET":
        form = NoteForm()
        context = {"form": form}
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect(
                reverse("content:note", kwargs={"slug": note.slug})
            )
    return render(request, "content/note_create.html", context)
