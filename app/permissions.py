PERMISSIONS = {
    'user': [
        'get_self',
        'delete_self'
    ],
    'admin': [
        'get_all',
        'get_by_id',
        'get_self',
        'delete_self'
    ],
    'superadmin': [
        'get_all',
        'get_by_id',
        'promote',
        'demote',
        'get_self',
        'delete_by_id',
        'delete_self'
    ]
}
