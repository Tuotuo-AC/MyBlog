import logging
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Post

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Post)
def generate_summary(sender, instance, created, **kwargs):
    """
    当文章状态变为 published 且没有摘要时，调用 DeepSeek API 生成摘要。
    """
    # 仅在文章已发布且 summary 为空（None 或空字符串）时生成
    if instance.status == 'published' and not instance.summary:
        # 内容不能太短
        if not instance.content or len(instance.content.strip()) < 50:
            logger.warning(f"Post {instance.id} 内容过短，跳过摘要生成")
            return

        api_key = settings.DEEPSEEK_API_KEY
        if not api_key:
            logger.error("未配置 DEEPSEEK_API_KEY，无法生成摘要")
            return

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        prompt = f"请用中文为以下文章生成一段150字以内的简洁摘要：\n\n{instance.content[:3000]}"
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 200
        }

        try:
            response = requests.post(
                settings.DEEPSEEK_API_URL,
                json=payload,
                headers=headers,
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                summary = data["choices"][0]["message"]["content"].strip()
                if len(summary) > 200:
                    summary = summary[:200] + "..."
                instance.summary = summary
                instance.save(update_fields=['summary'])
                logger.info(f"成功为文章 {instance.id} 生成摘要")
            else:
                logger.error(f"API 请求失败 {response.status_code}: {response.text}")
        except Exception as e:
            logger.error(f"生成摘要时出错: {str(e)}")
    else:
        logger.debug(f"文章 {instance.id} 不满足生成摘要条件")