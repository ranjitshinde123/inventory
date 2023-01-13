from django.test import TestCase

# Create your tests here.
import re

a=input('Enter the email')
b=re.fullmatch('[A-Za-z0-9.]@gmail[.]com',a)
if b:
    print("Right")
else:
    print("Wrong")