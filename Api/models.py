from django.db import models
from datetime import datetime

import json

def get_default(model, field):
    with open('COMPANY_DEFAULTS.json') as data_file:    
        data = json.load(data_file)

    return data[model][field]

def create_card_account():
    return 'NOT YET IMPLEMENTED'

# Create your models here.
class CompanyDefault(models.Model):
    airport_rate_park_day = models.DecimalField(default = get_default('Airport', 'rate_park_day'), max_digits = 5, decimal_places = 2)
    airport_rate_rent_day = models.DecimalField(default = get_default('Airport', 'rate_rent_day'), max_digits = 5, decimal_places = 2)
    airport_rate_valet = models.DecimalField(default = get_default('Airport', 'rate_valet'), max_digits = 5, decimal_places = 2)
    airport_rate_wash = models.DecimalField(default = get_default('Airport', 'rate_wash'), max_digits = 5, decimal_places = 2)
    airport_rate_detail = models.DecimalField(default = get_default('Airport', 'rate_detail'), max_digits = 5, decimal_places = 2)
    airport_rate_basic_cleaning_for_sublet = models.DecimalField(default = get_default('Airport', 'rate_basic_cleaning_for_sublet'), max_digits = 5, decimal_places = 2)
    airport_rate_itinerary_change_return_to_owner = models.DecimalField(default = get_default('Airport', 'rate_itinerary_change_return_to_owner'), max_digits = 5, decimal_places = 2)
    airport_rate_itinerary_change_per_mile_over_30_miles = models.DecimalField(default = get_default('Airport', 'rate_itinerary_change_per_mile_over_30_miles'), max_digits = 5, decimal_places = 2)
    airport_rate_valet_commission_park = models.DecimalField(default = get_default('Airport', 'rate_valet_commission_park'), max_digits = 5, decimal_places = 2)
    airport_rate_valet_commission_terminal = models.DecimalField(default = get_default('Airport', 'rate_valet_commission_terminal'), max_digits = 5, decimal_places = 2)
    airport_rate_valet_commission_fueling = models.DecimalField(default = get_default('Airport', 'rate_valet_commission_fueling'), max_digits = 5, decimal_places = 2)
    airport_rate_valet_commission_itinerary_change_return = models.DecimalField(default = get_default('Airport', 'rate_valet_commission_itinerary_change_return'), max_digits = 5, decimal_places = 2)
    airport_rate_valet_commission_empty_trip = models.DecimalField(default = get_default('Airport', 'rate_valet_commission_empty_trip'), max_digits = 5, decimal_places = 2)
    airport_rate_tax_1 = models.DecimalField(default = get_default('Airport', 'rate_tax_1'), max_digits = 5, decimal_places = 2)
    airport_rate_tax_2 = models.DecimalField(default = get_default('Airport', 'rate_tax_2'), max_digits = 5, decimal_places = 2)
    airport_rate_percent_sublet_paid_to_partner = models.DecimalField(default = get_default('Airport', 'rate_percent_sublet_paid_to_partner'), max_digits = 5, decimal_places = 2)
    airport_rate_percent_sublet_paid_to_auto_owner = models.DecimalField(default = get_default('Airport', 'rate_percent_sublet_paid_to_auto_owner'), max_digits = 5, decimal_places = 2)
    airport_rate_promotion_points = models.DecimalField(default = get_default('Airport', 'rate_promotion_points'), max_digits = 5, decimal_places = 2)

    partner_rate_park_day = models.DecimalField(default = get_default('Partner', 'rate_park_day'), max_digits = 5, decimal_places = 2)
    partner_rate_rent_day = models.DecimalField(default = get_default('Partner', 'rate_rent_day'), max_digits = 5, decimal_places = 2)
    partner_rate_valet = models.DecimalField(default = get_default('Partner', 'rate_valet'), max_digits = 5, decimal_places = 2)
    partner_rate_wash = models.DecimalField(default = get_default('Partner', 'rate_wash'), max_digits = 5, decimal_places = 2)
    partner_rate_detail = models.DecimalField(default = get_default('Partner', 'rate_detail'), max_digits = 5, decimal_places = 2)
    partner_rate_basic_cleaning_for_sublet = models.DecimalField(default = get_default('Partner', 'rate_basic_cleaning_for_sublet'), max_digits = 5, decimal_places = 2)
    partner_rate_itinerary_change_return_to_owner = models.DecimalField(default = get_default('Partner', 'rate_itinerary_change_return_to_owner'), max_digits = 5, decimal_places = 2)
    partner_rate_itinerary_change_per_mile_over_30_miles = models.DecimalField(default = get_default('Partner', 'rate_itinerary_change_per_mile_over_30_miles'), max_digits = 5, decimal_places = 2)
    partner_rate_valet_commission_park = models.DecimalField(default = get_default('Partner', 'rate_valet_commission_park'), max_digits = 5, decimal_places = 2)
    partner_rate_valet_commission_terminal = models.DecimalField(default = get_default('Partner', 'rate_valet_commission_terminal'), max_digits = 5, decimal_places = 2)
    partner_rate_valet_commission_fueling = models.DecimalField(default = get_default('Partner', 'rate_valet_commission_fueling'), max_digits = 5, decimal_places = 2)
    partner_rate_valet_commission_itinerary_change_return = models.DecimalField(default = get_default('Partner', 'rate_valet_commission_itinerary_change_return'), max_digits = 5, decimal_places = 2)
    partner_rate_valet_commission_empty_trip = models.DecimalField(default = get_default('Partner', 'rate_valet_commission_empty_trip'), max_digits = 5, decimal_places = 2)
    partner_rate_percent_sublet_paid_to_partner = models.DecimalField(default = get_default('Partner', 'rate_percent_sublet_paid_to_partner'), max_digits = 5, decimal_places = 2)
    partner_rate_percent_sublet_paid_to_auto_owner = models.DecimalField(default = get_default('Partner', 'rate_percent_sublet_paid_to_auto_owner'), max_digits = 5, decimal_places = 2)

