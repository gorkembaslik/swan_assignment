import hashlib
import re
import time
import hmac

SERVER_SECRET = "SWAN_SECRET_2025"

def generate_pickup_code(student_id: str) -> str:
    """
    Generates an 8 character pickup code using:
    - Student ID for uniqueness
    - Current timestamp (10 minute bucket for time window validation)
    
    Logic: Uses time buckets so codes remain valid for validation
    within 10 minute time window.
    """
    # Input validation
    if not student_id or not isinstance(student_id, str):
        raise ValueError("student_id must be a non-empty string")
    
    if not re.match(r'^[A-Za-z0-9_-]{3,20}$', student_id):
        raise ValueError("student_id must be 3-20 alphanumeric characters")
    
    # Get current 10 minute bucket
    current_bucket = int(time.time() // 600)

    # Unique string combining student_id and time bucket
    data = f"{student_id}:{current_bucket}"

    # Create HMAC-SHA256 hash
    hash = hmac.new(SERVER_SECRET.encode(), data.encode(), hashlib.sha256)
    code = hash.hexdigest()[:8].upper()

    return code


def validate_pickup_code(student_id: str, code: str) -> bool:
    """
    Validates if a pickup code is correct for a student within the time window.
    
    Logic: Checks code against current 10-minute bucket and previous bucket,
    giving 10-20 minute validity window

    Uses constant-time comparison to prevent timing attacks.
    
    Args:
        student_id: Unique student identifier
        code: The 8-character pickup code to validate
    """

    if not student_id or not isinstance(student_id, str):
        return False
    
    if not re.match(r'^[A-Za-z0-9_-]{3,20}$', student_id):
        raise ValueError("student_id must be 3-20 alphanumeric characters")
    
    if not code or not isinstance(code, str):
        return False
    
    if not re.match(r'^[A-Fa-f0-9]{8}$', code):
        return False
    
    current_bucket = int(time.time() // 600)

    # Check current bucket (0-10 min old) and previous bucket (10-20 min old)
    for bucket_offset in [0, -1]:
        test_bucket = current_bucket + bucket_offset
        data = f"{student_id}:{test_bucket}"
        
        hash = hmac.new(SERVER_SECRET.encode(), data.encode(), hashlib.sha256)
        valid_code = hash.hexdigest()[:8].upper()

        # Constant-time comparison to prevent timing attacks
        if hmac.compare_digest(valid_code, code):
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

    # Example 2: Same student requests code again within same bucket
    print(f"Student1: {student1} requests code again:")
    code1_again = generate_pickup_code(student1)
    print(f"New Code: {code1_again}")
    print(f"Codes Match: {code1 == code1_again}")
    print()

    # Example 3: Different student gets different code
    student2 = "S282540"
    print(f"Student2: {student2}")
    code2 = generate_pickup_code(student2)
    print(f"Generated Code: {code2}")
    print(f"Codes Match: {validate_pickup_code(student2, code2)}")
    print()

    # Example 4: Wrong code fails validation
    print(f"Attempting to use {student1}'s code for {student2}")
    print(f"Codes Match: {validate_pickup_code(student2, code1)}")
    print()

    # Example 5: Simulate code expiration by checking an old code
    current_bucket = int(time.time() // 600)
    two_buckets_ago = current_bucket - 1
    data = f"{student1}:{two_buckets_ago}"
    hmac_hash = hmac.new(SERVER_SECRET.encode(), data.encode(), hashlib.sha256)
    valid_code = hmac_hash.hexdigest()[:8].upper()
    
    print(f"   Student: {student1}")
    print(f"   Code from a bucket ago: {valid_code}")
    is_valid = validate_pickup_code(student1, valid_code)
    print(f"   Validation: {is_valid} (Expected: True)\n")

    # Example 5: Simulate code expiration by checking an old code
    current_bucket = int(time.time() // 600)
    two_buckets_ago = current_bucket - 2
    data = f"{student1}:{two_buckets_ago}"
    hmac_hash = hmac.new(SERVER_SECRET.encode(), data.encode(), hashlib.sha256)
    expired_code = hmac_hash.hexdigest()[:8].upper()
    
    print(f"   Student: {student1}")
    print(f"   Code from 2 buckets ago: {expired_code}")
    is_valid = validate_pickup_code(student1, expired_code)
    print(f"   Validation: {is_valid} (Expected: False)\n")
