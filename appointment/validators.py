import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password, user=None):
        # Ensure password is at least 8 characters long
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        # Check for uppercase and lowercase letters
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        
        # Check for digits
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number.")
        
        # Check for special characters, excluding < and >
        if not re.search(r'[!@#?$%^&*(),./;:"[]{}|\\`~_+-]', password):
            raise ValidationError("Password must contain at least one special character.")
        
        # Ensure password doesn't contain < or >
        if '<' in password or '>' in password:
            raise ValidationError("Password cannot contain '<' or '>'.")

    def get_help_text(self):
        return (
            "Your password must be at least 8 characters long, contain both uppercase and lowercase letters, "
            "include at least one number, one special character (e.g., ! @ #), and cannot contain '<' or '>'."
        )
