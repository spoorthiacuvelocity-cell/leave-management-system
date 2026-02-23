import smtplib

email = "acumenleavesystem@gmail.com"
password = "fdkfrrqfirfnpmwa"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    print("LOGIN SUCCESS")
    server.quit()
except Exception as e:
    print("LOGIN FAILED:", e)