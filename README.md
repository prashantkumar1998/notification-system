Whenever a new order is created or order status gets changed a msg has been send to notification service by logistics services through kafka broker

Once a new msg(tracking I'd, brand name) comes from logistics sevice notification handler pick it from here and check in db for that perticular brand, which channel need to be used to send notification, and new msg(tracking I'd) will pushed to Kafka

As the new msg populated here services like email_notifier, text_notifier, wp_notifier pick it ....these services call order-details api to get user details and status further prepar notification and send to end user

