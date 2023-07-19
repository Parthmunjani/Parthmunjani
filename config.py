from flask import Flask
# from flask_rbac import RBAC, RoleMixin
# from app.models.model import UserModel, Roles

app = Flask(__name__)

# RBAC_USE_WHITE = True

# class Role(RoleMixin):
#     pass

# Role.roles = {
#     'admin': Role('admin'),
#     'user': Role('user'),
# }

# rbac = RBAC(app, role_model=Role)
# rbac.set_user_model(UserModel)
# rbac.set_role_model(Roles)
