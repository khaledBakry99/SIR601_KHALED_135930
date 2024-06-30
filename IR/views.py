import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from IR.forms import MainPageForm, SearchPageForm
from IR.info_retrival_models.retrival_models import show_results, query_function
from IR.models import MainPage


@csrf_exempt
def main_page_view(request):
    if request.method == 'POST':
        # print('HERE: ', request.POST)
        form = MainPageForm(request.POST)
        if form.is_valid():
            instance = form.save()
            # json_string = json.dumps(form.cleaned_data['documents'], ensure_ascii=False).encode('utf8')
            # print(json_string)
            print('Form is valid')

            redirect_url = reverse('search_page_view', kwargs={'identifier': instance.pk})
            print('HEEEEEEEEEEEEEEEEEEEERE', redirect_url)
            return JsonResponse({'redirect_url': redirect_url})
        else:
            # Form is not valid, print errors
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {', '.join(errors)}")
    else:
        form = MainPageForm()

    # Render the view
    return render(
        request,
        'main.html',
        {'form': form}
    )


@csrf_exempt
def search_page_view(request, identifier):
    if request.method == 'POST':
        # print('HERE: ', request.POST)
        form = SearchPageForm(request.POST)
        if form.is_valid():
            print('Form is valid')
            instance = MainPage.objects.get(pk=identifier)
            language = instance.language
            documents = instance.documents
            retrieval_model = form.cleaned_data['retrieval_model']
            query = form.cleaned_data['query']
            print(retrieval_model)
            # print(query)
            to_ret = query_function(language, retrieval_model, documents, query)
            print(type(to_ret))
            return JsonResponse({'docs': documents, 'docs_result': to_ret}, safe=False)
        else:
            # Form is not valid, print errors
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {', '.join(errors)}")
    else:
        try:
            instance = MainPage.objects.get(pk=identifier)
            language = instance.language
            documents = instance.documents

            form_data = {
                'language': language,
                'documents': documents,
            }
            # Pass form_data to the template or use it as needed
            return render(request, 'search.html', {'form_data': form_data})
        except MainPage.DoesNotExist:
            return render(request, 'not_found.html')


def not_found_page_view(request, identifier):
    return render(request, 'not_found.html')
