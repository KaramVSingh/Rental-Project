import requests
import sys
import json
import pprint

from datetime import datetime, timedelta

URL = 'http://127.0.0.1:8000/'
LINE_BREAK = '=========================================================================='

def fail(message):
    print()
    print('FAILURE: ' + message)
    print(LINE_BREAK)
    sys.exit(-1)

def clear_database():
    if not requests.get(URL + 'cleardatabase/').ok:
        # we need to fail the test
        print(LINE_BREAK)
        print('Clearing the database did not return a successful status_code')
        fail('Please try again.')

def assert_equals(t1, t2, message):
    if t1 != t2:
        fail(message)

def dict_to_str(d):
    return str(d).replace("'", '"').replace('None', 'null').replace('False', 'false').replace('True', 'true')

def today():
    return datetime.today().strftime('%Y-%m-%d')

def tomorrow():
    return (datetime.today() + timedelta(1)).strftime('%Y-%m-%d')

def this_year():
    return int(datetime.today().strftime('%Y'))

def yesterday():
    return (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')

class tester:
    # this function calls all functions beginning with the word 'test_'
    def test(self):
        print('Initializing Testing.')
        clear_database()
        iterate = 1
        for name in dir(self):
            if name.startswith('test_'):
                print(LINE_BREAK)
                print(str(iterate) + '. ' + name + ': ')
                method = getattr(self, name)
                clear_database()
                method()
                print()
                print('SUCCESS')
                iterate += 1

        clear_database()
        print(LINE_BREAK)
        print()
        print('ALL TESTS SUCCESSFUL')

    # this is the standard api call to add a user to the database
    def test_users_create(self):
        print('Testing standard user post.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': 'HeadIsAFlame18!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        # now we need to check that the data we get back is correct
        correct_response = { 'pk': json.loads(r.text)['pk'], 'email': 'karamsingh175@gmail.com', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390', 'address': '## we are allowing any address I think ##', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'MD', 'partner': None, 'member_since': this_year(), 'cumulative_points': 0, 'available_points': 0, 'email_validated': False }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    # this is a call to the users view that is not a supported method
    def test_users_unsupported_method(self):
        print('Testing the error message when an unsupported method is used')
        r = requests.delete(URL + 'users/')

        if r.ok:
            fail('Test should have resulted in a 404 error.')

        # now we need to check that the error is appropriate
        correct_response = { 'error': 'Request method is unsupported.' }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    # this is the user api call without some fields
    def test_users_create_wo_fields(self):
        print('Testing user post with missing fields.')
        post_data = { 'email': 'karamsingh175@gmail.com', 'password': 'HeadIsAFlame18!', 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'secondary_number': ['This field is required.'], 'address': ['This field is required.'], 'license_expiration': ['This field is required.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    # this is the user api call with a partner
    def test_users_create_w_partner(self):
        print('Testing standard user post with a partner in the post.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': 'HeadIsAFlame18!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390', 'partner': 1 }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        # now we need to check that the data we get back is correct
        correct_response = { 'pk': json.loads(r.text)['pk'], 'email': 'karamsingh175@gmail.com', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390', 'address': '## we are allowing any address I think ##', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'MD', 'partner': None, 'member_since': this_year(), 'cumulative_points': 0, 'available_points': 0, 'email_validated': False }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    # this is the user api call with a partner without the password
    def test_users_create_w_partner_wo_password(self):
        print('Testing standard user post with a partner in the post and without a password in the post.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390', 'partner': 1 }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'password': ['This field is required.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    # now we should test the things that should prevent a user from being created
    # First we will try invalid email addresses:
    def test_users_create_invalid_email_1(self):
        print('Testing standard user post with an invalid email.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'FAKE', 'password': 'HeadIsAFlame18!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'email': ['Must enter a valid email address.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    # We will try invalid email addresses:
    def test_users_create_invalid_email_2(self):
        print('Testing standard user post with an invalid email.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': '@gmail.com', 'password': 'HeadIsAFlame18!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'email': ['Must enter a valid email address.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    # We will try using the same email twice:
    def test_users_create_email_twice(self):
        print('Testing standard user post with the same email twice.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': 'HeadIsAFlame18!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        # now we need to check that the data we get back is correct
        correct_response = { 'pk': json.loads(r.text)['pk'], 'email': 'karamsingh175@gmail.com', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390', 'address': '## we are allowing any address I think ##', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'MD', 'partner': None, 'member_since': this_year(), 'cumulative_points': 0, 'available_points': 0, 'email_validated': False }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'email': ['That email is already in use.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    # now we can test the password validators:
    def test_users_create_password_too_short(self):
        print('Testing standard user post with password that is too short.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': 'length7', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'password': ['Must be at least 8 characters long.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_password_long_enough(self):
        print('Testing standard user post with 8 character password.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': 'A1!Q1!!a', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        # now we need to check that the data we get back is correct
        correct_response = { 'pk': json.loads(r.text)['pk'], 'email': 'karamsingh175@gmail.com', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390', 'address': '## we are allowing any address I think ##', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'MD', 'partner': None, 'member_since': this_year(), 'cumulative_points': 0, 'available_points': 0, 'email_validated': False }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_password_no_special(self):
        print('Testing standard user post with no special characters in password.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': 'A1A1a1A1', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'password': ['Must contain one of the following characters: ~`!@#$%^&*()_-+={}|/,.<>?.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_password_no_upper(self):
        print('Testing standard user post with no upper case characters in password.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': 'a1!a1!a1', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'password': ['Must contain upper case letters.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_password_no_numbers(self):
        print('Testing standard user post with no numbers in password.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': 'aA!aA!a!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'password': ['Must contain numbers.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_password_no_lower(self):
        print('Testing standard user post with no lower case characters in password.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': '1A!1A!1!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'password': ['Must contain lower case letters.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_license_expiration_1(self):
        print('Testing standard user post with license expiration in the past.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': '1Aa!1A!1!', 'license_expiration': yesterday(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'license_expiration': ['The date you have entered is in the past.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_license_expiration_2(self):
        print('Testing standard user post with license expiration today.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': '1Aa!1A!1!', 'license_expiration': today(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'license_expiration': ['The date you have entered is in the past.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_license_expiration_3(self):
        print('Testing standard user post with license expiration with invalid date format.')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': '1Aa!1A!1!', 'license_expiration': '8/10/2050', 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'license_expiration': ['Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_license_state_1(self):
        print('Testing standard user post with invalid license state (not correct format).')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': '1Aa!1A!1!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'WOW', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'license_state': ['Must be entered as XX.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_license_state_2(self):
        print('Testing standard user post with invalid license state (not a state).')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': '1Aa!1A!1!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'ZZ', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'license_state': ['Must be a valid state code.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_primary_number_1(self):
        print('Testing standard user post with invalid phone number (has characters).')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': '1Aa!1A!1!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'MD', 'name': 'Karam Singh', 'primary_number': 'a434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'primary_number': ['Must be a valid phone number.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_users_create_primary_number_2(self):
        print('Testing standard user post with invalid phone number (11 characters).')
        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karamsingh175@gmail.com', 'password': '1Aa!1A!1!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'MD', 'name': 'Karam Singh', 'primary_number': '14434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        # now we need to check that the data we get back is correct
        correct_response = { 'primary_number': ['Must be 10 digits long.'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_login_standard(self):
        print('Testing the standard login api call.')
        self.test_users_create()
        post_data = { 'email': 'karamsingh175@gmail.com', 'password': 'HeadIsAFlame18!' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        correct_response = { 'token': json.loads(r.text)['token'], 'user': json.loads(r.text)['user'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_login_no_email(self):
        print('Testing the login without an email.')
        self.test_users_create()
        post_data = { 'email': '', 'password': 'HeadIsAFlame18!' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        correct_response = { 'email': 'Must provide email.' }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

        post_data = { 'password': 'HeadIsAFlame18!' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        correct_response = { 'email': 'Must provide email.' }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_login_no_password(self):
        print('Testing the login without a password.')
        self.test_users_create()
        post_data = { 'email': 'karamsingh175@gmail.com', 'password': '' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        correct_response = { 'password': 'Must provide password.' }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

        post_data = { 'email': 'karamsingh175@gmail.com' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        correct_response = { 'password': 'Must provide password.' }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_login_invalid_credentials(self):
        print('Testing the login with invalid credentials.')
        self.test_users_create()
        post_data = { 'email': 'karamsingh175@gmail.com', 'password': 'wowza' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        correct_response = { 'password': 'Incorrect password.' }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

        post_data = { 'email': 'karamsingh@gmail.com', 'password': 'HeadIsAFlame18!' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        correct_response = { 'email': 'Does not exist.' }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_login_double(self):
        print('Testing the login twice without logging out.')
        self.test_users_create()
        post_data = { 'email': 'karamsingh175@gmail.com', 'password': 'HeadIsAFlame18!' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        correct_response = { 'token': json.loads(r.text)['token'], 'user': json.loads(r.text)['user'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')
        
        r = requests.post(URL + 'login/', data = json.dumps(post_data))
        if not r.ok:
            fail('Request did not return a status_code of 200.')

        if correct_response['token'] == json.loads(r.text)['token']:
            fail('The token must change after relogging.')

        assert_equals(correct_response['user'], json.loads(r.text)['user'], 'The user must remain constant.')

    def test_logout_standard(self):
        print('Testing the standard logout with proper authentication.')
        self.test_users_create()
        post_data = { 'email': 'karamsingh175@gmail.com', 'password': 'HeadIsAFlame18!' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        correct_response = { 'token': json.loads(r.text)['token'], 'user': json.loads(r.text)['user'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

        headers = { 'AUTHENTICATION': json.loads(r.text)['token'] }
        r = requests.get(URL + 'logout/', headers = headers)

        if not r.ok:
            fail('Request did not return a status_code of 200.')

    def test_logout_no_auth(self):
        print('Testing the logout api without proper authentication')
        self.test_users_create()
        post_data = { 'email': 'karamsingh175@gmail.com', 'password': 'HeadIsAFlame18!' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        correct_response = { 'token': json.loads(r.text)['token'], 'user': json.loads(r.text)['user'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

        r = requests.get(URL + 'logout/')

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        correct_response = { 'error': 'You did not provide a valid token.'}
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_logout_twice(self):
        print('Testing the logout api without proper authentication')
        self.test_users_create()
        post_data = { 'email': 'karamsingh175@gmail.com', 'password': 'HeadIsAFlame18!' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        token = json.loads(r.text)['token']
        correct_response = { 'token': token, 'user': json.loads(r.text)['user'] }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

        headers = { 'AUTHENTICATION': token }
        r = requests.get(URL + 'logout/', headers = headers)

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        headers = { 'AUTHENTICATION': token }
        r = requests.get(URL + 'logout/', headers = headers)

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        correct_response = { 'error': 'You are already logged out.' }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

    def test_priviledges_1(self):
        print('Testing the innitial role creation and admin priviledges')
        self.test_users_create()

        post_data = { 'email': 'karamsingh175@gmail.com', 'password': 'HeadIsAFlame18!' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        token = json.loads(r.text)['token']
        user = json.loads(r.text)['user']

        headers = { 'AUTHENTICATION': token }
        r = requests.get(URL + 'roles/', headers = headers)
        correct_response = [{"name": "CONSUMER", "description": "Application user."}, {"name": "ADMINISTRATOR", "description": "Application owner."}]
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

        headers = { 'AUTHENTICATION': token }
        r = requests.get(URL + 'userroles/', headers = headers)

        correct_response = [{"pk": json.loads(r.text)[0]['pk'], "role": "ADMINISTRATOR", "user": user}, {"pk": json.loads(r.text)[1]['pk'], "role": "CONSUMER", "user": user}]
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

        post_data = { 'address': '## we are allowing any address I think ##', 'email': 'karam@gmail.com', 'password': 'HeadIsAFlame18!', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'md', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390' }
        r = requests.post(URL + 'users/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        # now we need to check that the data we get back is correct
        correct_response = { 'pk': json.loads(r.text)['pk'], 'email': 'karam@gmail.com', 'name': 'Karam Singh', 'primary_number': '4434746036', 'secondary_number': '4104650390', 'address': '## we are allowing any address I think ##', 'license_expiration': tomorrow(), 'license_number': 'We are allowing anything right now?', 'license_state': 'MD', 'partner': None, 'member_since': this_year(), 'cumulative_points': 0, 'available_points': 0, 'email_validated': False }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

        post_data = { 'email': 'karam@gmail.com', 'password': 'HeadIsAFlame18!' }
        r = requests.post(URL + 'login/', data = json.dumps(post_data))

        if not r.ok:
            fail('Request did not return a status_code of 200.')

        token = json.loads(r.text)['token']
        user = json.loads(r.text)['user']

        headers = { 'AUTHENTICATION': token }
        r = requests.get(URL + 'roles/', headers = headers)

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        correct_response = { 'error': 'User does not have required priviledges.' }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

        r = requests.get(URL + 'roles/')

        if r.ok:
            fail('Test should have resulted in a 400 error.')

        correct_response = { 'error': 'User does not have required priviledges.' }
        assert_equals(dict_to_str(correct_response), r.text, 'The response did not match the correct response.')

tester().test()
tester().test_users_create()