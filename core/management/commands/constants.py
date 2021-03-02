from api.common import constants


N_USERS = 11
N_TENANTS = 5

ADMIN = constants.TENANT_USER_ROLE_TYPE.ADMIN.value
GENERAL = constants.TENANT_USER_ROLE_TYPE.GENERAL.value

TENANT_USERS = {
    1: (1, 1, ADMIN), # tenant_user_id: user_id, tenant_id, role_type
    2: (1, 2, GENERAL),
    4: (3, 1, GENERAL),
    3: (2, 2, ADMIN),
    5: (3, 3, ADMIN),
    6: (4, 1, ADMIN),
    7: (5, 2, GENERAL),
    8: (6, 3, GENERAL),
    9: (7, 1, GENERAL),
    10: (8, 2, GENERAL),
    11: (9, 3, GENERAL),
    12: (10, 1, GENERAL),
}
