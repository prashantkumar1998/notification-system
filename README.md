Whenever a new order is created or order status gets changed a msg has been send to notification service by logistics services

Once a new msg came (tracking I'd, brand name) notification handler pick it here and check in db for that perticular brand which channel need to be used to send notification, and new msg(tracking I'd) has been pushed to Kafka 

As the new msg populated here services like email_notifier, text_notifier, wp_notifier pick it ....call api from order details to get user details and status and send notification to end user
