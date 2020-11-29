#https://django-extensions.readthedocs.io/en/latest/graph_models.html

./manage.py graph_models util customer hcauth lender realtor concierge property event service_provider -g -X HomeCaptainAbstractBaseModel,AbstractCertificationModel,AbstractBaseUser -o homecaptain_models.png
