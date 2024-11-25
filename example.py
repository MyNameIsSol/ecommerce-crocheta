from accounts.models import Account

# Retrieve the user
user = Account.objects.get(username='crocheta')

# Update the is_active field
user.is_active = True
user.save()

# Confirm the change
print(f"User {user.username} is_active status: {user.is_active}")
