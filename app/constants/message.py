class UserMessages:
    NOT_FOUND = "User not found"
    EMAIL_EXISTS = "Email already registered"

class AuthMessages:
    EMAIL_EXISTS = "Email already registered"
    INVALID_CREDENTIALS = "Invalid email or password"
    ACCOUNT_DISABLED = "Account is disabled"
    INVALID_TENANT = "Invalid tenant"
    TENANT_SLUG_EXISTS = "Tenant slug already registered"
    INVALID_TOKEN = "Invalid or expired token"
    NOT_AUTHENTICATED = "Authentication required"
    TOKEN_EXPIRED = "Access token expired"
    TENANT_SUSPENDED = "This company account is not accepting new users"

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

class TenantMessages:
    NOT_FOUND = "Tenant not found"
    SLUG_EXISTS = "Slug is already taken"
    SLUG_RESERVED = "Slug is reserved"
    ADMIN_EMAIL_EXISTS = "Admin email is already registered"
    BAD_TRANSITION = "Tenant cannot move from '{current}' to '{target}'"

class LanguageMessages:
    EXISTS = "Language code already exists"
    NOT_FOUND = "Language not found"

class PlanMessages:
    NOT_FOUND = "Plan not found"
    CODE_EXISTS = "Plan code already exists"
    UNKNOWN_LANGUAGES = "Unknown languages in plan limits: {codes}"
    INACTIVE = "Plan not found or inactive"