def get_company_default(model, field):
    if len(CompanyDefault.objects.all()) != 1:
        return 0
    else:
        return getattr(CompanyDefault.objects.all()[0], model.lower() + '_' + field)

class Airport(models.Model):
    airport_code = models.CharField(max_length = 3, primary_key = True)
    airport_name = models.CharField(max_length = 50)
    valet_location = models.CharField(max_length = 50)
    minutes_pickup_delay_with_checkin = models.IntegerField(default = 0)
    minutes_pickup_delay_no_checkin = models.IntegerField(default = 0)

    rate_park_day = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_rent_day = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_wash = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_detail = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_basic_cleaning_for_sublet = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_itinerary_change_return_to_owner = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_itinerary_change_per_mile_over_30_miles = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet_commission_park = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet_commission_terminal = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet_commission_fueling = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet_commission_itinerary_change_return = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet_commission_empty_trip = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_tax_1 = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_tax_2 = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_percent_sublet_paid_to_partner = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_percent_sublet_paid_to_auto_owner = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_promotion_points = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)

    def save(self, *args, **kwargs):
        rate_members = [attr for attr in dir(self) if attr.startswith("rate_")]
        for rate in rate_members:
            setattr(self, rate, get_company_default('Airport', rate))
        super(Airport, self).save(*args, **kwargs)

