import requests
from math import sqrt

from django.http import JsonResponse
from rest_framework.decorators import api_view

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

@api_view(['GET'])
def classify_number(request):
    number = request.GET.get('number')

    if not number or not number.lstrip('-').isdigit():
        return JsonResponse({"number": number, "error": True}, status=400)

    number = int(number)
    
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 else "even")
    
    digit_sum = sum(int(d) for d in str(abs(number)))
    
    fun_fact = "No fun fact available"
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math?json")
        if response.status_code == 200:
            fun_fact = response.json().get("text", "No fun fact available")
    except:
        pass  # Handle failure gracefully

    return JsonResponse({
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    })
