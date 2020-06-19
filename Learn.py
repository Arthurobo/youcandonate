from PIL import Image, ImageFilter
from django.urls import reverse
from django.core.files.storage import default_storage
from django.conf.global_settings import DEFAULT_FILE_STORAGE
from io import BytesIO
from PIL import Image
import io
from django.core.files.storage import default_storage as storage


def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    img_read = storage.open(self.img.name, 'rb')
    img = Image.open(img_read)

    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        in_mem_file = io.BytesIO()
        img.save(in_mem_file, format='JPEG')
        img_write = storage.open(self.img.name, 'w+')
        img_write.write(in_mem_file.getvalue())
        img_write.close()

    img_read.close()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Load Image from File
        img_read = storage.open(self.img.name, 'rb')
        img = Image.open(img_read)

        # Convert Image to Array
        pixels = asarray(img)
        # Create the Detector Using the Default Weights
        detector = MTCNN()
        # Detect Faces in the Image
        results = detector.detect_faces(pixels)
        numfaces = len(results)
        # Create For Loop to Blur All Faces in Photo
        for i in range(numfaces):
            # Extract the Bounding Box from the First Face
            x1, y1, width, height = results[i]['box']
            # Negative Coordinates Bug Fix
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height
            # Extract the Face
            face = pixels[y1:y2, x1:x2]
            # Blur Out Face Pixels
            faceimage = Image.fromarray(face)
            faceimage = faceimage.filter(ImageFilter.BoxBlur(radius=100))
            # Reattach Blurred Faces to Original Photo
            img = img.copy()
            img.paste(faceimage, (x1, y1))
        # Show the New Image
        # image.show()
        # Save the New Image
        in_mem_file = io.BytesIO()
        img.save(in_mem_file, format='JPEG')
        #img.save(self.img.path)


