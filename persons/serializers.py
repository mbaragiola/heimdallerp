from persons import models
from rest_framework.serializers import HyperlinkedModelSerializer


class PhysicalAddressSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.PhysicalAddress
        fields = (
            'url',
            'id',
            'street_address',
            'floor_number',
            'apartment_number',
            'locality',
            'postal_code'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:persons:physicaladdress-detail'
            },
            'locality': {
                'view_name': 'api:geo:locality-detail',
                'required': False,
                'allow_null': True
            }
        }


class CompanySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Company
        fields = (
            'url',
            'id',
            'fantasy_name',
            'slogan',
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:persons:company-detail'
            }
        }
