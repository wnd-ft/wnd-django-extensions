from django.test import TestCase

from sample_app.models import User, VendorInformation, VendorStaff, Vendor, AnSns


class WndModelMixinTests(TestCase):
    def setUp(self):
        super(WndModelMixinTests, self).setUp()
        an_sns = AnSns.objects.create(sns_id="an_sns_sns_id")

        user = User.objects.create(
            name="user_name",
            an_sns=an_sns
        )

        vendor_information = VendorInformation.objects.create()

        vendor = Vendor.objects.create(
            user=user,
            information=vendor_information,
            corporate_number=123456789,
            name="vendor_name"
        )

        self.vendor = vendor

        VendorStaff.objects.create(vendor=vendor, email="vendor_staff1_email")
        VendorStaff.objects.create(vendor=vendor, email="vendor_staff2_email")

    def test_to_dict(self):
        self.assertEqual(self.vendor.to_dict(
            field_name_list=[]
        ), {'id': 1})

        self.assertEqual(self.vendor.to_dict(
            field_name_list=[
                'name',
                'corporate_number',
            ]
        ), {'id': 1, 'name': 'vendor_name', 'corporate_number': 123456789})

        self.assertEqual(self.vendor.to_dict(
            field_name_list=[
                'user'
            ]
        ), {'id': 1, 'user': {'id': 1, 'name': 'user_name'}})

        self.assertEqual(self.vendor.to_dict(
            field_name_list=[
                'user__name'
            ]
        ), {'id': 1, 'user': {'id': 1, 'name': 'user_name'}})

        self.assertEqual(self.vendor.to_dict(
            field_name_list=[
                'user__an_sns__sns_id'
            ]
        ), {'id': 1, 'user': {'id': 1, 'an_sns': {'id': 1, 'sns_id': 'an_sns_sns_id'}}})

        self.assertEqual(self.vendor.to_dict(
            field_name_list=[
                'name',
                'corporate_number',
                'user',
            ]
        ), {'id': 1, 'name': 'vendor_name', 'corporate_number': 123456789, 'user': {'id': 1, 'name': 'user_name'}})

        self.assertEqual(self.vendor.to_dict(
            field_name_list=[
                'name',
                'corporate_number',
                'user__name',
                'user__an_sns__sns_id',
            ]
        ), {'id': 1,
            'name': 'vendor_name',
            'corporate_number': 123456789,
            'user':
                {'id': 1,
                 'name': 'user_name',
                 'an_sns':
                     {'id': 1,
                      'sns_id':
                          'an_sns_sns_id'}}}
        )

        self.assertEqual(self.vendor.to_dict(
            field_name_list=[
                'name',
                'corporate_number',
                'staffs__email'
            ]
        ), {'id': 1, 'name': 'vendor_name', 'corporate_number': 123456789,
            'staffs': [{'id': 1, 'email': 'vendor_staff1_email'}, {'id': 2, 'email': 'vendor_staff2_email'}]})

        self.assertEqual(self.vendor.to_dict(
            field_name_list=[
                'name',
                'corporate_number',
                'staffs'
            ]
        ), {'id': 1, 'name': 'vendor_name', 'corporate_number': 123456789, 'staffs':
            [{'id': 1, 'email': 'vendor_staff1_email'}, {'id': 2, 'email': 'vendor_staff2_email'}]}
        )
