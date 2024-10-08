import hashlib
import base64

from decimal import Decimal
from datetime import datetime

from profiles.models import Profile


def hash_to_smaller_int(large_int):
    # Convert the large integer to a string before hashing
    large_int_str = str(large_int)
    
    # Compute the SHA-256 hash of the string representation of the large integer
    hashed_bytes = hashlib.sha256(large_int_str.encode()).digest()
    
    # Convert the hashed bytes to an integer
    hashed_int = int.from_bytes(hashed_bytes, byteorder='big')
    
    # Generate a smaller integer by taking the modulo of a large number
    smaller_int = hashed_int % (10 ** 9)  # Restricting to a 9-digit number
    
    return smaller_int


def base64_encode(value):
    # Encode the concatenated string using Base64
    return base64.b64encode(value.encode()).decode()


def date_formatter(date):
    return date.strftime('%a, %d %m %Y')


def convert_lbs_to_kg(value, unit):
    if unit == "lbs":
        return value * Decimal("0.453592")
    elif unit == "kg":
        return value


def convert_ft_to_cm(value, unit):
    if unit == "ft":
        return value * Decimal("30.48")
    elif unit == "cm":
        return value
        

def calculate_calorie(sex, weight, height, age, activity_level, goal):
    BMR = None
    AMR = None
    calorie = None

    if sex == "male":
        BMR = (Decimal("10") * weight) + (Decimal("6.25") * height) - (Decimal("5") * age) + Decimal("5") 
    elif sex == "female":
        BMR = (Decimal("10") * weight) + (Decimal("6.25") * height) - (Decimal("5") * age) - Decimal("161")

    if activity_level == "very active":
        AMR = Decimal("1.9") * BMR
    elif activity_level == "active":
        AMR = Decimal("1.725") * BMR
    elif activity_level == "moderate activity":
        AMR = Decimal("1.55") * BMR
    elif activity_level == "low activity":
        AMR = Decimal("1.375") * BMR
    
    if goal == "lose weight":
        calorie = AMR - 500
    elif goal == "gain weight":
        calorie = AMR + 500
    elif goal == "maintain weight":
        calorie = AMR

    carbs = round((Decimal("0.55") * calorie) / 4, 2)
    protein = round((Decimal("0.225") * calorie) / 4, 2)
    fats = round((Decimal("0.275") * calorie) / 9, 2)

    return [round(calorie, 2), carbs, protein, fats]

def calculate_requirements(user):
    try:
        profile = Profile.objects.get(user=user)
    except Exception as e:
        raise LookupError(e) from e

    today = datetime.today()
    dob = profile.dob
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)) 
    calorie, carbs, protein, fats = calculate_calorie(
        profile.sex.lower(),
        convert_lbs_to_kg(profile.weight, profile.weight_unit.lower()),
        convert_ft_to_cm(profile.height, profile.height_unit.lower()),
        age,
        profile.activity_level.lower(),
        profile.nutritional_goal.lower()
    )
    return calorie, carbs, protein, fats