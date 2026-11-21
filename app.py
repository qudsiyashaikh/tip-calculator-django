import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.template import Context, Template
from django.urls import path

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY="super-secret-key-for-tip-calculator",
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
        }
    ],
)


def tip_calculator(request):
    per_person = None
    total_with_tip = None
    error = None

    if request.method == "POST":
        try:
            bill = float(request.POST.get("bill", 0))
            tip_percent = float(request.POST.get("tip", 0))
            people = int(request.POST.get("people", 1))

            if bill <= 0 or tip_percent < 0 or people <= 0:
                error = "Please enter positive values (bill and people must be greater than 0)."
            else:
                tip_amount = bill * (tip_percent / 100)
                total_with_tip = round(bill + tip_amount, 2)
                per_person = round(total_with_tip / people, 2)
        except ValueError:
            error = "Please enter valid numbers."

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tip Calculator </title>
        <style>
            body { font-family: Arial, sans-serif; background: #f0f2f5; text-align: center; margin-top: 70px; }
            .container { display: inline-block; padding: 35px; background: white; border-radius: 12px; box-shadow: 0px 4px 20px rgba(0,0,0,0.1); width: 400px; }
            h2 { color: #092e20; margin-bottom: 20px; }
            input { width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; font-size: 16px; }
            button { width: 96%; background-color: #092e20; color: white; border: none; padding: 12px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-top: 10px; }
            button:hover { background-color: #114b35; }
            .result { margin-top: 22px; padding: 15px; background: #e8f5e9; border-radius: 6px; color: #1b5e20; font-size: 17px; font-weight: bold; }
            .error { margin-top: 18px; padding: 12px; background: #fdecea; border-radius: 6px; color: #b71c1c; font-size: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>💰  Tip Calculator</h2>
            <form method="POST">
                {% csrf_token %}
                <input type="number" step="0.01" name="bill" placeholder="Total Bill Amount (e.g. 1200)" required autofocus>
                <input type="number" step="0.1" name="tip" placeholder="Tip Percentage (e.g. 10, 15, 20)" required>
                <input type="number" name="people" placeholder="Number of People to Split" required>
                <button type="submit">Calculate Split</button>
            </form>

            {% if error %}
                <div class="error">{{ error }}</div>
            {% endif %}

            {% if per_person is not None %}
                <div class="result">
                    Total Bill + Tip: ₹{{ total_with_tip }} <br>
                    Each Person Pays: ✨ ₹{{ per_person }} ✨
                </div>
            {% endif %}
        </div>
    </body>
    </html>
    """
    t = Template(html_content)
    c = Context({
        "per_person": per_person,
        "total_with_tip": total_with_tip,
        "error": error,
        "request": request,
    })
    return HttpResponse(t.render(c))


urlpatterns = [
    path("", tip_calculator),
]

if __name__ == "__main__":
    execute_from_command_line([sys.argv[0], "runserver"])