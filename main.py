import hashlib
import time


def generate_pickup_code(student_id: str) -> str:
    """
    Generates an 8 character pickup code using:
    - Student ID for uniqueness
    - Current timestamp (hourly bucket for time window validation)
    
    Logic: Uses time buckets so codes remain valid for validation
    within 2 hours time window.
    """
    # Get current hour bucket
    current_hour = int(time.time() // 3600)
    
    # Unique string combining student_id and time bucket
    data = f"{student_id}:{current_hour}"
    
    # Generating hash because everyone can guess simple combination. Then take first 8 characters.
    hash_object = hashlib.sha256(data.encode())
    code = hash_object.hexdigest()[:8].upper()
    
    return code


def validate_pickup_code(student_id: str, code: str) -> bool:
    """
    Validates if a pickup code is correct for a student within the time window.
    
    Logic: Checks code against current hour and previous hour buckets,
    giving around 2 hour validity window.
    """
    current_hour = int(time.time() // 3600)
    
    # Check current hour and previous hour (2-hour window)
    for hour_offset in [0, -1]:
        test_hour = current_hour + hour_offset
        data = f"{student_id}:{test_hour}"
        hash_object = hashlib.sha256(data.encode())
        valid_code = hash_object.hexdigest()[:8].upper()
        
        if code.upper() == valid_code:
            return True
    
    return False

if __name__ == "__main__":
    print("*** Examples ***\n")
    
    # Example 1: Generate and immediately validate
    student1 = "S282539"
    code1 = generate_pickup_code(student1)
    print(f"Student1: {student1}")
    print(f"Generated Code: {code1}")
    print(f"Codes Match: {validate_pickup_code(student1, code1)}")
    print()
    
    # Example 2: Different student gets different code
    student2 = "S282540"
    print(f"Student2: {student2}")
    code2 = generate_pickup_code(student2)
    print(f"Generated Code: {code2}")
    print(f"Codes Match: {validate_pickup_code(student2, code2)}")
    print()
    
    # Example 3: Wrong code fails validation
    print(f"Attempting to use {student1}'s code for {student2}")
    print(f"Codes Match: {validate_pickup_code(student2, code1)}")
    print()
    
	# Example 4: Same student requests code again within same hour
    print(f"Student1: {student1} requests code again:")
    code1_again = generate_pickup_code(student1)
    print(f"New Code: {code1_again}")
    print(f"Codes Match: {code1 == code1_again}")
    print()
    
	# Example 5: Simulate code expiration by checking an old code
    print(f"Simulating code expiration for {student1}:")
    three_hours_ago = int(time.time() // 3600) - 3
    data = f"{student1}:{three_hours_ago}"
    hash_object = hashlib.sha256(data.encode())
    code3 = hash_object.hexdigest()[:8].upper()
    print(f"Codes Match: {validate_pickup_code(student1, code3)}")