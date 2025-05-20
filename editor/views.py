from django.shortcuts import render
import json
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# This renders the HTML page with the Monaco Editor
def editor_view(request):
    return render(request, 'editor.html')

# This handles the code execution request
@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get("code", "")

        try:
            result = subprocess.run(
                ['python3', '-c', code],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "Execution timed out."

        return JsonResponse({"output": output})