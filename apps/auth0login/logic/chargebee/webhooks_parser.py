# #!/usr/bin/python3
# import json
#
#
# def do_test_01_subscription_created_webhook():
#     filepath = r'K:\resources\chargebee\subscription created webhook.txt'
#     body = open(filepath, 'r', encoding='utf-8').read()
#     j_body = json.loads(body)
#
#     event_type = j_body['event_type']
#     customer_id = j_body['content']['subscription']['customer_id']
#     next_billing_at = j_body['content']['subscription']['plan_id']['next_billing_at']
#
# def do_tests():
#
# if __name__ == '__main__':
#     do_tests()
