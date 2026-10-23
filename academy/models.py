"""Entidades de catálogo; sin cuentas, roles ni datos personales en servidor."""
import uuid
from django.db import models
class BaseModel(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: abstract=True
class Lesson(BaseModel):
    number=models.PositiveIntegerField(unique=True)
    title=models.CharField(max_length=200)
    concept=models.TextField()
    source_path=models.CharField(max_length=400)
    class Meta: ordering=['number']
