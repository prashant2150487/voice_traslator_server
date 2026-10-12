class UserMessages:
    NOT_FOUND = "User not found"
    EMAIL_EXISTS = "Email already registered"

class AuthMessages:
    EMAIL_EXISTS = "Email already registered"
    INVALID_CREDENTIALS = "Invalid email or password"
    ACCOUNT_DISABLED = "Account is disabled"
    INVALID_TENANT = "Invalid tenant"
    INVALID_TOKEN = "Invalid or expired token"

class RoleMessages:
    NOT_FOUND = "Role not found"
    CODE_EXISTS = "Role code already exists"
    CODE_LOCKED = "The super_admin role code cannot be changed"
    UNKNOWN_PERMISSIONS = "Unknown permissions: {codes}"
    SUPER_ADMIN_LOCKED = "super_admin permissions cannot be changed"
    FORBIDDEN = "You do not have permission to do this"
    ROLE_NOT_ASSIGNABLE = "This role cannot be assigned"
    USER_NOT_FOUND = "User not found"
    CANNOT_CHANGE_OWN_ROLE = "You cannot change your own role"
    CANNOT_CHANGE_THIS_USER = "This user's role cannot be changed"