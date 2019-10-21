import random

# 缓存数据的有效期          单位秒
# CACHE_TTL = 60 * 60
# CACHE_TIMEDELTA = 2 * 60
# CACHE_NOT_EXISTS = 5 * 60
#
# def get_val():
#     return CACHE_TTL + random.randint(1,CACHE_TIMEDELTA)

class CacheTTL(object):
    CACHE_TTL = 60 * 60
    CACHE_TIMEDELTA = 2 * 60

    @classmethod
    def get_val(cls):
        return cls.CACHE_TTL + random.randint(1, cls.CACHE_TIMEDELTA)

class CacheUserTTL(CacheTTL):
    CACHE_TIMEDELTA = 5 * 60
    pass

class CacheNotExistsTTL(CacheTTL):
    CACHE_TTL = 5 * 60
    CACHE_TIMEDELTA = 1 * 60

class CacheUserFollowingTTL(CacheTTL):
    pass

class CacheArticlesTTL(CacheTTL):
    pass

class CacheCommentsTTL(CacheTTL):
    pass