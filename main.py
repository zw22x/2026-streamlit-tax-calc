

print("---Filing Status Selection---")
print("1. Single")
print("2. Married Filing Jointly")
print("3. Married Filing Separately")
print("4. Head of Household")
try:
    choice = input("Choose 1-4 corresponding to your filing status: ").strip()
    if choice not in ["1", "2", "3", "4"]:
        raise ValueError("Invalid choice. Please select a number between 1 and 4.")
    income = float(input("Enter your taxable income: "))
except ValueError:
    print("Invalid input. Please enter a valid number.")
    exit()

if choice == "1":
    maritalStatus = "single"
    fileJoint = "no"
elif choice == "2":
    maritalStatus = "married"
    fileJoint = "yes" 
elif choice == "3":
    maritalStatus = "married"
    fileJoint = "no"
elif choice == "4":
    maritalStatus = "head of household" 
    fileJoint = "no"
else:
    print("Invalid choice. Defaulting to single.")
    maritalStatus = "single"
    fileJoint = "no"

print("Do you have any dependents? (yes/no): ")
dependents = input().strip().lower()
if dependents == "yes":
    num_dependents = int(input("Enter the number of dependents: "))
else:
    num_dependents = 0

print("Do you qualify for the adoption tax credit? (yes/no): ")
adoption_credit = input().strip().lower()
if adoption_credit == "yes":
    adoption_credit_amount = 17670
else: adoption_credit_amount = 0

def calculate_deduction(maritalStatus):
    if maritalStatus == "single":
        return 16100
    elif maritalStatus == "married" and fileJoint == "yes":
        return 32200
    elif maritalStatus == "married" and fileJoint == "no":
        return 16100
    elif maritalStatus == "head of household":
        return 24150
    else:
        return 0

def calculate_tax(income, maritalStatus):
    if maritalStatus == "married" and fileJoint == "yes":
        if income > 0 and income <= 24799:
            return income * 0.10
        elif income > 24799 and income <= 100800:
            return 2480 + (income - 24800) * 0.12
        elif income > 100800 and income <= 211400:
            return 11600 + (income - 100800) * 0.22
        elif income > 211400 and income <= 403550:
            return 35932 + (income - 211400) * 0.24
        elif income > 403550 and income <= 512450:
            return 82048 + (income - 403550) * 0.32
        elif income > 512450 and income <= 768700:
            return 116896 + (income - 512450) * 0.35
        else:
            return 206583.50 + (income - 768700) * 0.37
    
    elif maritalStatus == "married" and fileJoint == "no":
        if income > 0 and income <= 12400:
            return income * 0.10
        elif income > 12400 and income <= 50400:
            return 1240 + (income - 12400) * 0.12
        elif income > 50400 and income <= 105700:
            return 5800 + (income - 50400) * 0.22
        elif income > 105700 and income <= 201775:
            return 17966 + (income - 105700) * 0.24
        elif income > 201775 and income <= 256225:
            return 41024 + (income - 201775) * 0.32
        elif income > 256225 and income <= 384350:
            return 58448 + (income - 256225) * 0.35
        else:
            return 103291.75 + (income - 384350) * 0.37
    
    elif maritalStatus == "single":
        if income > 0 and income <= 12400:
            return income * 0.10
        elif income > 12400 and income <= 50400:
            return 1250 + (income -12400) * 0.12
        elif income > 50400 and income <= 105700:
            return 5800 + (income -50400) * 0.22
        elif income > 105700 and income <= 201775:
            return 17966 + (income - 105700) * 0.24
        elif income > 201775 and income <= 256225:
            return 41024 + (income - 201775) * 0.32
        elif income > 256225 and income <= 640600:
            return 58448 + (income - 256225) * 0.35
        else:
            return 192979.25 + (income - 640600) * 0.37
    
    elif maritalStatus == "head of household":
        if income > 0 and income <= 17700:
            return income * 0.10
        elif income > 17700 and income <=67450:
            return 1770 + (income - 17700) * 0.12
        elif income > 67450 and income <= 105700:
            return 7740 + (income - 67450) * 0.22
        elif income > 105700 and income <= 201750:
            return 16155 + (income - 105700) * 0.24
        elif income > 201750 and income <= 256200:
            return 39207 + (income - 201750) * 0.32
        elif income > 256200 and income <= 640600:
            return 56631 + (income - 256200) * 0.35
        else:
            return 191171 + (income - 640600) * 0.37
    else:
        return 0
    

standard_deduction = calculate_deduction(maritalStatus)
taxable_income = max(0, income - standard_deduction - (num_dependents * 2200) - adoption_credit_amount)
final_tax = calculate_tax(taxable_income, maritalStatus)
print(f"Your tax liability is: ${final_tax:.2f}")
