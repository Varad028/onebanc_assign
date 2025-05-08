
import re

# Constants for violation types
PATTERN_VIOLATION = 'PATTERN_VIOLATION: Common pattern detected'
SAME_DIGITS = 'SAME_DIGITS: All digits are the same'
SEQUENTIAL = 'SEQUENTIAL: Sequential digits'
REPEATED_GROUPS = 'REPEATED_GROUPS: Repeating pattern of digits'
DEMOGRAPHIC_MATCH = 'DEMOGRAPHIC_MATCH: Matches personal information'
PALINDROME = 'PALINDROME: Reads the same forward and backward'
KEYPAD_PATTERN = 'KEYPAD_PATTERN: Forms a pattern on keypad'
KEYBOARD_SEQUENTIAL = 'KEYBOARD_SEQUENTIAL: Sequential keys on keyboard/keypad'
ALL_SAME_TYPE = 'ALL_SAME_TYPE: All digits are even or all digits are odd'
MATHEMATICAL_PATTERN = 'MATHEMATICAL_PATTERN: Special mathematical sequence'
LAZY_REPEAT = 'LAZY_REPEAT: Simple repetition pattern'
ALTERNATING_DIGITS = 'ALTERNATING_DIGITS: Alternating digit pattern'

# Define common geometric patterns on keypad
KEYPAD_PATTERNS = [
    '147258', '258147', '852741', '741852',  # columns
    '159357', '357159', '753951', '951753',  # 'X' shape
    '258025', '025852', '520258', '852025',  # diagonals
    '147963', '369741',  # L shapes
    '963741', '147369'   # reverse L shapes
]

# Keyboard rows and patterns (standard number row and numpad)
KEYBOARD_SEQUENCES = [
    '123456', '234567', '345678', '456789', '567890',  # forward sequences
    '654321', '765432', '876543', '987654', '098765',  # backward sequences
    '123698', '896321',  # diagonal walks
    '789456', '456123', '123456', '456789',  # numpad rows
    '741852', '852963', '963852', '852741',  # numpad columns
]

# Mathematical curiosities
MATHEMATICAL_PATTERNS = [
    '142857',  # Repeating decimal of 1/7
    '100489', '117649', '262144',  # Perfect squares/cubes examples
]

def check_mpin(pin, dob_self=None, dob_spouse=None, anniversary=None):
    """
    Check if the MPIN follows any common patterns.
    Returns a list of violations if found, or empty list if secure.
    """
    violations = []
    
    # Validate input format
    if not re.fullmatch(r"\d{6}", pin):
        return ["INVALID_FORMAT: MPIN must be a 6-digit numeric string"]
    
    # Check for same digit repeating (e.g., 111111)
    if len(set(pin)) == 1:
        violations.append(SAME_DIGITS)
    
    # Check for repeating patterns (e.g., 123123, 112233)
    for d in (1, 2, 3):
        if pin == pin[:d] * (6 // d):
            violations.append(REPEATED_GROUPS)
            break
    
    # Check for increasing sequence (e.g., 123456)
    if all(int(pin[i+1]) - int(pin[i]) == 1 for i in range(5)):
        violations.append(SEQUENTIAL)
    
    # Check for decreasing sequence (e.g., 654321)
    if all(int(pin[i]) - int(pin[i+1]) == 1 for i in range(5)):
        violations.append(SEQUENTIAL)
    
    # Check for keyboard sequences
    if any(pin == pattern or pin == pattern[::-1] for pattern in KEYBOARD_SEQUENCES):
        violations.append(KEYBOARD_SEQUENTIAL)
    
    # Check for palindrome numbers (e.g., 123321)
    if pin == pin[::-1] and len(set(pin)) > 1:  # Avoid duplicate with SAME_DIGITS
        violations.append(PALINDROME)
    
    # Check for keypad patterns
    if any(pin == pattern or pin == pattern[::-1] for pattern in KEYPAD_PATTERNS):
        violations.append(KEYPAD_PATTERN)
    
    # Check for mathematical curiosities
    if pin in MATHEMATICAL_PATTERNS:
        violations.append(MATHEMATICAL_PATTERN)
    
    # Check for all even or all odd digits
    if all(int(d) % 2 == 0 for d in pin) or all(int(d) % 2 == 1 for d in pin):
        violations.append(ALL_SAME_TYPE)
    
    # Check for "lazy" repeats like 112233
    if re.match(r"(\d)\1(\d)\2(\d)\3", pin):
        violations.append(LAZY_REPEAT)
    
    # Check for alternating patterns like 121212, 131313
    if re.match(r"(\d)(\d)\1\2\1\2", pin):
        violations.append(ALTERNATING_DIGITS)
    if len(set(pin[::2])) == 1 and len(set(pin[1::2])) == 1:
        violations.append(ALTERNATING_DIGITS)
    
    # Check for demographic matches
    for date_str in [dob_self, dob_spouse, anniversary]:
        if date_str and re.fullmatch(r"\d{8}", date_str):
            # Check if PIN is contained in the date
            if pin in date_str:
                violations.append(DEMOGRAPHIC_MATCH)
                break
            
            # Check for significant digit overlap
            date_digits = {d: date_str.count(d) for d in set(date_str)}
            pin_digits = {d: pin.count(d) for d in set(pin)}
            
            common_digits = 0
            for digit in pin_digits:
                if digit in date_digits and pin_digits[digit] <= date_digits[digit]:
                    common_digits += pin_digits[digit]
            
            if common_digits >= 4:  # If 4+ digits match in frequency
                violations.append(DEMOGRAPHIC_MATCH)
                break
    
    return violations

# def main():
#     print("=== Secure 6-digit MPIN Validator ===")
#     print("This program checks if your MPIN follows common patterns that should be avoided.")
    
#     while True:
#         print("\nOptions:")
#         print("1. Check MPIN security")
#         print("2. Exit")
        
#         choice = input("Enter choice (1-2): ").strip()
        
#         if choice == '1':
#             pin = input("\nEnter 6-digit MPIN to check: ").strip()
            
#             # Optional demographic information
#             print("\nOptional: Enter personal information to check for matches (or press Enter to skip)")
#             dob_self = input("Your date of birth (YYYYMMDD): ").strip() or None
#             dob_spouse = input("Spouse's date of birth (YYYYMMDD): ").strip() or None
#             anniversary = input("Anniversary date (YYYYMMDD): ").strip() or None
            
#             # Check the MPIN
#             violations = check_mpin(pin, dob_self, dob_spouse, anniversary)
            
#             print("\n=== MPIN Security Check Results ===")
#             if not violations:
#                 print("✓ SECURE: Your MPIN doesn't follow any common patterns")
#                 print("✓ This MPIN is acceptable")
#             else:
#                 print("✗ INSECURE: Your MPIN is not acceptable")
#                 print("\nReason for rejection:")
#                 print(f"  - {violations[0]}")  # Show only the first violation
#                 print("\n✗ Please choose a different MPIN")
#                 print("\nA secure MPIN should:")
#                 print("- Not contain repeated or sequential digits")
#                 print("- Not form patterns on a keypad or keyboard")
#                 print("- Not relate to your personal information")
#                 print("- Not use only even or only odd digits")
#                 print("- Not be a palindrome or have simple repeating patterns")
        
#         elif choice == '2':
#             print("Thank you for using the MPIN Validator. Goodbye!")
#             break
        
#         else:
#             print("Invalid choice. Please enter 1 or 2.")

# if __name__ == '__main__':
#     main()