import random


def generate_otp(length=8):
    """Generate a random OTP of specified length"""
    digits = "0123456789"
    otp = ""
    for i in range(length):
        otp += random.choice(digits)
    return otp
