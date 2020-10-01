


# class StoresViewPrePurchase(TemplateView):
#     template_name = 'templates_stores/stores_pre_purchase.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(StoresViewPrePurchase, self).get_context_data(**kwargs)
#
#         # auth0_uid, auth0_first_name, auth0_last_name, auth0user_email = self.enrich_user_info()
#         auth0_uid, auth0_first_name, auth0_last_name, auth0user_email = extract_user_info(self.request)
#         context['auth0_uid'] = auth0_uid
#         context['auth0user_email'] = auth0user_email
#
#         return context
#
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         auth0user_email = context['auth0user_email']
#         auth0_uid = context['auth0_uid']
#
#         logger.info(f"getting crb_user_id for auth0_uid [{auth0_uid}]")
#         crb_userid, crb_site = get_or_create_crb_user(auth0_uid, auth0user_email)
#
#         # context['crb_userid'] = crb_userid
#         # hosted_page = ChargebeeManager().create_checkout(crb_user_id=crb_userid, plan_id='cbdemo_free')
#         # logger.info(f"retrieved hosted_page [{str(hosted_page.url)}]")
#         # return redirect(hosted_page.url)


# class StoresViewReturnPage(TemplateView):
#     template_name = 'templates_stores/stores_pre_purchase.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(StoresViewReturnPage, self).get_context_data(**kwargs)
#
#         subscription_id = self.request.GET.get('subid', None)
#         customer_id = self.request.GET.get('cid', None)
#         plan_id = self.request.GET.get('pid', None)
#         logger.info(f"got customer_id [{customer_id}] plan_id [{plan_id}] subscription_id [{subscription_id}]")
#         context['subscription_id'] = subscription_id
#         context['customer_id'] = customer_id
#         context['plan_id'] = plan_id
#
#         auth0_uid, auth0_first_name, auth0_last_name, auth0user_email = extract_user_info(self.request)
#         context['auth0_uid'] = auth0_uid
#         context['auth0user_email'] = auth0user_email
#
#         return context
#
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#
#         got_subscription_id = context['subscription_id']
#         got_customer_id = context['customer_id']
#         got_plan_id = context['plan_id']
#         auth0_uid = context['auth0_uid']
#         auth0user_email = context['auth0user_email']
#
#         logger.info(f"getting crb_user_id for auth0_uid [{auth0_uid}]")
#         crb_userid, crb_site = get_or_create_crb_user(auth0_uid, auth0user_email, create_if_dont_exist=False)
#
#         # verification:
#         # need to verify customer_id is what we have in auth0 data
#         # why? because otherwise users could pretend to be other users (given customer_id)..
#
#         logger.info(f"from request got_customer_id: [{got_customer_id}] from crb: [{crb_userid}]")
#         if got_customer_id != crb_userid:
#             logger.error(f"not equal customer id!!! request got_customer_id: [{got_customer_id}] from crb: [{crb_userid}]")
#             return HttpResponseBadRequest(content='bad request parameters')
#
#
#         subscription, customer = ChargebeeManager().get_subscription(subscription_id=got_subscription_id)
#         if subscription is None or customer is None:
#             logger.error(f"subscription or customer are None!")
#             return HttpResponseBadRequest(content='bad request parameters')
#
#         # verify the specified subscription belongs to the given user
#         if customer.id != crb_userid:
#             logger.error(f"error with customer id: customer.id [{customer.id}] crb_userid [{crb_userid}]")
#             return HttpResponseBadRequest(content='bad request parameters')
#
#
#         # # context['crb_userid'] = crb_userid
#         # hosted_page = ChargebeeManager().create_checkout(crb_user_id=crb_userid, plan_id='cbdemo_free')
#         # logger.info(f"retrieved hosted_page [{str(hosted_page.url)}]")
#         # redirect is shotcut for HttpResponseRedirect: https://realpython.com/django-redirects/#django-redirects-a-super-simple-example
#         return redirect(reverse('view_stores_home'))



