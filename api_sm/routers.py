class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'api_sm':
            return 'default'
        elif model._meta.app_label == 'api_sch':
            return 'ca_ch'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'api_sm':
            return 'default'
        elif model._meta.app_label == 'api_sch':
            return 'ca_ch'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'api_sm' and obj2._meta.app_label == 'api_sch':
            return True
        elif obj1._meta.app_label == 'api_sch' and obj2._meta.app_label == 'api_sm':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ['api_sm', 'api_sch']:
            return db in ['default', 'ca_ch']
        return None