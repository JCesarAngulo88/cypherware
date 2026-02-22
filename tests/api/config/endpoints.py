class Endpoints:
    """API test_endpoints configuration"""

    # Auth test_endpoints
    LOGIN = "/auth/login" # TODO:
    LOGOUT = "/auth/logout" # TODO:
    REFRESH_TOKEN = "/auth/refresh" # TODO:

    # User test_endpoints
    USERS = "/users" # TODO:
    USER_BY_ID = "/users/{id}" # TODO:

    # Product test_endpoints
    PRODUCTS = "/products" # TODO:
    PRODUCT_BY_ID = "/products/{id}" # TODO:

    # Health endpoint
    HEALTH: str = "/api/health"
    # Contact test_endpoints
    CONTACTS = "/api/contacts"
    CONTACTS_BY_ID = "/api/contacts/"