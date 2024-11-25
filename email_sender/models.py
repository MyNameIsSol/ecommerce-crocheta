from django.db import models

# Create your models here.

class EmailLog(models.Model):
    subject = models.CharField(max_length=255)
    recipient = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to {self.recipient} on {self.sent_at}"
    
    class Meta:
        verbose_name_plural = "Send Email To Users"