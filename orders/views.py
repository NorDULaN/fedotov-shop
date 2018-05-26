from django.http import JsonResponse


def ordersAdd(request):
    return_dict = dict()

    session_key = request.session.session_key
    print(request.POST)
    
    return JsonResponse(return_dict)