# # @csrf_exempt    ## TODO: This is for test only! Add CSRF Support..
# @require_POST
# def generate_checkout_new_or_existing_url(request):
#     # chargebee.configure("test_jqXGuQLkBHUSR2PM0qgUV21W1VqSFJIU", "honeycomics-v3-test")
#     chargebee.configure("test_qDNCoDWdlzgkepytSgFgcucch5lrqWXsh", "cartstuff-test")
#
#     plan_id = None
#     if 'plan_id' in request.POST:
#         plan_id = request.POST['plan_id']
#     if plan_id is None:
#         return HttpResponseBadRequest("no plan_id specified")
#
#     auth0_uid, auth0_first_name, auth0_last_name, auth0user_email = extract_user_info(request)
#     crb_userid, crb_site = get_or_create_crb_user(auth0_uid, auth0user_email)
#
#     # https://apidocs.chargebee.com/docs/api/hosted_pages#checkoutExisting-usecases
#     result = chargebee.HostedPage.checkout_existing({
#         "subscription": {
#             # "id": "16CHNjS8hwmvwFTk"
#             "id": "16CHNjS8hyk7TFYn",
#             # "plan_id": "cbdemo_grow"
#             "plan_id": "cbdemo_hustle"      # new plan
#         }
#     })
#     hosted_page = result._response['hosted_page']
#     data = hosted_page
#     print("return data:", str(data))
#     return JsonResponse(data)

# @csrf_exempt    ## TODO: This is for test only! Add CSRF Support..
# @require_POST
# def generate_checkout_existing_url(request):
#     # chargebee.configure("test_jqXGuQLkBHUSR2PM0qgUV21W1VqSFJIU", "honeycomics-v3-test")
#     chargebee.configure("test_qDNCoDWdlzgkepytSgFgcucch5lrqWXsh", "cartstuff-test")
#
#     plan_id = None
#     if 'plan_id' in request.POST:
#         plan_id = request.POST['plan_id']
#     if plan_id is None:
#         return HttpResponseBadRequest("no plan_id specified")
#
#     auth0_uid, auth0_first_name, auth0_last_name, auth0user_email = extract_user_info(request)
#     crb_userid, crb_site = get_or_create_crb_user(auth0_uid, auth0user_email)
#
#     # https://apidocs.chargebee.com/docs/api/hosted_pages#checkoutExisting-usecases
#     result = chargebee.HostedPage.checkout_existing({
#         "subscription": {
#             # "id": "16CHNjS8hwmvwFTk"
#             "id": "16CHNjS8hyk7TFYn",   #customer lasttttt
#             # "plan_id": "cbdemo_grow"
#             "plan_id": "cbdemo_hustle"
#         }
#     })
#     hosted_page = result._response['hosted_page']
#     data = hosted_page
#     print("return data:", str(data))
#     return JsonResponse(data)


# @csrf_exempt    # otherwise POST request by Chargebee will return 403 Forbidden error
# def Webhook_webhook_test_1(request):
#     webhook_secret = request.GET.get('secret', 1)
#
#     if webhook_secret != settings.CB_WEBHOOK_CREDENTIALS_SECRET:
#         return HttpResponseNotAllowed("error wrong secret")
#
#     auth_header = request.META.get('HTTP_AUTHORIZATION', '')
#     token_type, _, credentials = auth_header.partition(' ')
#     credentials_actual = base64.b64decode(credentials).decode()
#     credentials_expected = settings.CB_WEBHOOK_CREDENTIALS_BASIC_AUTH_VAL_SECRET
#     print(f"credentials_actual: [{credentials_actual}]")
#     if token_type != 'Basic' or credentials_actual != credentials_expected:
#         return HttpResponse("error - wrong credentials!", status=401)
#
#     return HttpResponse("thanks!")
#
