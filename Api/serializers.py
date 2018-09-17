from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from datetime import datetime, date, timedelta
from django.utils import timezone
from Api.helper import *
from Api.models import *

import re

PASSWORD_MINIMUM_LENGTH = 8
STATE_CODES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

class ParkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Park
        fields = ('pk', 'itinerary', 'airport', 'partner', 'auto', 'start', 'end', 'wash_requested', 'detail_reqested', 'record_creator', 'date_created', 'auto_returned_on')
        read_only_fields = ('pk', 'record_creator', 'date_created')

class SublettableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sublettable
        fields = ('pk', 'auto', 'available_for_rent', 'fuel', 'has_garage_opener', 'has_ez_pass', 'wash_condition', 'detail_condition', 'informed_cleaning', 'condition', 'stored_belongings', 'fuel_topped_amount', 'record_creator', 'date_created')
        read_only_fields = ('pk', 'date_created', 'record_creator', 'auto')

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ('pk', 'user', 'record_creator', 'date_created', 'active')
        read_only_fields = ('pk', 'date_created', 'active')

class CompanyDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDefault
        fields = '__all__'

class AutoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoType
        fields = ('pk', 'make', 'model', 'year', 'classification')

class GET_AutoSerializer(serializers.ModelSerializer):
    auto_type = AutoTypeSerializer(many = False)
    class Meta:
        model = Auto
        fields = ('pk', 'user', 'auto_type', 'color', 'license_plate', 'premium_expected', 'prefered_gas_type', 'hybrid', 'primary_auto')

class POST_AutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auto
        fields = ('pk', 'user', 'auto_type', 'color', 'license_plate', 'premium_expected', 'prefered_gas_type', 'hybrid', 'primary_auto')

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ('airport_code', 'airport_name', 'valet_location', 'minutes_pickup_delay_with_checkin', 'minutes_pickup_delay_no_checkin', 'rate_park_day', 'rate_rent_day', 'rate_valet', 'rate_wash', 'rate_detail', 'rate_basic_cleaning_for_sublet', 'rate_itinerary_change_return_to_owner', 'rate_itinerary_change_per_mile_over_30_miles', 'rate_valet_commission_park', 'rate_valet_commission_terminal', 'rate_valet_commission_fueling', 'rate_valet_commission_itinerary_change_return', 'rate_valet_commission_empty_trip', 'rate_tax_1', 'rate_tax_2', 'rate_percent_sublet_paid_to_partner', 'rate_percent_sublet_paid_to_auto_owner', 'rate_promotion_points')

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ('pk', 'partner_name', 'airport', 'partner_tax_id', 'address', 'primary_number', 'secondary_number', 'has_wash', 'has_detail', 'partner_since', 'cumulative_points', 'available_points', 'partner_level', 'rate_park_day', 'rate_rent_day', 'rate_valet', 'rate_wash', 'rate_detail', 'rate_basic_cleaning_for_sublet', 'rate_itinerary_change_return_to_owner', 'rate_itinerary_change_per_mile_over_30_miles', 'rate_valet_commission_park', 'rate_valet_commission_terminal', 'rate_valet_commission_fueling', 'rate_valet_commission_itinerary_change_return', 'rate_valet_commission_empty_trip', 'rate_percent_sublet_paid_to_partner', 'rate_percent_sublet_paid_to_auto_owner')
        read_only_fields = ('pk', 'partner_since', 'cumulative_points', 'available_points')

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('pk', 'role', 'user')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name', 'description')

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('token', 'user')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    salt = serializers.CharField(write_only = True, default = '')

    class Meta:
        model = User
        fields = ('pk', 'email', 'password', 'salt', 'name', 'primary_number', 'secondary_number', 'address', 'license_expiration', 'license_number', 'license_state', 'partner', 'member_since', 'cumulative_points', 'available_points', 'email_validated')
        read_only_fields = ('pk', 'member_since', 'cumulative_points', 'available_points', 'email_validated')

    # create function needs a small change in order to make the password include the salt
    def create(self, validated_data):
        data = validated_data.copy()
        data['password'] = make_password(data['password'] + data['salt'])
        return super(UserSerializer, self).create(data)

    # secondary_number validator:
    def validate_secondary_number(self, secondary_number):
        try:
            int(secondary_number)
        except ValueError:
            raise serializers.ValidationError('Must be a valid phone number.')

        if len(secondary_number) != 10:
            raise serializers.ValidationError('Must be 10 digits long.')

        return secondary_number

    # primary_number validator:
    def validate_primary_number(self, primary_number):
        try:
            int(primary_number)
        except ValueError:
            raise serializers.ValidationError('Must be a valid phone number.')
            
        if len(primary_number) != 10:
            raise serializers.ValidationError('Must be 10 digits long.')

        return primary_number

    # address validator:
    def validate_address(self, address):
        # https://www.ups.com/us/en/services/technology-integration/us-address-validation.page?
        return address

    # partner validator:
    def validate_partner(self, partner):
        # return None
        return partner

    # license_expiration validator:
    def validate_license_expiration(self, license_expiration):
        if license_expiration <= datetime.today().date():
            raise serializers.ValidationError('The date you have entered is in the past.')

        return license_expiration

    # license_state validator:
    def validate_license_state(self, license_state):
        license_state = license_state.upper()
        if not re.match(r'^[A-Z]{2}$', license_state):
            raise serializers.ValidationError('Must be entered as XX.')

        if not license_state in STATE_CODES:
            raise serializers.ValidationError('Must be a valid state code.')

        return license_state

    # license_number validator:
    def validate_license_number(self, license_number):
        # https://stackoverflow.com/questions/1021362/help-with-drivers-license-number-validation-regex
        return license_number

    # name validator:
    def validate_name(self, name):
        if not re.match(r"^[a-zA-Z ,.'-]+$", name):
            raise serializers.ValidationError('The name you entered is not a valid name.')

        return name

    # salt validator:=
    def validate_salt(self, salt):
        return random_string(5)

    # password validator:
    # checks that the password is long enough
    # checks that the password contains a special character
    # checks that the password contains a capital letter
    # checks that the password contains numbers
    # checks that the password contains lower case latters
    def validate_password(self, password):
        if len(password) < PASSWORD_MINIMUM_LENGTH:
            raise serializers.ValidationError('Must be at least ' + str(PASSWORD_MINIMUM_LENGTH) + ' characters long.')

        if not re.search(r'[~`!@#$%^&*()_+={}|/",.<>?-]', password):
            raise serializers.ValidationError('Must contain one of the following characters: ~`!@#$%^&*()_-+={}|/,.<>?.')

        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError('Must contain upper case letters.')

        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError('Must contain numbers.')
            
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError('Must contain lower case letters.')
        
        return password

    # email validator:
    def validate_email(self, email):
        if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
            raise serializers.ValidationError('Must enter a valid email address.')
        
        if len(User.objects.filter(email = email)) > 0:
            raise serializers.ValidationError('That email is already in use.')

        return email