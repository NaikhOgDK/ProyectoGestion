def licencia_detalle(request, licencia_id):
    licencia = get_object_or_404(LicenciaConductor, id=licencia_id)

    # Obtener el nombre del archivo como cadena
    archivo_s3 = str(licencia.archivo.name)  # Asegurar que es una cadena
    #print(f"Archivo S3: {archivo_s3}")

    tiempo_expiracion = 240

    s3_client = boto3.client(
        's3',
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    # Generar URL temporal
    try:
        url_temporal = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': archivo_s3},
            ExpiresIn=tiempo_expiracion
        )
        #print(f"URL temporal generada: {url_temporal}")   
    except Exception as e:
        #print(f"Error al generar el enlace temporal: {e}")
        url_temporal = None

    return render(request, 'areas/documento/conductores/licencia_detalle.html', {'licencia': licencia, 'url_temporal': url_temporal})