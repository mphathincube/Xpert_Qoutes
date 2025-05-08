from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect
from django.contrib import messages
from .forms import ClientForm, QuoteForm


def add_quote(request):
    if request.method == 'POST':
        # Initialize both forms
        client_form = ClientForm(request.POST)
        quote_form = QuoteForm(request.POST)

        # Check if an existing client is selected
        selected_client = quote_form.data.get('client')
        if selected_client and selected_client != '':
            # Skip ClientForm validation entirely
            if quote_form.is_valid():
                quote = quote_form.save(commit=False)
                quote.client_id = selected_client  # Assign the selected client
                quote.save()
                messages.success(
                    request, f"Quote for {quote.service} created successfully for {quote.client.name}!")
                return redirect('add_quote')
            else:
                messages.error(
                    request, "Please fill in all required quote fields (service and price).")
                return render(request, 'quotes/add_quote.html', {
                    'client_form': client_form,
                    'quote_form': quote_form
                })

        # If no existing client is selected, check for a new client
        # Only validate ClientForm if any data is provided
        has_client_data = any(request.POST.get(field)
                              for field in ['name', 'email', 'phone'])
        if has_client_data:
            if client_form.is_valid():
                new_client = client_form.save()
                if quote_form.is_valid():
                    quote = quote_form.save(commit=False)
                    quote.client = new_client
                    quote.save()
                    messages.success(
                        request, f"Quote for {quote.service} created successfully for {new_client.name}!")
                    return redirect('add_quote')
                else:
                    messages.error(
                        request, "Please fill in all required quote fields (service and price).")
            else:
                messages.error(
                    request, "Please provide a valid name for the new client.")
        else:
            messages.error(
                request, "Please either add a new client (at least a name) or select an existing client.")

        return render(request, 'quotes/add_quote.html', {
            'client_form': client_form,
            'quote_form': quote_form
        })

    else:
        client_form = ClientForm()
        quote_form = QuoteForm()

    return render(request, 'quotes/add_quote.html', {
        'client_form': client_form,
        'quote_form': quote_form
    })
