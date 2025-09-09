from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
import json

# JSON at: dashboard/data/budget.json
BUDGET_FILE = Path(__file__).resolve().parent / "data" / "budget.json"

def dashboard_page(request):
    # Template at: dashboard/templates/dashboard.html
    return render(request, "dashboard.html")

@csrf_exempt
def budget_api(request):
    if request.method == "GET":
        if not BUDGET_FILE.exists():
            # Return an empty-but-valid shape so the UI can render
            return JsonResponse({"header": {}, "summary": {}, "divisions": []})
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"header": {}, "summary": {}, "divisions": []}
        return JsonResponse(data, safe=False)

    if request.method == "PUT":
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
            if not isinstance(payload, dict):
                return HttpResponseBadRequest("JSON must be an object")
        except Exception as e:
            return HttpResponseBadRequest(f"Invalid JSON: {e}")

        BUDGET_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(BUDGET_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        return JsonResponse(payload, safe=False)

    return HttpResponseNotAllowed(["GET", "PUT"])
