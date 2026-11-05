Chapter 04 - Access Control
Python Account RBAC demonstration

Requirements: Python 3. No extra packages, database or network are needed.
Run from this folder:
    python rbac.py
On Windows, if Python is installed through its launcher:
    py -3 rbac.py

Choose admin, manager, customer or trainee. These are demonstration identities,
not authenticated accounts. Anyone using the console can select an identity;
this program demonstrates authorization, not a secure login system.

Starting assignments:
admin -> Admin: Create, View, Update, Delete
manager -> Manager: View, Update
customer -> Customer: View
trainee -> no role: denied until an Admin assigns a role

Menu 1 creates an Account ID and name. Menu 2 shows one account, or all accounts
when its ID is blank. Menu 3 changes a name. Menu 4 removes an account.
Menu 5 assigns an existing demo user to a role. Menu 6 grants or revokes a role
permission. Only a user currently assigned Admin can use menus 5 and 6.
Menu 7 switches the demonstration identity. Menu 0 exits.
Names of roles and permissions are case-sensitive, as printed in the prompts.

Code explanation:
The users dictionary maps each username to one role. The permissions dictionary
maps each role to a set of Account actions. The accounts dictionary stores the
actual sample Account IDs and names. can_access finds the user's role and checks
the requested action. Unknown users, roles and actions deny by default.
perform checks authorization before CRUD validation and data changes.
assign_user and assign_permission separately require the Admin role.
main provides a small input/print menu using these same functions.

All data is in memory and resets on exit. The one-role-per-user design is a
small subset of general RBAC, which can allow several roles and sessions.
There are no real credentials, persistence, authentication or production claims.
The supplied accounts are fictional examples.
