from django.apps import AppConfig


class ArticleConfig(AppConfig):
    name = 'article'

    def ready(self):
        import article.signals
        # print("✅ article signals loaded")  # 添加这一行