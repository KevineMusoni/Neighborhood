from django.shortcuts import render

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})