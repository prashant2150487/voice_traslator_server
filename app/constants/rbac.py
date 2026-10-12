

class Roles:
    SUPER_ADMIN = 'super_admin'
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


ROLES = [
    {"code": "super_admin", "name": "Super Admin", "scope": "platform",
     "description": "Whole platform, no tenant. Your own team. Manages tenants, plans, suspension, provider profiles, platform usage and billing status. Does not read transcripts; support access is explicit, time-limited and audited."},
    {"code": "admin", "name": "Admin", "scope": "tenant",
     "description": "One tenant. The person who bought the plan and anyone they promote. Company settings, users and invitations, plan and billing, usage, audit log, all company rooms and transcripts."},
    {"code": "user", "name": "User", "scope": "tenant",
     "description": "One tenant. Company employees. Create and join rooms, set own language and voice, see transcripts of rooms they joined, invite guests to rooms they host."},
    {"code": "guest", "name": "Guest", "scope": "room",
     "description": "One room. External invitee. Join the invited room only, speak, listen and see the live transcript. No access to company data. History after leaving is off by default."},
]

PERMISSIONS = {
    # platform
    "tenants.manage": "Create, edit and suspend tenants",
    "plans.manage": "Manage plans",
    "providers.manage": "Manage platform provider profiles",
    "platform.usage.view": "View platform usage and billing status",
    "support.access": "Explicit, time-limited, audited support access",
    "roles.view": "View roles and permissions",
    "roles.manage": "Edit role permissions",
    # tenant admin
    "company.settings": "Manage company settings",
    "users.manage": "Manage users, roles and invitations",
    "billing.manage": "Manage plan and billing",
    "usage.view": "View tenant usage",
    "audit.view": "View audit log",
    "rooms.view_all": "View all company rooms",
    "transcripts.view_all": "View all company transcripts",
    # user
    "rooms.create": "Create rooms",
    "rooms.join": "Join rooms",
    "profile.edit": "Set own language and voice",
    "transcripts.view_own": "View transcripts of joined rooms",
    "guests.invite": "Invite guests to hosted rooms",
    # guest
    "room.join_invited": "Join the invited room only",
    "room.speak_listen": "Speak and listen in the room",
    "transcript.live": "See the live transcript",
}
ROLE_PERMISSIONS = {
    "super_admin": ["tenants.manage", "plans.manage", "providers.manage", "platform.usage.view",
                    "support.access", "roles.view", "roles.manage"],
    "admin": ["company.settings", "users.manage", "billing.manage", "usage.view", "audit.view",
              "rooms.view_all", "transcripts.view_all", "rooms.create", "rooms.join",
              "profile.edit", "guests.invite", "roles.view"],
    "user": ["rooms.create", "rooms.join", "profile.edit", "transcripts.view_own", "guests.invite"],
    "guest": ["room.join_invited", "room.speak_listen", "transcript.live"],
}