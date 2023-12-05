import base64

encoded_text = '=?UTF-8?B?xJDDtCB0aOG7iyBow7NhLmRvY3g=?='

# Extract the encoded part of the string
encoded_part = encoded_text.split('?')[3]

# Decode the Base64 part to obtain the original UTF-8 text
decoded_text = base64.b64decode(encoded_part).decode('utf-8')

print(decoded_text)