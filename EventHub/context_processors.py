import settings

def config(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'WEB_ROOT': settings.WEB_ROOT,
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID}