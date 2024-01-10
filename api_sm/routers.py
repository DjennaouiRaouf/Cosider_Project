class AppRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'api_sm':
            return 'default'


        return None

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'api_sch':
            return 'ca_ch'


        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'api_sm':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'api_sm' or obj2._meta.app_label == 'api_sm':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'api_sm' and db == 'default':
            return True
        else:
            return False