class Partner(models.Model):
    partner_name = models.CharField(max_length = 50)
    partner_tax_id = models.CharField(max_length = 50)
    address = models.CharField(max_length = 50)
    primary_number = models.CharField(max_length = 50)
    secondary_number = models.CharField(max_length = 50)
    has_wash = models.BooleanField(default = False)
    has_detail = models.BooleanField(default = False)
    airport = models.ForeignKey(Airport, on_delete = models.CASCADE)
    partner_since = models.IntegerField(default = int(datetime.today().strftime('%Y')))
    cumulative_points = models.IntegerField(default = 0)
    available_points = models.IntegerField(default = 0)
    partner_level = models.CharField(max_length = 50, default = 'BASE')
    # partner_logo = models.ImageField()

    rate_park_day = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_rent_day = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_wash = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_detail = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_basic_cleaning_for_sublet = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_itinerary_change_return_to_owner = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_itinerary_change_per_mile_over_30_miles = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet_commission_park = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet_commission_terminal = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet_commission_fueling = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet_commission_itinerary_change_return = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_valet_commission_empty_trip = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_percent_sublet_paid_to_partner = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)
    rate_percent_sublet_paid_to_auto_owner = models.DecimalField(default = 0, max_digits = 5, decimal_places = 2)

    def save(self, *args, **kwargs):
        rate_members = [attr for attr in dir(self) if attr.startswith("rate_")]
        for rate in rate_members:
            setattr(self, rate, get_company_default('Partner', rate))
        super(Partner, self).save(*args, **kwargs)

class User(models.Model):
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    salt = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    primary_number = models.CharField(max_length = 50)
    secondary_number = models.CharField(max_length = 50)
    address = models.CharField(max_length = 50)
    license_expiration = models.DateField()
    license_number = models.CharField(max_length = 50)
    license_state = models.CharField(max_length = 50)
    member_since = models.IntegerField(default = int(datetime.today().strftime('%Y')))
    partner = models.ForeignKey(Partner, on_delete = models.CASCADE, blank = True, null = True, default = None)
    cumulative_points = models.IntegerField(default = 0)
    available_points = models.IntegerField(default = 0)
    email_validated = models.BooleanField(default = False)
    card_account_id = models.CharField(max_length = 50, default = create_card_account())

class Token(models.Model):
    token = models.TextField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

class Role(models.Model):
    name = models.CharField(max_length = 50, primary_key = True)
    description = models.CharField(max_length = 50)

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    role = models.ForeignKey(Role, on_delete = models.CASCADE)

class AutoType(models.Model):
    make = models.CharField(max_length = 50)
    model = models.CharField(max_length = 50)
    year = models.IntegerField()
    classification = models.CharField(max_length = 50)

class Auto(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    auto_type = models.ForeignKey(AutoType, on_delete = models.CASCADE)
    color = models.CharField(max_length = 50)
    license_plate = models.CharField(max_length = 50)
    premium_expected = models.BooleanField(default = False)
    prefered_gas_type = models.CharField(max_length = 50)
    hybrid = models.BooleanField(default = False)
    primary_auto = models.BooleanField(default = False)

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'target_user_itinerary')
    record_creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'origin_user_itinerary')
    date_created = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default = False)

class Sublettable(models.Model):
    # itinerary = models.ForeignKey(Itinerary, on_delete = models.CASCADE)
    auto = models.ForeignKey(Auto, on_delete = models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    available_for_rent = models.BooleanField(default = False)
    fuel = models.CharField(max_length = 50, default = 'NOT CHECKED')
    has_garage_opener = models.BooleanField(default = False)
    has_ez_pass = models.BooleanField(default = False)
    wash_condition = models.CharField(max_length = 50, default = 'NOT CHECKED')
    detail_condition = models.CharField(max_length = 50, default = 'NOT CHECKED')
    informed_cleaning = models.BooleanField(default = False)
    dent_condition = models.CharField(max_length = 50, default = 'NOT CHECKED')
    informed_condition = models.BooleanField(default = False)
    condition = models.TextField(default = 'NOT CHECKED')
    # condition_images = models.ImageField()
    stored_belongings = models.BooleanField(default = False)
    fuel_topped_amount = models.CharField(max_length = 50, default = 'NOT CHECKED')
    # fuel invoice = models.ImageField()
    record_creator = models.ForeignKey(User, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now = True)

class Park(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete = models.CASCADE)
    airport = models.ForeignKey(Airport, on_delete = models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete = models.CASCADE)
    auto = models.ForeignKey(Auto, on_delete = models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    wash_requested = models.BooleanField(default = False)
    detail_requested = models.BooleanField(default = False)
    record_creator = models.ForeignKey(User, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now = True)
    auto_returned_on = models.DateTimeField(blank = True, null = True)
