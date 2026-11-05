"""A small in-memory RBAC example for the Account object."""


class RBAC:
    def __init__(self):
        self.users = {'admin': 'Admin', 'manager': 'Manager',
                      'customer': 'Customer', 'trainee': None}
        self.permissions = {
            'Admin': {'Create', 'View', 'Update', 'Delete'},
            'Manager': {'View', 'Update'},
            'Customer': {'View'}
        }
        self.accounts = {'A100': 'Sample Account'}

    def can_access(self, user, action):
        """Unknown users, roles and actions have no permission."""
        role = self.users.get(user)
        return action in self.permissions.get(role, set())

    def perform(self, user, action, account_id='', name=''):
        # Check authorization before changing any account data.
        if not self.can_access(user, action):
            return False, 'DENIED: ' + user + ' cannot ' + action + ' Account.'
        account_id = account_id.strip()
        name = name.strip()
        if action == 'View':
            if account_id:
                if account_id not in self.accounts:
                    return False, 'Account not found.'
                return True, account_id + ': ' + self.accounts[account_id]
            if not self.accounts:
                return True, 'No accounts.'
            return True, '\n'.join(key + ': ' + value for key, value in self.accounts.items())
        if action == 'Create':
            if not account_id or not name:
                return False, 'Account ID and name are required.'
            if account_id in self.accounts:
                return False, 'Account ID already exists.'
            self.accounts[account_id] = name
            return True, 'CREATED ' + account_id + ': ' + name
        if account_id not in self.accounts:
            return False, 'Account not found.'
        if action == 'Update':
            if not name:
                return False, 'Account name is required.'
            self.accounts[account_id] = name
            return True, 'UPDATED ' + account_id + ': ' + name
        if action == 'Delete':
            del self.accounts[account_id]
            return True, 'DELETED ' + account_id
        return False, 'Unknown action.'

    def assign_user(self, actor, user, role):
        # Administration is a separate Admin-only operation.
        if self.users.get(actor) != 'Admin':
            return False, 'DENIED: only Admin can assign roles.'
        if user not in self.users or role not in self.permissions:
            return False, 'Unknown user or role.'
        self.users[user] = role
        return True, 'ASSIGNED ' + user + ' -> ' + role

    def assign_permission(self, actor, role, action, grant):
        if self.users.get(actor) != 'Admin':
            return False, 'DENIED: only Admin can assign permissions.'
        if role not in self.permissions or action not in {'Create', 'View', 'Update', 'Delete'}:
            return False, 'Unknown role or permission.'
        if grant:
            self.permissions[role].add(action)
            return True, 'GRANTED ' + action + ' to ' + role
        self.permissions[role].discard(action)
        return True, 'REVOKED ' + action + ' from ' + role


def main():
    app = RBAC()
    print('Account RBAC demonstration')
    print('Demo identity selection is NOT real authentication.')
    print('Data and assignments reset when the program exits.')
    user = input('Select demo user (admin/manager/customer/trainee): ').strip()
    if user not in app.users:
        print('DENIED: unknown user.')
        return
    while True:
        print('\nUser: ' + user + ' | Role: ' + str(app.users[user]))
        print('1 Create | 2 View | 3 Update | 4 Delete')
        print('5 Assign user role | 6 Assign role permission | 7 Switch demo user | 0 Exit')
        choice = input('Choice: ').strip()
        if choice == '0':
            print('Goodbye.')
            break
        if choice in {'1', '2', '3', '4'}:
            action = {'1':'Create', '2':'View', '3':'Update', '4':'Delete'}[choice]
            if not app.can_access(user, action):
                print(app.perform(user, action)[1])
                continue
            account_id = input('Account ID (blank = all for View): ').strip()
            name = input('Account name: ').strip() if action in {'Create', 'Update'} else ''
            print(app.perform(user, action, account_id, name)[1])
        elif choice == '5':
            if app.users.get(user) != 'Admin':
                print('DENIED: only Admin can assign roles.')
                continue
            target = input('User (admin/manager/customer/trainee): ').strip()
            role = input('Role (Admin/Manager/Customer): ').strip()
            print(app.assign_user(user, target, role)[1])
        elif choice == '6':
            if app.users.get(user) != 'Admin':
                print('DENIED: only Admin can assign permissions.')
                continue
            role = input('Role (Admin/Manager/Customer): ').strip()
            action = input('Permission (Create/View/Update/Delete): ').strip()
            mode = input('grant or revoke: ').strip()
            if mode not in {'grant', 'revoke'}:
                print('Invalid permission mode.')
                continue
            print(app.assign_permission(user, role, action, mode == 'grant')[1])
        elif choice == '7':
            target = input('Select demo user: ').strip()
            if target in app.users:
                user = target
            else:
                print('DENIED: unknown user. Current demo user unchanged.')
        else:
            print('Invalid menu choice.')


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\nDemo ended.')
