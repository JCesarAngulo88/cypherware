/**

@api {get} /api/health API Health Check

@apiName GetHealth

@apiGroup System

@apiVersion 1.0.0

@apiDescription Verifies that the Flask server and database connection are active.

@apiSuccess {String} status "healthy"

@apiSuccess {String} database "connected"

@apiSuccess {String} timestamp ISO format timestamp.*/

/**

@api {get} /api/contacts List all contacts

@apiName GetContacts

@apiGroup Contacts

@apiVersion 1.0.0

@apiDescription Retrieves a list of all project inquiries stored in the database.

@apiSuccess {Object[]} contacts List of contact objects.
*/

/**

@api {post} /api/contacts Create a new contact

@apiName PostContact

@apiGroup Contacts

@apiVersion 1.0.0

@apiBody {String} user_name Full name.

@apiBody {String} email_address Email.

@apiBody {String} phone_number Phone.

@apiBody {String} service_type Service requested.

@apiBody {String} project_name Project name.

@apiBody {String} project_description Requirements.

@apiSuccess (201) {String} message Success message.

@apiSuccess (201) {Object} contact The created object.
*/

/**

@api {get} /api/contacts/:id Get contact details

@apiName GetContactById

@apiGroup Contacts

@apiVersion 1.0.0

@apiParam {Number} id Unique ID of the contact.

@apiSuccess {Number} id Unique ID.

@apiSuccess {String} user_name Full name.

@apiSuccess {String} email_address Email.

@apiError (404) NotFound The contact with that ID was not found.
*/

/**

@api {delete} /api/contacts/:id Delete a contact

@apiName DeleteContact

@apiGroup Contacts

@apiVersion 1.0.0

@apiParam {Number} id Unique ID of the contact to delete.

@apiSuccess {String} message Deletion confirmation.

@apiError (404) NotFound The contact with that ID was not found.
*/