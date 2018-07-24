import os
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_file_extension_and_size(value):
	valid_extensions = ['.jpg','.png','.mp4','.gif']
	MAX_UPLOAD_SIZE = 5242880
	ext = os.path.splitext(value.name)[1]
	if not ext.lower() in valid_extensions:
		raise ValidationError(_('Unsupported file extension.'))
	if ext.lower() in valid_extensions:
		if value.size > MAX_UPLOAD_SIZE :
				raise ValidationError(
            	 _('%(file_name)s has not been uploaded: File too big.'))