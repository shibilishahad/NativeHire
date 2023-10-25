from django.shortcuts import render
from .forms import EmployerForm

def employer_reg(request):
    if request.method == 'POST':
        form = EmployerForm(request.POST)
        if form.is_valid():
            # Process the form data
            form.save()  # You can save the form data to the database
            return render(request, 'base.html')  # Redirect or perform other actions
    else:
        form = EmployerForm()

    return render(request, 'employer_reg.html', {'form': form})
