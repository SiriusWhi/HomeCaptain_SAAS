from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from .models import HomeCaptainUser, HomeCaptainRecommend, Favorite


class FavoriteMixin(models.Model):
    favorited_entities = GenericRelation(Favorite,
                                       content_type_field='favoriting_content_type',
                                       object_id_field='favoriting_object_id')

    def get_favorited_ids(self, favorited_content_type):
        return self.favorited_entities.filter(
            favorited_content_type=favorited_content_type).\
            values_list('favorited_object_id', flat=True)
    
    def favorite(self, favorited_content_type, favorited_object_id):
        favorite, created = Favorite.objects.get_or_create(
                    favoriting_content_type=self.content_type,
                    favoriting_object_id=self.id,
                    favorited_content_type=favorited_content_type,
                    favorited_object_id=favorited_object_id)
        favorite.save()
        return (favorite, created)
        
    def unfavorite(self, favorited_contented_type, favorited_object_id):
        try:
            favorite = Favorite.objects.get(
                favoriting_content_type=self.content_type,
                favoriting_object_id=self.id,
                favorited_content_type=favorited_contented_type,
                favorited_object_id=favorited_object_id)
            favorite.delete()
            return True
        except Favorite.DoesNotExist:
            return False

    class Meta:
        abstract = True    


class FavoritedMixin(models.Model):
    favorite_users = models.ManyToManyField(
        HomeCaptainUser,
        related_name='favorite_%(class)s',
        blank=True
    )
    favorite_count = models.IntegerField(default=0, blank=True, null=True)

    
    def add_favorite_user(self, user):
        self.favorite_users.add(user)
        self.favorite_count += 1
        self.save()

    def remove_favorite_user(self, user):
        self.favorite_users.remove(user)
        self.favorite_count -= 1
        self.save()
    
    class Meta:
        abstract = True


class RecommendMixin(models.Model):
    recommended_users = models.ManyToManyField(
        HomeCaptainRecommend,
        related_name='recommended_%(class)s',
        blank=True,
    )

    def recommended_users_count():
        return recommended_users.all().count()

    class Meta:
        abstract = True    
