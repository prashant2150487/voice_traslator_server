class TenantStatus:
    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    ALL = (TRIAL, ACTIVE, PAST_DUE, SUSPENDED, CANCELLED)
    ACCEPTS_NEW_USERS = (TRIAL, ACTIVE, PAST_DUE)

class SubscriptionStatus:
    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    ALL = (TRIALING, ACTIVE, PAST_DUE, CANCELLED)