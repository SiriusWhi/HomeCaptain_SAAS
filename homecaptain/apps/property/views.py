from datetime import datetime

from django.conf import settings
from geocodio import GeocodioClient
from geocodio.exceptions import GeocodioDataError
from rest_framework import (
    status,
    generics,
    permissions,
    mixins,
    viewsets,
)
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.util.utils import get_logger
from .models import PropertyPhoto
from .serializers import PropertyPhotoOnDemandSerializer, PropertyGeocodingSerializer

class PropertyPhotoOnDemandView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    request: /api/property/photo/{photo.uid}/
    
    The first time ever the photo with the given UID is requested it will take some time
    because the photo is getting transfered from ListhHub to Our S3
    So make sure to display a loading gif
    
    The next time the same photo UID is requested, it will just get the presigned URL 
    from our S3
    
    success response: 
    ```
    {
        "s3_url": "https://homecaptainlocal.s3............." 
    }
    ```
    Which is valid for 10 minutes.
    
    failure response:
    1) 404 - the photo with the specified UID is not found
    2) error: 
    ```
    {
        "error": "technical error reason" #you shall NOT display this.
    }
    ```
    """

    queryset = PropertyPhoto.objects.all()
    serializer_class = PropertyPhotoOnDemandSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'

class GeocodingView(GenericAPIView):
    serializer_class = PropertyGeocodingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    logger = get_logger('GeocodingView')

    def post(self, request, *args, **kwargs):
        """
        API to batch encode property addresses
        ---
        serializer: .serializers.PropertyGeocodingSerializer

        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 403
              message: Insufficient rights to call this procedure

        consumes:
            - application/json
        produces:
            - application/json
        """
        serializer = PropertyGeocodingSerializer(data=request.data)
        if serializer.is_valid():
            uids = serializer.data['addresses'].keys()
            ##had to explicitly cast to list, .values() object was resulting
            ##in Geocodio to return wierd error!
            addresses = list(serializer.data['addresses'].values())
            client = GeocodioClient(settings.GEOCODIO_API_KEY)
            self.logger.debug("addresses: %s" % addresses)
            try:
                geocoded_addresses = client.geocode(addresses)
                data = {"geocodes" : dict(zip(uids, geocoded_addresses.coords))}
                return Response(data)
            except GeocodioDataError as e:
                data = {"error": str(e),}
            del cient
        else:
            data = serializer.errors
            
        return Response(data, status=status.HTTP_400_BAD_REQUEST)            
