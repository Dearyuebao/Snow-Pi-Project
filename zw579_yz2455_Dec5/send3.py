import sendgrid
# import thing
import os


def send():
    # api key

    print("start sending email")
    # client = sendgrid.SendGridClient(
    #     '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')
    client = sendgrid.SendGridClient(
        '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')

    message = sendgrid.Mail()
    message.add_to("yz2455@cornell.edu")
    message.set_from("zixiao1511034@outlook.com")
    message.set_subject("Deep Snow Alert!")
    message.set_html("Snow is deep, be careful!!")
    client.send(message)
    print("has sent email")


with open('/home/pi/Documents/rpiWebServer/test_fifo') as f:
    for line in f:
        print(line, type(line))
        if line == 'sendEmail\n':
            print("enter")
            send()
            print('finish')
            break
# while True:
#     import thing
#     if thing.signal == 1:
#         print("get signal from thing!")
#         #print "come into"
#         send()

# while True:
#     signal = thing.get_name()
#     if thing.signal == 1:
#         print("get signal from thing!")
#         # print "come into"
#         send()
#         break
