

def order_sms(request, called_service):
    sender = UserProfile.objects.get(person =called_service.admin)
    sennum = sender.phone_number
    phone = str(sennum)
    account_sid = tw_sid
    auth_token = tw_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Hi {called_service.name} admin, You have a new service order for your {called_service.category} service on rendapp. Kindly accept the order if you are interested ",
        from_='+12569608957',
        to= phone
    )

def admin_confirm_sms(request, called_service):
    sender = UserProfile.objects.get(person =called_service.user)
    sennum = sender.phone_number
    phone = str(sennum)
    account_sid = tw_sid
    auth_token = tw_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Hi {called_service.order_service} admin, Your client has sucessfully closed the service you rendered with code {called_service.ref_code}. Kindly close this service from your end to receive your payment within the next 24 hours",
        from_='+12569608957',
        to= phone
    )

def client_confirm_sms(request, called_service):
    sender = UserProfile.objects.get(person =called_service.order_service.admin)
    sennum = sender.phone_number
    phone = str(sennum)
    account_sid = tw_sid
    auth_token = tw_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Hi {request.user}, A provider has sucessfully closed the service you ordered with code {called_service.ref_code}. Kindly close this service from your end to enable your payment to provider within the next 24 hours",
        from_='+12569608957',
        to= phone
    )