from django.utils.crypto import get_random_string


# https://stackoverflow.com/a/43256732/15473443 - Slightly modified for my concept
def get_random_slug(obj):
    if not obj.slug or obj.slug == '':
        obj.slug = get_random_string(6)
        slug_is_wrong = True
        while slug_is_wrong:
            slug_is_wrong = False
            other_objs_with_slug = type(obj).objects.filter(slug=obj.slug).first()
            if other_objs_with_slug is not None:
                slug_is_wrong = True
            if slug_is_wrong:
                obj.slug = get_random_string(6)
